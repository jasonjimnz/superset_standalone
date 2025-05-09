"""
Transactions View

The heart of our financial data generator - create realistic purchase records, 
payment histories, and order details. What makes this really special is how it can 
connect to your existing customer, product, and company datasets to create a fully 
integrated data ecosystem that feels like real business activity.
"""

import streamlit as st
import pandas as pd
import duckdb
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid
from .database import execute_duckdb_query

# Initialize Faker
fake = Faker()

def get_reference_data(table_name, id_column):
    """
    Pulls IDs from your existing tables to connect transactions to real entities.

    This is what makes our transactions feel real - instead of making up random
    customer IDs, we can link to actual customers you've already generated.
    It's like creating a mini relational database right in your test data!
    """
    try:
        # Check if the table exists
        tables = execute_duckdb_query("SHOW TABLES")
        if tables.empty or table_name not in tables.iloc[:, 0].tolist():
            return None

        # Get the IDs from the table
        result = execute_duckdb_query(f"SELECT {id_column} FROM {table_name}")
        if result.empty:
            return None

        return result[id_column].tolist()
    except Exception as e:
        st.error(f"Error getting reference data: {e}")
        return None

def generate_transactions(num_records, include_fields, reference_tables=None):
    """
    Creates a complete transaction history with all the financial details you need.

    This is our most sophisticated generator - it handles everything from basic
    purchase records to complex calculations like taxes and discounts. It even
    makes sure delivery dates come after transaction dates, and gift messages
    only appear for items marked as gifts.

    The real magic happens when you connect it to your customer, product, and
    company tables - suddenly you have a complete business data ecosystem!
    """
    transactions = []

    # Define payment methods
    payment_methods = [
        "Credit Card", "Debit Card", "PayPal", "Bank Transfer", "Cash",
        "Check", "Cryptocurrency", "Gift Card", "Store Credit", "Mobile Payment"
    ]

    # Define transaction types
    transaction_types = [
        "Purchase", "Refund", "Exchange", "Subscription", "Renewal",
        "Cancellation", "Upgrade", "Downgrade", "Chargeback", "Adjustment"
    ]

    # Define transaction statuses
    transaction_statuses = [
        "Completed", "Pending", "Failed", "Cancelled", "Refunded",
        "Partially Refunded", "Disputed", "Processing", "On Hold", "Authorized"
    ]

    # Define shipping methods
    shipping_methods = [
        "Standard", "Express", "Next Day", "Two-Day", "International",
        "Local Pickup", "Digital Delivery", "Freight", "Same Day", "Economy"
    ]

    # Get reference data if provided
    customer_ids = None
    product_ids = None
    company_ids = None

    if reference_tables:
        if "customers" in reference_tables:
            customer_ids = get_reference_data(reference_tables["customers"], "customer_id")
        if "products" in reference_tables:
            product_ids = get_reference_data(reference_tables["products"], "product_id")
        if "companies" in reference_tables:
            company_ids = get_reference_data(reference_tables["companies"], "company_id")

    for _ in range(num_records):
        transaction = {}

        # Basic information
        if "transaction_id" in include_fields:
            transaction["transaction_id"] = fake.uuid4()
        if "order_id" in include_fields:
            transaction["order_id"] = fake.bothify(text="ORD-######")
        if "invoice_id" in include_fields:
            transaction["invoice_id"] = fake.bothify(text="INV-######")

        # Customer information
        if "customer_id" in include_fields:
            if customer_ids:
                transaction["customer_id"] = random.choice(customer_ids)
            else:
                transaction["customer_id"] = fake.uuid4()

        # Product information
        if "product_id" in include_fields:
            if product_ids:
                transaction["product_id"] = random.choice(product_ids)
            else:
                transaction["product_id"] = fake.uuid4()

        # Company information
        if "company_id" in include_fields:
            if company_ids:
                transaction["company_id"] = random.choice(company_ids)
            else:
                transaction["company_id"] = fake.uuid4()

        # Transaction details
        if "transaction_date" in include_fields:
            transaction["transaction_date"] = fake.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
        if "transaction_type" in include_fields:
            transaction["transaction_type"] = random.choice(transaction_types)
        if "transaction_status" in include_fields:
            transaction["transaction_status"] = random.choice(transaction_statuses)

        # Financial information
        if "amount" in include_fields:
            transaction["amount"] = round(random.uniform(1, 1000), 2)
        if "tax" in include_fields:
            if "amount" in include_fields:
                transaction["tax"] = round(transaction["amount"] * random.uniform(0.05, 0.25), 2)
            else:
                transaction["tax"] = round(random.uniform(0.1, 100), 2)
        if "shipping_cost" in include_fields:
            transaction["shipping_cost"] = round(random.uniform(0, 50), 2)
        if "discount" in include_fields:
            if "amount" in include_fields:
                transaction["discount"] = round(transaction["amount"] * random.uniform(0, 0.3), 2)
            else:
                transaction["discount"] = round(random.uniform(0, 100), 2)
        if "total" in include_fields:
            # Calculate total based on amount, tax, shipping, and discount if they exist
            total = 0
            if "amount" in include_fields:
                total += transaction["amount"]
            if "tax" in include_fields:
                total += transaction["tax"]
            if "shipping_cost" in include_fields:
                total += transaction["shipping_cost"]
            if "discount" in include_fields:
                total -= transaction["discount"]
            transaction["total"] = round(max(0, total), 2)
        if "currency" in include_fields:
            transaction["currency"] = random.choice(["USD", "EUR", "GBP", "CAD", "AUD", "JPY"])

        # Payment information
        if "payment_method" in include_fields:
            transaction["payment_method"] = random.choice(payment_methods)
        if "payment_status" in include_fields:
            transaction["payment_status"] = random.choice(["Paid", "Pending", "Failed", "Refunded", "Partially Refunded"])
        if "card_type" in include_fields:
            transaction["card_type"] = random.choice(["Visa", "Mastercard", "American Express", "Discover", "JCB"])
        if "card_last_four" in include_fields:
            transaction["card_last_four"] = fake.bothify(text="####")

        # Shipping information
        if "shipping_method" in include_fields:
            transaction["shipping_method"] = random.choice(shipping_methods)
        if "shipping_address" in include_fields:
            transaction["shipping_address"] = fake.street_address()
        if "shipping_city" in include_fields:
            transaction["shipping_city"] = fake.city()
        if "shipping_state" in include_fields:
            transaction["shipping_state"] = fake.state()
        if "shipping_zipcode" in include_fields:
            transaction["shipping_zipcode"] = fake.zipcode()
        if "shipping_country" in include_fields:
            transaction["shipping_country"] = fake.country()
        if "tracking_number" in include_fields:
            transaction["tracking_number"] = fake.bothify(text="TRK-############")
        if "estimated_delivery" in include_fields:
            if "transaction_date" in include_fields:
                transaction_date = datetime.strptime(transaction["transaction_date"], "%Y-%m-%d %H:%M:%S")
                delivery_date = transaction_date + timedelta(days=random.randint(1, 14))
                transaction["estimated_delivery"] = delivery_date.strftime("%Y-%m-%d")
            else:
                transaction["estimated_delivery"] = fake.date_between(start_date="today", end_date="+14d").strftime("%Y-%m-%d")

        # Additional information
        if "notes" in include_fields:
            transaction["notes"] = fake.text(max_nb_chars=100)
        if "is_gift" in include_fields:
            transaction["is_gift"] = random.choice([True, False])
        if "gift_message" in include_fields:
            if "is_gift" in include_fields and transaction["is_gift"]:
                transaction["gift_message"] = fake.text(max_nb_chars=50)
            else:
                transaction["gift_message"] = None
        if "source" in include_fields:
            transaction["source"] = random.choice(["Website", "Mobile App", "In-Store", "Phone", "Email", "Social Media"])
        if "ip_address" in include_fields:
            transaction["ip_address"] = fake.ipv4()
        if "user_agent" in include_fields:
            transaction["user_agent"] = fake.user_agent()
        if "coupon_code" in include_fields:
            # 30% chance of having a coupon code
            if random.random() < 0.3:
                transaction["coupon_code"] = fake.bothify(text="???###").upper()
            else:
                transaction["coupon_code"] = None

        transactions.append(transaction)

    return pd.DataFrame(transactions)

def save_transactions_to_duckdb(df, table_name="transactions"):
    """
    Stores your transaction history in our DuckDB database for analysis and export.

    Once your beautiful transaction data is generated, we'll save it to DuckDB
    where you can run SQL queries on it, join it with other tables, or export it
    to other systems. By default, we'll call the table "transactions" unless you
    specify a different name.
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

def transactions_view():
    """
    Powers our transaction generator interface with all its interconnected options.

    This is the crown jewel of our data generators - it brings together customers,
    products, and companies into a unified transaction system. The UI lets you
    build exactly the transaction dataset you need, from simple sales records to
    complex order histories with shipping details and payment information.
    """
    st.header("Transaction Data Generator")

    st.markdown("""
    Generate realistic transaction data using Faker. Select the fields you want to include
    and the number of records to generate. You can also reference existing customer, product,
    and company data if available.
    """)

    # Check for existing reference tables
    tables = execute_duckdb_query("SHOW TABLES")
    available_tables = tables.iloc[:, 0].tolist() if not tables.empty else []

    # Reference tables
    st.subheader("Reference Tables")
    st.markdown("""
    If you have already generated customer, product, or company data, you can reference those tables
    to create more realistic transaction data. Otherwise, random IDs will be generated.
    """)

    reference_tables = {}

    col1, col2, col3 = st.columns(3)

    with col1:
        if "customers" in available_tables:
            use_customers = st.checkbox("Reference Customers Table", value=True)
            if use_customers:
                customer_table = st.selectbox("Select Customers Table", [t for t in available_tables if "customer" in t.lower()], index=0)
                reference_tables["customers"] = customer_table
        else:
            st.info("No customer tables found. Generate customer data first to reference it.")

    with col2:
        if "products" in available_tables:
            use_products = st.checkbox("Reference Products Table", value=True)
            if use_products:
                product_table = st.selectbox("Select Products Table", [t for t in available_tables if "product" in t.lower()], index=0)
                reference_tables["products"] = product_table
        else:
            st.info("No product tables found. Generate product data first to reference it.")

    with col3:
        if "companies" in available_tables:
            use_companies = st.checkbox("Reference Companies Table", value=True)
            if use_companies:
                company_table = st.selectbox("Select Companies Table", [t for t in available_tables if "compan" in t.lower()], index=0)
                reference_tables["companies"] = company_table
        else:
            st.info("No company tables found. Generate company data first to reference it.")

    # Number of records to generate
    num_records = st.number_input("Number of records to generate:", min_value=1, max_value=100000, value=100)

    # Fields to include
    st.subheader("Fields to Include")

    # Organize fields into categories for better UI
    with st.expander("Basic Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            include_transaction_id = st.checkbox("Transaction ID", value=True)
            include_order_id = st.checkbox("Order ID", value=True)
        with col2:
            include_invoice_id = st.checkbox("Invoice ID")

    with st.expander("References", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            include_customer_id = st.checkbox("Customer ID", value=True)
        with col2:
            include_product_id = st.checkbox("Product ID", value=True)
        with col3:
            include_company_id = st.checkbox("Company ID")

    with st.expander("Transaction Details"):
        col1, col2 = st.columns(2)
        with col1:
            include_transaction_date = st.checkbox("Transaction Date", value=True)
            include_transaction_type = st.checkbox("Transaction Type", value=True)
        with col2:
            include_transaction_status = st.checkbox("Transaction Status", value=True)

    with st.expander("Financial Information"):
        col1, col2, col3 = st.columns(3)
        with col1:
            include_amount = st.checkbox("Amount", value=True)
            include_tax = st.checkbox("Tax")
            include_shipping_cost = st.checkbox("Shipping Cost")
        with col2:
            include_discount = st.checkbox("Discount")
            include_total = st.checkbox("Total", value=True)
            include_currency = st.checkbox("Currency")
        with col3:
            include_payment_method = st.checkbox("Payment Method", value=True)
            include_payment_status = st.checkbox("Payment Status")
            include_card_type = st.checkbox("Card Type")
            include_card_last_four = st.checkbox("Card Last Four")

    with st.expander("Shipping Information"):
        col1, col2, col3 = st.columns(3)
        with col1:
            include_shipping_method = st.checkbox("Shipping Method")
            include_shipping_address = st.checkbox("Shipping Address")
            include_shipping_city = st.checkbox("Shipping City")
        with col2:
            include_shipping_state = st.checkbox("Shipping State")
            include_shipping_zipcode = st.checkbox("Shipping Zipcode")
            include_shipping_country = st.checkbox("Shipping Country")
        with col3:
            include_tracking_number = st.checkbox("Tracking Number")
            include_estimated_delivery = st.checkbox("Estimated Delivery")

    with st.expander("Additional Information"):
        col1, col2, col3 = st.columns(3)
        with col1:
            include_notes = st.checkbox("Notes")
            include_is_gift = st.checkbox("Is Gift")
            include_gift_message = st.checkbox("Gift Message")
        with col2:
            include_source = st.checkbox("Source")
            include_ip_address = st.checkbox("IP Address")
            include_user_agent = st.checkbox("User Agent")
        with col3:
            include_coupon_code = st.checkbox("Coupon Code")

    # Collect all selected fields
    include_fields = []
    if include_transaction_id:
        include_fields.append("transaction_id")
    if include_order_id:
        include_fields.append("order_id")
    if include_invoice_id:
        include_fields.append("invoice_id")
    if include_customer_id:
        include_fields.append("customer_id")
    if include_product_id:
        include_fields.append("product_id")
    if include_company_id:
        include_fields.append("company_id")
    if include_transaction_date:
        include_fields.append("transaction_date")
    if include_transaction_type:
        include_fields.append("transaction_type")
    if include_transaction_status:
        include_fields.append("transaction_status")
    if include_amount:
        include_fields.append("amount")
    if include_tax:
        include_fields.append("tax")
    if include_shipping_cost:
        include_fields.append("shipping_cost")
    if include_discount:
        include_fields.append("discount")
    if include_total:
        include_fields.append("total")
    if include_currency:
        include_fields.append("currency")
    if include_payment_method:
        include_fields.append("payment_method")
    if include_payment_status:
        include_fields.append("payment_status")
    if include_card_type:
        include_fields.append("card_type")
    if include_card_last_four:
        include_fields.append("card_last_four")
    if include_shipping_method:
        include_fields.append("shipping_method")
    if include_shipping_address:
        include_fields.append("shipping_address")
    if include_shipping_city:
        include_fields.append("shipping_city")
    if include_shipping_state:
        include_fields.append("shipping_state")
    if include_shipping_zipcode:
        include_fields.append("shipping_zipcode")
    if include_shipping_country:
        include_fields.append("shipping_country")
    if include_tracking_number:
        include_fields.append("tracking_number")
    if include_estimated_delivery:
        include_fields.append("estimated_delivery")
    if include_notes:
        include_fields.append("notes")
    if include_is_gift:
        include_fields.append("is_gift")
    if include_gift_message:
        include_fields.append("gift_message")
    if include_source:
        include_fields.append("source")
    if include_ip_address:
        include_fields.append("ip_address")
    if include_user_agent:
        include_fields.append("user_agent")
    if include_coupon_code:
        include_fields.append("coupon_code")

    # Table name
    table_name = st.text_input("Table name:", "transactions")

    # Generate button
    if st.button("Generate Transaction Data"):
        if not include_fields:
            st.warning("Please select at least one field to include.")
        else:
            with st.spinner("Generating transaction data..."):
                # Generate data
                df = generate_transactions(num_records, include_fields, reference_tables)

                # Display preview
                st.subheader("Preview")
                st.dataframe(df.head(10))

                # Save to DuckDB
                if save_transactions_to_duckdb(df, table_name):
                    st.success(f"Successfully generated {num_records} transaction records and saved to table '{table_name}'.")

                    # Show SQL query to retrieve data
                    st.subheader("SQL Query")
                    st.code(f"SELECT * FROM {table_name};")

                    # Option to view all data
                    if st.button("View All Data"):
                        result = execute_duckdb_query(f"SELECT * FROM {table_name}")
                        st.dataframe(result)
