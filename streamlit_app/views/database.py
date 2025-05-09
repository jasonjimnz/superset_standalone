"""
Database Operations View

The data management hub of our application - where all your generated datasets
come together. Connect to databases, run SQL queries, export your data to CSV,
or transfer it to PostgreSQL for more advanced analysis. This is where your
test data becomes truly useful for development and testing.
"""

import os
import streamlit as st
import pandas as pd
import duckdb
import psycopg2
from psycopg2.extras import execute_values
from io import StringIO

# Global variables for database connections
DUCKDB_PATH = "datasets.duckdb"

def get_duckdb_connection():
    """
    Opens up a connection to our local DuckDB database where all your generated data lives.

    This is our go-to lightweight database that powers everything in the app.
    It's fast, requires no setup, and works right out of the box.
    """
    return duckdb.connect(DUCKDB_PATH)

def get_postgres_connection(host, port, dbname, user, password):
    """
    Connects to your PostgreSQL database for more serious data operations.

    When you're ready to move beyond our built-in DuckDB and work with a full-featured
    database system, this function handles all the connection details. Just provide
    your PostgreSQL credentials, and we'll establish a secure connection to your server.

    If anything goes wrong with the connection, we'll show a friendly error message
    instead of crashing.
    """
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to PostgreSQL: {e}")
        return None

def execute_duckdb_query(query, params=None):
    """
    Runs your SQL queries against our DuckDB database and returns the results.

    This is the workhorse function that powers all our data operations. Give it
    any SQL query, and it'll return the results as a pandas DataFrame ready for
    display or further processing. We handle all the connection details and error
    checking behind the scenes.
    """
    try:
        conn = get_duckdb_connection()
        if params:
            result = conn.execute(query, params).fetchdf()
        else:
            result = conn.execute(query).fetchdf()
        conn.close()
        return result
    except Exception as e:
        st.error(f"Error executing DuckDB query: {e}")
        return pd.DataFrame()

def execute_postgres_query(conn, query, params=None):
    """
    Sends your SQL commands to PostgreSQL and brings back the results.

    Similar to our DuckDB query function, but for PostgreSQL databases. We're smart
    about handling different types of queries - SELECT statements return data, while
    other commands (like INSERT or UPDATE) return success status and row counts.

    We also take care of transactions - automatically committing successful changes
    and rolling back if anything goes wrong.
    """
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if query.strip().upper().startswith(('SELECT', 'SHOW')):
            columns = [desc[0] for desc in cursor.description]
            result = pd.DataFrame(cursor.fetchall(), columns=columns)
        else:
            conn.commit()
            result = pd.DataFrame([{"status": "Success", "rows_affected": cursor.rowcount}])

        cursor.close()
        return result
    except Exception as e:
        st.error(f"Error executing PostgreSQL query: {e}")
        conn.rollback()
        return pd.DataFrame([{"status": "Error", "message": str(e)}])

def transfer_data_to_postgres(table_name, conn):
    """
    Moves your generated data from DuckDB to a PostgreSQL database.

    This is perfect when you want to take your test data to the next level.
    We'll automatically create the table in PostgreSQL if it doesn't exist,
    and handle all the data conversion and bulk insertion for you. It's the
    easiest way to get your generated data into a production-grade database
    system.
    """
    try:
        # Get data from DuckDB
        data = execute_duckdb_query(f"SELECT * FROM {table_name}")
        if data.empty:
            st.warning(f"No data found in table {table_name}")
            return False

        # Create table in PostgreSQL if it doesn't exist
        columns = ", ".join([f"{col} TEXT" for col in data.columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        execute_postgres_query(conn, create_table_query)

        # Insert data into PostgreSQL
        cursor = conn.cursor()

        # Convert DataFrame to list of tuples
        values = [tuple(row) for row in data.values]

        # Generate the INSERT query
        columns_str = ", ".join(data.columns)
        insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES %s"

        # Execute the query with execute_values for better performance
        execute_values(cursor, insert_query, values)
        conn.commit()

        st.success(f"Successfully transferred {len(data)} rows to PostgreSQL table {table_name}")
        return True
    except Exception as e:
        st.error(f"Error transferring data to PostgreSQL: {e}")
        if conn:
            conn.rollback()
        return False

def export_to_csv(table_name):
    """
    Exports data from DuckDB to a CSV file.

    Args:
        table_name (str): The name of the table to export.

    Returns:
        str: The path to the exported CSV file, or None if the export failed.
    """
    try:
        # Get data from DuckDB
        data = execute_duckdb_query(f"SELECT * FROM {table_name}")
        if data.empty:
            st.warning(f"No data found in table {table_name}")
            return None

        # Create exports directory if it doesn't exist
        os.makedirs("exports", exist_ok=True)

        # Export to CSV
        csv_path = f"exports/{table_name}.csv"
        data.to_csv(csv_path, index=False)

        st.success(f"Successfully exported {len(data)} rows to {csv_path}")
        return csv_path
    except Exception as e:
        st.error(f"Error exporting to CSV: {e}")
        return None

def database_view():
    """
    Renders the database operations view in the Streamlit application.
    """
    st.header("Database Operations")

    # Create tabs for different database operations
    tab1, tab2, tab3 = st.tabs(["DuckDB Operations", "PostgreSQL Operations", "Data Transfer"])

    with tab1:
        st.subheader("DuckDB Operations")

        # Show available tables
        st.markdown("### Available Tables")
        tables = execute_duckdb_query("SHOW TABLES")
        if not tables.empty:
            st.dataframe(tables)
        else:
            st.info("No tables found in DuckDB. Generate some data first.")

        # Query DuckDB
        st.markdown("### Query DuckDB")
        duckdb_query = st.text_area("Enter SQL query for DuckDB:", height=100)
        if st.button("Execute DuckDB Query"):
            if duckdb_query:
                result = execute_duckdb_query(duckdb_query)
                st.dataframe(result)
            else:
                st.warning("Please enter a query.")

    with tab2:
        st.subheader("PostgreSQL Operations")

        # PostgreSQL connection parameters
        st.markdown("### PostgreSQL Connection")
        pg_host = st.text_input("Host:", "localhost")
        pg_port = st.text_input("Port:", "5432")
        pg_dbname = st.text_input("Database:", "postgres")
        pg_user = st.text_input("Username:", "postgres")
        pg_password = st.text_input("Password:", type="password")

        # Test connection
        if st.button("Test Connection"):
            conn = get_postgres_connection(pg_host, pg_port, pg_dbname, pg_user, pg_password)
            if conn:
                st.success("Connection successful!")
                conn.close()

        # Query PostgreSQL
        st.markdown("### Query PostgreSQL")
        pg_query = st.text_area("Enter SQL query for PostgreSQL:", height=100)
        if st.button("Execute PostgreSQL Query"):
            if pg_query:
                conn = get_postgres_connection(pg_host, pg_port, pg_dbname, pg_user, pg_password)
                if conn:
                    result = execute_postgres_query(conn, pg_query)
                    st.dataframe(result)
                    conn.close()
            else:
                st.warning("Please enter a query.")

    with tab3:
        st.subheader("Data Transfer")

        # Show available tables for transfer
        st.markdown("### Transfer Data from DuckDB to PostgreSQL")
        tables = execute_duckdb_query("SHOW TABLES")
        if not tables.empty:
            table_names = tables.iloc[:, 0].tolist()
            selected_table = st.selectbox("Select table to transfer:", table_names)

            # Transfer options
            transfer_method = st.radio("Transfer method:", ["Direct Transfer", "Export to CSV"])

            if transfer_method == "Direct Transfer":
                # PostgreSQL connection parameters
                st.markdown("### PostgreSQL Connection")
                pg_host = st.text_input("Host:", "localhost", key="transfer_host")
                pg_port = st.text_input("Port:", "5432", key="transfer_port")
                pg_dbname = st.text_input("Database:", "postgres", key="transfer_dbname")
                pg_user = st.text_input("Username:", "postgres", key="transfer_user")
                pg_password = st.text_input("Password:", type="password", key="transfer_password")

                if st.button("Transfer Data"):
                    conn = get_postgres_connection(pg_host, pg_port, pg_dbname, pg_user, pg_password)
                    if conn:
                        transfer_data_to_postgres(selected_table, conn)
                        conn.close()
            else:
                if st.button("Export to CSV"):
                    csv_path = export_to_csv(selected_table)
                    if csv_path:
                        # Create a download button for the CSV file
                        with open(csv_path, "r") as f:
                            st.download_button(
                                label="Download CSV",
                                data=f,
                                file_name=f"{selected_table}.csv",
                                mime="text/csv"
                            )
        else:
            st.info("No tables found in DuckDB. Generate some data first.")
