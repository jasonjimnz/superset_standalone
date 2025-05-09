"""
Customers View

Our customer data generator page. Here you can create realistic customer profiles
with names, contact details, addresses and more - perfect for testing your CRM or
e-commerce applications without using real customer data.
"""

import streamlit as st
import pandas as pd
import duckdb
from faker import Faker
import random
from datetime import datetime, timedelta
from .database import execute_duckdb_query

# Initialize Faker
fake = Faker()

def generate_customers(num_records, include_fields):
    """
    Creates a batch of fake customer records based on selected fields.

    Takes the number of records you want and a list of fields to include,
    then works its magic with Faker to create realistic-looking customer data.
    Returns everything in a nice pandas DataFrame ready for preview or export.
    """
    customers = []

    for _ in range(num_records):
        customer = {}

        # Basic information
        if "customer_id" in include_fields:
            customer["customer_id"] = fake.uuid4()
        if "first_name" in include_fields:
            customer["first_name"] = fake.first_name()
        if "last_name" in include_fields:
            customer["last_name"] = fake.last_name()
        if "email" in include_fields:
            customer["email"] = fake.email()
        if "phone_number" in include_fields:
            customer["phone_number"] = fake.phone_number()

        # Address information
        if "street_address" in include_fields:
            customer["street_address"] = fake.street_address()
        if "city" in include_fields:
            customer["city"] = fake.city()
        if "state" in include_fields:
            customer["state"] = fake.state()
        if "zipcode" in include_fields:
            customer["zipcode"] = fake.zipcode()
        if "country" in include_fields:
            customer["country"] = fake.country()

        # Additional information
        if "date_of_birth" in include_fields:
            customer["date_of_birth"] = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d")
        if "registration_date" in include_fields:
            customer["registration_date"] = fake.date_time_between(start_date="-5y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
        if "last_login" in include_fields:
            customer["last_login"] = fake.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
        if "gender" in include_fields:
            customer["gender"] = random.choice(["Male", "Female", "Other", "Prefer not to say"])
        if "credit_card" in include_fields:
            customer["credit_card"] = fake.credit_card_number()
        if "credit_card_provider" in include_fields:
            customer["credit_card_provider"] = fake.credit_card_provider()
        if "credit_card_expiry" in include_fields:
            customer["credit_card_expiry"] = fake.credit_card_expire()
        if "user_agent" in include_fields:
            customer["user_agent"] = fake.user_agent()
        if "ip_address" in include_fields:
            customer["ip_address"] = fake.ipv4()
        if "job_title" in include_fields:
            customer["job_title"] = fake.job()
        if "company" in include_fields:
            customer["company"] = fake.company()
        if "ssn" in include_fields:
            customer["ssn"] = fake.ssn()
        if "preferred_language" in include_fields:
            customer["preferred_language"] = fake.language_name()
        if "account_status" in include_fields:
            customer["account_status"] = random.choice(["Active", "Inactive", "Suspended", "Pending"])
        if "loyalty_points" in include_fields:
            customer["loyalty_points"] = random.randint(0, 10000)
        if "customer_segment" in include_fields:
            customer["customer_segment"] = random.choice(["New", "Regular", "VIP", "Inactive"])

        customers.append(customer)

    return pd.DataFrame(customers)

def save_customers_to_duckdb(df, table_name="customers"):
    """
    Stores your freshly generated customer data in our DuckDB database.

    Takes your DataFrame of customer records and saves it to a table with the name
    you specify (or just uses "customers" if you don't provide a name).

    Let's you know if everything went smoothly or if something went wrong.
    """
    try:
        # Create the table if it doesn't exist
        conn = duckdb.connect("datasets.duckdb")

        # Convert DataFrame to DuckDB table
        conn.register("temp_df", df)
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM temp_df")

        conn.close()
        return True
    except Exception as e:
        st.error(f"Error saving to DuckDB: {e}")
        return False

def customers_view():
    """
    Sets up our customer data generation page with all the UI controls and options.
    This is where the magic happens for creating those perfect test customer profiles!
    """
    st.header("Customer Data Generator")

    st.markdown("""
    Generate realistic customer data using Faker. Select the fields you want to include
    and the number of records to generate.
    """)

    # Number of records to generate
    num_records = st.number_input("Number of records to generate:", min_value=1, max_value=100000, value=100)

    # Fields to include
    st.subheader("Fields to Include")

    # Organize fields into categories for better UI
    with st.expander("Basic Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            include_customer_id = st.checkbox("Customer ID", value=True)
            include_first_name = st.checkbox("First Name", value=True)
            include_last_name = st.checkbox("Last Name", value=True)
        with col2:
            include_email = st.checkbox("Email", value=True)
            include_phone_number = st.checkbox("Phone Number", value=True)

    with st.expander("Address Information"):
        col1, col2 = st.columns(2)
        with col1:
            include_street_address = st.checkbox("Street Address")
            include_city = st.checkbox("City")
            include_state = st.checkbox("State/Province")
        with col2:
            include_zipcode = st.checkbox("Zipcode/Postal Code")
            include_country = st.checkbox("Country")

    with st.expander("Additional Information"):
        col1, col2, col3 = st.columns(3)
        with col1:
            include_dob = st.checkbox("Date of Birth")
            include_registration_date = st.checkbox("Registration Date")
            include_last_login = st.checkbox("Last Login")
            include_gender = st.checkbox("Gender")
            include_credit_card = st.checkbox("Credit Card Number")
            include_credit_card_provider = st.checkbox("Credit Card Provider")
        with col2:
            include_credit_card_expiry = st.checkbox("Credit Card Expiry")
            include_user_agent = st.checkbox("User Agent")
            include_ip_address = st.checkbox("IP Address")
            include_job_title = st.checkbox("Job Title")
            include_company = st.checkbox("Company")
            include_ssn = st.checkbox("SSN")
        with col3:
            include_preferred_language = st.checkbox("Preferred Language")
            include_account_status = st.checkbox("Account Status")
            include_loyalty_points = st.checkbox("Loyalty Points")
            include_customer_segment = st.checkbox("Customer Segment")

    # Collect all selected fields
    include_fields = []
    if include_customer_id:
        include_fields.append("customer_id")
    if include_first_name:
        include_fields.append("first_name")
    if include_last_name:
        include_fields.append("last_name")
    if include_email:
        include_fields.append("email")
    if include_phone_number:
        include_fields.append("phone_number")
    if include_street_address:
        include_fields.append("street_address")
    if include_city:
        include_fields.append("city")
    if include_state:
        include_fields.append("state")
    if include_zipcode:
        include_fields.append("zipcode")
    if include_country:
        include_fields.append("country")
    if include_dob:
        include_fields.append("date_of_birth")
    if include_registration_date:
        include_fields.append("registration_date")
    if include_last_login:
        include_fields.append("last_login")
    if include_gender:
        include_fields.append("gender")
    if include_credit_card:
        include_fields.append("credit_card")
    if include_credit_card_provider:
        include_fields.append("credit_card_provider")
    if include_credit_card_expiry:
        include_fields.append("credit_card_expiry")
    if include_user_agent:
        include_fields.append("user_agent")
    if include_ip_address:
        include_fields.append("ip_address")
    if include_job_title:
        include_fields.append("job_title")
    if include_company:
        include_fields.append("company")
    if include_ssn:
        include_fields.append("ssn")
    if include_preferred_language:
        include_fields.append("preferred_language")
    if include_account_status:
        include_fields.append("account_status")
    if include_loyalty_points:
        include_fields.append("loyalty_points")
    if include_customer_segment:
        include_fields.append("customer_segment")

    # Table name
    table_name = st.text_input("Table name:", "customers")

    # Generate button
    if st.button("Generate Customer Data"):
        if not include_fields:
            st.warning("Please select at least one field to include.")
        else:
            with st.spinner("Generating customer data..."):
                # Generate data
                df = generate_customers(num_records, include_fields)

                # Display preview
                st.subheader("Preview")
                st.dataframe(df.head(10))

                # Save to DuckDB
                if save_customers_to_duckdb(df, table_name):
                    st.success(f"Successfully generated {num_records} customer records and saved to table '{table_name}'.")

                    # Show SQL query to retrieve data
                    st.subheader("SQL Query")
                    st.code(f"SELECT * FROM {table_name};")

                    # Option to view all data
                    if st.button("View All Data"):
                        result = execute_duckdb_query(f"SELECT * FROM {table_name}")
                        st.dataframe(result)
