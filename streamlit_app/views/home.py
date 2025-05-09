"""
Homepage View

The welcome page of our Dataset Generator app. This is where users get their first
impression of what our tool can do and how to use it.
"""

import streamlit as st

def home_view():
    """
    Creates our welcoming homepage with feature highlights and getting started info.
    """
    st.header("Welcome to the Dataset Generator")

    st.markdown("""
    ## About This Application

    The Dataset Generator is a powerful tool designed to help you create realistic test data for your applications, 
    databases, and data analysis projects. Using the Faker library, it generates high-quality, 
    realistic data across multiple domains.

    ## Key Features

    ### Data Generation
    - **Customers**: Generate customer profiles with names, contact information, addresses, and more
    - **Products**: Create product catalogs with names, descriptions, prices, and categories
    - **Companies**: Generate company data including names, addresses, and industry information
    - **Transactions**: Create realistic transaction records with dates, amounts, and references
    - **Custom Datasets**: Design your own data schema and generate custom datasets

    ### Database Operations
    - Store generated data in a local DuckDB database
    - Export data to other database systems
    - Run SQL queries on your generated data

    ## Getting Started

    1. Use the navigation menu on the left to select the type of data you want to generate
    2. Configure the data generation options (number of records, fields to include, etc.)
    3. Generate the data and view the results
    4. Use the database operations to manage your generated datasets

    ## Use Cases

    - Developing and testing applications without using real customer data
    - Creating demo datasets for presentations and training
    - Populating test databases for performance testing
    - Generating sample data for data analysis and visualization projects
    """)

    # Add some visual elements
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("**Customers Data**\n\nGenerate realistic customer profiles with customizable fields")

    with col2:
        st.info("**Products Data**\n\nCreate product catalogs with names, prices, and categories")

    with col3:
        st.info("**Custom Datasets**\n\nDesign your own data schema and generate custom data")
