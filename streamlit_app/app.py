"""
Dataset Generator App

Our Streamlit app for creating realistic test data with Faker. Generate customer profiles,
product catalogs, company information, and transaction records with just a few clicks.

Store your generated datasets in DuckDB locally or export them to PostgreSQL
for more advanced database operations.
"""

import streamlit as st
from views.home import home_view
from views.customers import customers_view
from views.products import products_view
from views.companies import companies_view
from views.transactions import transactions_view
from views.custom import custom_view
from views.database import database_view

# Set page configuration
st.set_page_config(
    page_title="Dataset Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application title
st.title("Dataset Generator")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["Home", "Customers", "Products", "Companies", "Transactions", "Custom Dataset", "Database Operations"],
    index=0  # Set Home as the default selected option
)

# Display the selected page
if page == "Home":
    home_view()
elif page == "Customers":
    customers_view()
elif page == "Products":
    products_view()
elif page == "Companies":
    companies_view()
elif page == "Transactions":
    transactions_view()
elif page == "Custom Dataset":
    custom_view()
elif page == "Database Operations":
    database_view()

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Dataset Generator v1.0")
