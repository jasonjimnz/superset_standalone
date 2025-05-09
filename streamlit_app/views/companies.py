"""
Companies View

Our business data generator - create realistic company profiles complete with 
industry classifications, financial details, and contact information. Great for 
B2B application testing, CRM demos, or when you need a directory of fictional 
but believable organizations.
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

def generate_companies(num_records, include_fields):
    """
    Creates a realistic business directory with companies of all types and sizes.

    We've built in lots of smart relationships - startups have fewer employees than
    enterprises, company size affects revenue ranges, and registration dates always
    come after founding dates. The result is a dataset that feels like it could be
    a real business directory, not just random data.
    """
    companies = []

    # Define company types
    company_types = ["Corporation", "LLC", "Partnership", "Sole Proprietorship", "Non-Profit", "Public Company"]

    # Define industry sectors
    industry_sectors = [
        "Technology", "Healthcare", "Finance", "Retail", "Manufacturing", "Energy",
        "Education", "Entertainment", "Transportation", "Agriculture", "Construction",
        "Hospitality", "Real Estate", "Telecommunications", "Media", "Consulting"
    ]

    # Define company sizes
    company_sizes = ["Startup", "Small", "Medium", "Large", "Enterprise"]

    # Define company statuses
    company_statuses = ["Active", "Inactive", "Bankrupt", "Acquired", "Merged", "IPO"]

    for _ in range(num_records):
        company = {}

        # Basic information
        if "company_id" in include_fields:
            company["company_id"] = fake.uuid4()
        if "company_name" in include_fields:
            company["company_name"] = fake.company()
        if "legal_name" in include_fields:
            company["legal_name"] = fake.company() + " " + random.choice(["Inc.", "LLC", "Corp.", "Ltd.", "Group"])
        if "description" in include_fields:
            company["description"] = fake.catch_phrase() + ". " + fake.bs()
        if "slogan" in include_fields:
            company["slogan"] = fake.catch_phrase()
        if "company_type" in include_fields:
            company["company_type"] = random.choice(company_types)
        if "industry" in include_fields:
            company["industry"] = random.choice(industry_sectors)
        if "company_size" in include_fields:
            company["company_size"] = random.choice(company_sizes)
        if "employees" in include_fields:
            # Generate employee count based on company size
            if "company_size" in include_fields:
                if company["company_size"] == "Startup":
                    company["employees"] = random.randint(1, 50)
                elif company["company_size"] == "Small":
                    company["employees"] = random.randint(51, 200)
                elif company["company_size"] == "Medium":
                    company["employees"] = random.randint(201, 1000)
                elif company["company_size"] == "Large":
                    company["employees"] = random.randint(1001, 10000)
                else:  # Enterprise
                    company["employees"] = random.randint(10001, 100000)
            else:
                company["employees"] = random.randint(1, 100000)

        # Contact information
        if "email" in include_fields:
            company["email"] = "contact@" + fake.domain_name()
        if "phone" in include_fields:
            company["phone"] = fake.phone_number()
        if "website" in include_fields:
            company["website"] = "https://www." + fake.domain_name()
        if "fax" in include_fields:
            company["fax"] = fake.phone_number()

        # Address information
        if "street_address" in include_fields:
            company["street_address"] = fake.street_address()
        if "city" in include_fields:
            company["city"] = fake.city()
        if "state" in include_fields:
            company["state"] = fake.state()
        if "zipcode" in include_fields:
            company["zipcode"] = fake.zipcode()
        if "country" in include_fields:
            company["country"] = fake.country()
        if "latitude" in include_fields:
            company["latitude"] = str(fake.latitude())
        if "longitude" in include_fields:
            company["longitude"] = str(fake.longitude())

        # Financial information
        if "revenue" in include_fields:
            # Generate revenue based on company size
            if "company_size" in include_fields:
                if company["company_size"] == "Startup":
                    company["revenue"] = round(random.uniform(0, 1000000), 2)
                elif company["company_size"] == "Small":
                    company["revenue"] = round(random.uniform(1000000, 10000000), 2)
                elif company["company_size"] == "Medium":
                    company["revenue"] = round(random.uniform(10000000, 100000000), 2)
                elif company["company_size"] == "Large":
                    company["revenue"] = round(random.uniform(100000000, 1000000000), 2)
                else:  # Enterprise
                    company["revenue"] = round(random.uniform(1000000000, 10000000000), 2)
            else:
                company["revenue"] = round(random.uniform(0, 10000000000), 2)
        if "currency" in include_fields:
            company["currency"] = random.choice(["USD", "EUR", "GBP", "CAD", "AUD", "JPY"])
        if "tax_id" in include_fields:
            company["tax_id"] = fake.bothify(text="??-#######")
        if "duns_number" in include_fields:
            company["duns_number"] = fake.bothify(text="###-###-###")
        if "stock_symbol" in include_fields:
            company["stock_symbol"] = fake.lexify(text="????").upper()
        if "stock_exchange" in include_fields:
            company["stock_exchange"] = random.choice(["NYSE", "NASDAQ", "LSE", "TSX", "JPX", "SSE"])

        # Additional information
        if "founded_date" in include_fields:
            company["founded_date"] = fake.date_between(start_date="-50y", end_date="-1y").strftime("%Y-%m-%d")
        if "registration_date" in include_fields:
            if "founded_date" in include_fields:
                founded_date = datetime.strptime(company["founded_date"], "%Y-%m-%d")
                registration_date = fake.date_between(start_date=founded_date, end_date=founded_date + timedelta(days=365))
                company["registration_date"] = registration_date.strftime("%Y-%m-%d")
            else:
                company["registration_date"] = fake.date_between(start_date="-50y", end_date="-1y").strftime("%Y-%m-%d")
        if "status" in include_fields:
            company["status"] = random.choice(company_statuses)
        if "logo_url" in include_fields:
            company["logo_url"] = f"https://example.com/logos/{fake.uuid4()}.png"
        if "parent_company" in include_fields:
            # 30% chance of having a parent company
            if random.random() < 0.3:
                company["parent_company"] = fake.company()
            else:
                company["parent_company"] = None
        if "ceo" in include_fields:
            company["ceo"] = fake.name()
        if "social_media" in include_fields:
            company["social_media"] = {
                "facebook": f"https://facebook.com/{fake.user_name()}",
                "twitter": f"https://twitter.com/{fake.user_name()}",
                "linkedin": f"https://linkedin.com/company/{fake.user_name()}"
            }

        companies.append(company)

    return pd.DataFrame(companies)

def save_companies_to_duckdb(df, table_name="companies"):
    """
    Archives your business directory into our DuckDB database for safekeeping.

    Takes your newly created company dataset and saves it to DuckDB with your
    chosen table name (or just uses "companies" if you don't specify one).
    This makes it easy to run SQL queries on your data or export it later.
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

def companies_view():
    """
    Creates our company data generation interface with all its options and controls.

    This is where you can build your own business directory by selecting exactly
    which company details to include - from basic info to financial data to social media.
    """
    st.header("Company Data Generator")

    st.markdown("""
    Generate realistic company data using Faker. Select the fields you want to include
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
            include_company_id = st.checkbox("Company ID", value=True)
            include_company_name = st.checkbox("Company Name", value=True)
            include_legal_name = st.checkbox("Legal Name")
            include_description = st.checkbox("Description", value=True)
        with col2:
            include_slogan = st.checkbox("Slogan")
            include_company_type = st.checkbox("Company Type", value=True)
            include_industry = st.checkbox("Industry", value=True)
            include_company_size = st.checkbox("Company Size")
            include_employees = st.checkbox("Number of Employees")

    with st.expander("Contact Information"):
        col1, col2 = st.columns(2)
        with col1:
            include_email = st.checkbox("Email", value=True)
            include_phone = st.checkbox("Phone", value=True)
        with col2:
            include_website = st.checkbox("Website")
            include_fax = st.checkbox("Fax")

    with st.expander("Address Information"):
        col1, col2 = st.columns(2)
        with col1:
            include_street_address = st.checkbox("Street Address")
            include_city = st.checkbox("City")
            include_state = st.checkbox("State/Province")
        with col2:
            include_zipcode = st.checkbox("Zipcode/Postal Code")
            include_country = st.checkbox("Country")
            include_latitude = st.checkbox("Latitude")
            include_longitude = st.checkbox("Longitude")

    with st.expander("Financial Information"):
        col1, col2 = st.columns(2)
        with col1:
            include_revenue = st.checkbox("Revenue")
            include_currency = st.checkbox("Currency")
            include_tax_id = st.checkbox("Tax ID")
        with col2:
            include_duns_number = st.checkbox("DUNS Number")
            include_stock_symbol = st.checkbox("Stock Symbol")
            include_stock_exchange = st.checkbox("Stock Exchange")

    with st.expander("Additional Information"):
        col1, col2, col3 = st.columns(3)
        with col1:
            include_founded_date = st.checkbox("Founded Date")
            include_registration_date = st.checkbox("Registration Date")
            include_status = st.checkbox("Status")
        with col2:
            include_logo_url = st.checkbox("Logo URL")
            include_parent_company = st.checkbox("Parent Company")
            include_ceo = st.checkbox("CEO")
        with col3:
            include_social_media = st.checkbox("Social Media")

    # Collect all selected fields
    include_fields = []
    if include_company_id:
        include_fields.append("company_id")
    if include_company_name:
        include_fields.append("company_name")
    if include_legal_name:
        include_fields.append("legal_name")
    if include_description:
        include_fields.append("description")
    if include_slogan:
        include_fields.append("slogan")
    if include_company_type:
        include_fields.append("company_type")
    if include_industry:
        include_fields.append("industry")
    if include_company_size:
        include_fields.append("company_size")
    if include_employees:
        include_fields.append("employees")
    if include_email:
        include_fields.append("email")
    if include_phone:
        include_fields.append("phone")
    if include_website:
        include_fields.append("website")
    if include_fax:
        include_fields.append("fax")
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
    if include_latitude:
        include_fields.append("latitude")
    if include_longitude:
        include_fields.append("longitude")
    if include_revenue:
        include_fields.append("revenue")
    if include_currency:
        include_fields.append("currency")
    if include_tax_id:
        include_fields.append("tax_id")
    if include_duns_number:
        include_fields.append("duns_number")
    if include_stock_symbol:
        include_fields.append("stock_symbol")
    if include_stock_exchange:
        include_fields.append("stock_exchange")
    if include_founded_date:
        include_fields.append("founded_date")
    if include_registration_date:
        include_fields.append("registration_date")
    if include_status:
        include_fields.append("status")
    if include_logo_url:
        include_fields.append("logo_url")
    if include_parent_company:
        include_fields.append("parent_company")
    if include_ceo:
        include_fields.append("ceo")
    if include_social_media:
        include_fields.append("social_media")

    # Table name
    table_name = st.text_input("Table name:", "companies")

    # Generate button
    if st.button("Generate Company Data"):
        if not include_fields:
            st.warning("Please select at least one field to include.")
        else:
            with st.spinner("Generating company data..."):
                # Generate data
                df = generate_companies(num_records, include_fields)

                # Display preview
                st.subheader("Preview")
                st.dataframe(df.head(10))

                # Save to DuckDB
                if save_companies_to_duckdb(df, table_name):
                    st.success(f"Successfully generated {num_records} company records and saved to table '{table_name}'.")

                    # Show SQL query to retrieve data
                    st.subheader("SQL Query")
                    st.code(f"SELECT * FROM {table_name};")

                    # Option to view all data
                    if st.button("View All Data"):
                        result = execute_duckdb_query(f"SELECT * FROM {table_name}")
                        st.dataframe(result)
