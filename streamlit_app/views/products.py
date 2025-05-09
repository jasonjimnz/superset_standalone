"""
Products View

Our product catalog generator - create realistic product listings with prices, 
categories, inventory details and more. Perfect for e-commerce testing, demo shops,
or when you need to populate a product database with believable items.
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

def generate_products(num_records, include_fields):
    """
    Creates a realistic product catalog with all the details you'd expect in an e-commerce system.

    Feed it the number of products you want and which fields to include, and it'll
    whip up a complete catalog with categories, prices, inventory levels and more.
    We've included lots of realistic touches like proper category-subcategory relationships
    and sensible pricing (costs lower than retail prices, for example).
    """
    products = []

    # Define categories for products
    categories = [
        "Electronics", "Clothing", "Home & Kitchen", "Books", "Toys & Games",
        "Sports & Outdoors", "Beauty & Personal Care", "Health & Household",
        "Automotive", "Office Products", "Pet Supplies", "Grocery", "Tools & Home Improvement"
    ]

    # Define conditions for products
    conditions = ["New", "Used - Like New", "Used - Good", "Used - Fair", "Refurbished"]

    # Define availability statuses
    availability = ["In Stock", "Out of Stock", "Pre-order", "Discontinued", "Limited Stock"]

    for _ in range(num_records):
        product = {}

        # Basic information
        if "product_id" in include_fields:
            product["product_id"] = fake.uuid4()
        if "product_name" in include_fields:
            product["product_name"] = fake.catch_phrase()
        if "description" in include_fields:
            product["description"] = fake.paragraph(nb_sentences=3)
        if "category" in include_fields:
            product["category"] = random.choice(categories)
        if "subcategory" in include_fields:
            # Generate a subcategory based on the category
            subcategories = {
                "Electronics": ["Smartphones", "Laptops", "Tablets", "Cameras", "Audio", "Wearables"],
                "Clothing": ["Men's", "Women's", "Children's", "Shoes", "Accessories", "Activewear"],
                "Home & Kitchen": ["Furniture", "Appliances", "Cookware", "Bedding", "Decor", "Storage"],
                "Books": ["Fiction", "Non-fiction", "Children's Books", "Textbooks", "Comics", "Magazines"],
                "Toys & Games": ["Board Games", "Puzzles", "Action Figures", "Dolls", "Educational", "Outdoor Play"],
                "Sports & Outdoors": ["Fitness", "Camping", "Cycling", "Team Sports", "Water Sports", "Winter Sports"],
                "Beauty & Personal Care": ["Skincare", "Haircare", "Makeup", "Fragrance", "Bath & Body", "Men's Grooming"],
                "Health & Household": ["Vitamins", "First Aid", "Household Supplies", "Personal Care", "Baby & Child Care"],
                "Automotive": ["Interior", "Exterior", "Tools & Equipment", "Parts & Accessories", "Electronics"],
                "Office Products": ["Writing Supplies", "Paper Products", "Office Furniture", "Office Electronics"],
                "Pet Supplies": ["Dog", "Cat", "Fish", "Bird", "Small Animal", "Reptile"],
                "Grocery": ["Beverages", "Snacks", "Canned Goods", "Baking", "Dairy", "Produce"],
                "Tools & Home Improvement": ["Power Tools", "Hand Tools", "Hardware", "Electrical", "Plumbing"]
            }

            if "category" in include_fields and product["category"] in subcategories:
                product["subcategory"] = random.choice(subcategories[product["category"]])
            else:
                # If no category is selected or category not in subcategories
                product["subcategory"] = random.choice(["Subcategory 1", "Subcategory 2", "Subcategory 3"])

        # Pricing information
        if "price" in include_fields:
            product["price"] = round(random.uniform(1.99, 999.99), 2)
        if "cost" in include_fields:
            # Cost is typically lower than price
            if "price" in include_fields:
                product["cost"] = round(product["price"] * random.uniform(0.4, 0.8), 2)
            else:
                product["cost"] = round(random.uniform(0.99, 799.99), 2)
        if "currency" in include_fields:
            product["currency"] = random.choice(["USD", "EUR", "GBP", "CAD", "AUD", "JPY"])
        if "discount_percentage" in include_fields:
            product["discount_percentage"] = round(random.uniform(0, 50), 2)
        if "tax_rate" in include_fields:
            product["tax_rate"] = round(random.uniform(0, 25), 2)

        # Inventory information
        if "sku" in include_fields:
            product["sku"] = fake.bothify(text="??-####-????").upper()
        if "barcode" in include_fields:
            product["barcode"] = fake.ean13()
        if "stock_quantity" in include_fields:
            product["stock_quantity"] = random.randint(0, 1000)
        if "availability" in include_fields:
            product["availability"] = random.choice(availability)
        if "condition" in include_fields:
            product["condition"] = random.choice(conditions)
        if "weight" in include_fields:
            product["weight"] = round(random.uniform(0.1, 50), 2)
        if "weight_unit" in include_fields:
            product["weight_unit"] = random.choice(["kg", "g", "lb", "oz"])
        if "dimensions" in include_fields:
            product["dimensions"] = f"{random.randint(1, 100)}x{random.randint(1, 100)}x{random.randint(1, 100)}"
        if "dimensions_unit" in include_fields:
            product["dimensions_unit"] = random.choice(["cm", "mm", "in"])

        # Supplier information
        if "supplier_id" in include_fields:
            product["supplier_id"] = fake.uuid4()
        if "supplier_name" in include_fields:
            product["supplier_name"] = fake.company()
        if "manufacturer" in include_fields:
            product["manufacturer"] = fake.company()
        if "country_of_origin" in include_fields:
            product["country_of_origin"] = fake.country()

        # Additional information
        if "created_date" in include_fields:
            product["created_date"] = fake.date_time_between(start_date="-2y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
        if "modified_date" in include_fields:
            if "created_date" in include_fields:
                created_date = datetime.strptime(product["created_date"], "%Y-%m-%d %H:%M:%S")
                modified_date = fake.date_time_between(start_date=created_date, end_date="now")
                product["modified_date"] = modified_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                product["modified_date"] = fake.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
        if "is_featured" in include_fields:
            product["is_featured"] = random.choice([True, False])
        if "is_active" in include_fields:
            product["is_active"] = random.choice([True, False])
        if "rating" in include_fields:
            product["rating"] = round(random.uniform(1, 5), 1)
        if "review_count" in include_fields:
            product["review_count"] = random.randint(0, 1000)
        if "tags" in include_fields:
            num_tags = random.randint(1, 5)
            product["tags"] = ", ".join([fake.word() for _ in range(num_tags)])
        if "image_url" in include_fields:
            product["image_url"] = f"https://example.com/images/products/{fake.uuid4()}.jpg"

        products.append(product)

    return pd.DataFrame(products)

def save_products_to_duckdb(df, table_name="products"):
    """
    Saves your shiny new product catalog to our DuckDB database.

    Takes your freshly generated product DataFrame and stores it in DuckDB under
    whatever name you choose (or just calls it "products" if you don't specify).
    This makes it available for querying, exporting, or connecting to other datasets.
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

def products_view():
    """
    Sets up our product generator page with all its bells and whistles.

    This is where users can create their dream product catalog by selecting
    exactly which fields they want and how many products they need.
    """
    st.header("Product Data Generator")

    st.markdown("""
    Generate realistic product data using Faker. Select the fields you want to include
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
            include_product_id = st.checkbox("Product ID", value=True)
            include_product_name = st.checkbox("Product Name", value=True)
            include_description = st.checkbox("Description", value=True)
        with col2:
            include_category = st.checkbox("Category", value=True)
            include_subcategory = st.checkbox("Subcategory")

    with st.expander("Pricing Information"):
        col1, col2 = st.columns(2)
        with col1:
            include_price = st.checkbox("Price", value=True)
            include_cost = st.checkbox("Cost")
            include_currency = st.checkbox("Currency")
        with col2:
            include_discount = st.checkbox("Discount Percentage")
            include_tax_rate = st.checkbox("Tax Rate")

    with st.expander("Inventory Information"):
        col1, col2, col3 = st.columns(3)
        with col1:
            include_sku = st.checkbox("SKU")
            include_barcode = st.checkbox("Barcode")
            include_stock = st.checkbox("Stock Quantity", value=True)
        with col2:
            include_availability = st.checkbox("Availability")
            include_condition = st.checkbox("Condition")
            include_weight = st.checkbox("Weight")
        with col3:
            include_weight_unit = st.checkbox("Weight Unit")
            include_dimensions = st.checkbox("Dimensions")
            include_dimensions_unit = st.checkbox("Dimensions Unit")

    with st.expander("Supplier Information"):
        col1, col2 = st.columns(2)
        with col1:
            include_supplier_id = st.checkbox("Supplier ID")
            include_supplier_name = st.checkbox("Supplier Name")
        with col2:
            include_manufacturer = st.checkbox("Manufacturer")
            include_country_of_origin = st.checkbox("Country of Origin")

    with st.expander("Additional Information"):
        col1, col2, col3 = st.columns(3)
        with col1:
            include_created_date = st.checkbox("Created Date")
            include_modified_date = st.checkbox("Modified Date")
            include_is_featured = st.checkbox("Is Featured")
        with col2:
            include_is_active = st.checkbox("Is Active")
            include_rating = st.checkbox("Rating")
            include_review_count = st.checkbox("Review Count")
        with col3:
            include_tags = st.checkbox("Tags")
            include_image_url = st.checkbox("Image URL")

    # Collect all selected fields
    include_fields = []
    if include_product_id:
        include_fields.append("product_id")
    if include_product_name:
        include_fields.append("product_name")
    if include_description:
        include_fields.append("description")
    if include_category:
        include_fields.append("category")
    if include_subcategory:
        include_fields.append("subcategory")
    if include_price:
        include_fields.append("price")
    if include_cost:
        include_fields.append("cost")
    if include_currency:
        include_fields.append("currency")
    if include_discount:
        include_fields.append("discount_percentage")
    if include_tax_rate:
        include_fields.append("tax_rate")
    if include_sku:
        include_fields.append("sku")
    if include_barcode:
        include_fields.append("barcode")
    if include_stock:
        include_fields.append("stock_quantity")
    if include_availability:
        include_fields.append("availability")
    if include_condition:
        include_fields.append("condition")
    if include_weight:
        include_fields.append("weight")
    if include_weight_unit:
        include_fields.append("weight_unit")
    if include_dimensions:
        include_fields.append("dimensions")
    if include_dimensions_unit:
        include_fields.append("dimensions_unit")
    if include_supplier_id:
        include_fields.append("supplier_id")
    if include_supplier_name:
        include_fields.append("supplier_name")
    if include_manufacturer:
        include_fields.append("manufacturer")
    if include_country_of_origin:
        include_fields.append("country_of_origin")
    if include_created_date:
        include_fields.append("created_date")
    if include_modified_date:
        include_fields.append("modified_date")
    if include_is_featured:
        include_fields.append("is_featured")
    if include_is_active:
        include_fields.append("is_active")
    if include_rating:
        include_fields.append("rating")
    if include_review_count:
        include_fields.append("review_count")
    if include_tags:
        include_fields.append("tags")
    if include_image_url:
        include_fields.append("image_url")

    # Table name
    table_name = st.text_input("Table name:", "products")

    # Generate button
    if st.button("Generate Product Data"):
        if not include_fields:
            st.warning("Please select at least one field to include.")
        else:
            with st.spinner("Generating product data..."):
                # Generate data
                df = generate_products(num_records, include_fields)

                # Display preview
                st.subheader("Preview")
                st.dataframe(df.head(10))

                # Save to DuckDB
                if save_products_to_duckdb(df, table_name):
                    st.success(f"Successfully generated {num_records} product records and saved to table '{table_name}'.")

                    # Show SQL query to retrieve data
                    st.subheader("SQL Query")
                    st.code(f"SELECT * FROM {table_name};")

                    # Option to view all data
                    if st.button("View All Data"):
                        result = execute_duckdb_query(f"SELECT * FROM {table_name}")
                        st.dataframe(result)
