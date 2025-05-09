"""
Custom Dataset View

The most flexible part of our app - build your own custom datasets from scratch!
Choose from hundreds of Faker providers to create exactly the data you need,
whether it's for testing, demos, or just playing around with different data types.
"""

import streamlit as st
import pandas as pd
import duckdb
import faker
import inspect
import random
from .database import execute_duckdb_query

# Initialize Faker
fake = faker.Faker()

faker_elements_list = [
    'address', 'am_pm', 'android_platform_token', 'ascii_company_email', 'ascii_email',
    'ascii_free_email', 'ascii_safe_email', 'bank_country', 'bban', 'binary', 'boolean',
    'bothify', 'bs', 'building_number', 'cache_pattern', 'catch_phrase', 'century', 'chrome',
    'city', 'city_prefix', 'city_suffix', 'color', 'color_name', 'company', 'company_email',
    'company_suffix', 'coordinate', 'country', 'country_calling_code', 'country_code',
    'credit_card_expire', 'credit_card_full', 'credit_card_number', 'credit_card_provider',
    'credit_card_security_code', 'cryptocurrency', 'cryptocurrency_code', 'cryptocurrency_name',
    'csv', 'currency', 'currency_code', 'currency_name', 'currency_symbol', 'date',
    'date_of_birth', 'date_this_century', 'date_this_decade', 'date_this_month',
    'date_this_year', 'date_time', 'date_time_ad', 'date_time_this_century',
    'date_time_this_decade', 'date_time_this_month', 'date_time_this_year', 'day_of_month',
    'day_of_week', 'dga', 'domain_name', 'domain_word', 'dsv', 'ean', 'ean13', 'ean8', 'ein',
    'email', 'factories', 'file_extension', 'file_name', 'file_path', 'first_name',
    'first_name_female', 'first_name_male', 'free_email', 'free_email_domain',
    'future_date', 'future_datetime', 'hex_color', 'hexify', 'hostname',
    'http_method', 'iban', 'image_url', 'internet_explorer', 'invalid_ssn',
    'ios_platform_token', 'ipv4', 'ipv4_network_class', 'ipv4_private',
    'ipv4_public', 'ipv6', 'isbn10', 'isbn13', 'iso8601', 'items', 'itin', 'job',
    'language_code', 'language_name', 'last_name', 'last_name_female', 'last_name_male',
    'latitude', 'latlng', 'lexify', 'license_plate', 'linux_platform_token', 'linux_processor',
    'local_latlng', 'locale', 'locales', 'localized_ean', 'localized_ean13', 'localized_ean8',
    'location_on_land', 'longitude', 'mac_address', 'mac_platform_token', 'mac_processor',
    'md5', 'military_apo', 'military_dpo', 'military_ship', 'military_state', 'mime_type',
    'month', 'month_name', 'msisdn', 'name', 'name_female', 'name_male', 'null_boolean',
    'numerify', 'paragraph', 'paragraphs', 'parse', 'password', 'past_date',
    'past_datetime', 'phone_number', 'port_number', 'postalcode', 'postalcode_in_state',
    'postalcode_plus4', 'postcode', 'postcode_in_state', 'prefix', 'prefix_female',
    'prefix_male', 'profile', 'psv', 'pybool', 'pydecimal','rgb_color', 'rgb_css_color',
    'safe_color_name', 'safe_email', 'safe_hex_color', 'secondary_address',
    'sentence', 'sentences', 'set_formatter', 'sha1', 'sha256',
    'simple_profile', 'slug', 'ssn', 'state', 'state_abbr', 'street_address',
    'street_name', 'street_suffix', 'suffix', 'suffix_female', 'suffix_male', 'tar',
    'text', 'texts', 'time', 'time_delta', 'time_object', 'time_series', 'timezone',
    'tld', 'tsv', 'unix_device', 'unix_partition', 'unix_time', 'upc_a', 'upc_e', 'uri',
    'uri_extension', 'uri_page', 'uri_path', 'url', 'user_agent', 'user_name', 'uuid4',
    'weights', 'windows_platform_token', 'word', 'words', 'year', 'zip', 'zipcode',
    'zipcode_in_state', 'zipcode_plus4'
]

def get_faker_providers():
    """
    Scans through all the Faker goodies we can offer in the custom generator.

    Digs into the Faker library to find all the cool data types you can generate,
    along with helpful descriptions so you know what each one does.
    """
    methods_details = {}

    for name in faker_elements_list:
        description = "Description not available or attribute/method not found."
        method_or_attr = None

        try:
            method_or_attr = getattr(fake, name, None)
            if method_or_attr is not None:
                docstring = getattr(method_or_attr, '__doc__', None)
                if docstring:
                    description = docstring.strip()
                elif callable(method_or_attr):
                    # Get the signature of the method
                    try:
                        sig = inspect.signature(method_or_attr)
                        params = []
                        for param_name, param in sig.parameters.items():
                            if param.default == inspect.Parameter.empty:
                                params.append(param_name)
                            else:
                                params.append(f"{param_name}={param.default}")

                        if params:
                            params_str = ", ".join(params)
                            description = f"Callable method '{name}({params_str})' found, but it has no specific docstring."
                        else:
                            try:
                                # Try to get the source code of the method
                                method_source = inspect.getsource(method_or_attr)
                                description = f"Callable method '{name}()' found, but it has no specific docstring. \nMethod definition: \n{method_source}"
                            except Exception:
                                description = f"Callable method '{name}()' found, but it has no specific docstring."
                    except Exception:
                        description = f"Callable method '{name}' found, but it has no specific docstring."
                else:
                    description = f"Attribute '{name}' found, but it has no specific docstring. Value type: {type(method_or_attr).__name__}"
            else:
                description = f"Method or attribute '{name}' not found on the Faker instance."

        except Exception as e:
            # This might catch rare errors during getattr or docstring access
            description = f"Could not retrieve details for '{name}': {str(e)}"

        methods_details[name] = {
            'name': name,
            'description': description
        }

    return methods_details

def generate_custom_data(num_records, fields):
    """
    The heart of our custom data generator - creates your dataset exactly how you want it.

    Give it the number of records you need and your field specifications, and it'll
    create a beautiful dataset using all the Faker methods you've selected. Each field
    can use a different Faker provider to generate just the right kind of data.

    You'll get back a pandas DataFrame ready to preview, save, or export.
    """
    data = []

    for _ in range(num_records):
        record = {}

        for field in fields:
            field_name = field['name']
            faker_method = field['faker_method']
            args = field.get('args', [])
            kwargs = field.get('kwargs', {})

            # Get the Faker method
            method = getattr(fake, faker_method)

            # Call the method with args and kwargs
            try:
                value = method(*args, **kwargs)
                record[field_name] = value
            except Exception as e:
                st.error(f"Error generating value for field '{field_name}' using method '{faker_method}': {e}")
                record[field_name] = None

        data.append(record)

    return pd.DataFrame(data)

def save_custom_data_to_duckdb(df, table_name):
    """
    Tucks your custom dataset safely into our DuckDB database for safekeeping.

    Takes the DataFrame you've just created and gives it a permanent home in DuckDB
    with whatever table name you've chosen. This makes it available for SQL queries
    and exports later on.
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

def custom_view():
    """
    Powers our most flexible data generation page - the custom dataset builder.

    This is where you get to play data architect and design your own datasets
    from scratch using any combination of Faker providers. The sky's the limit!
    """
    st.header("Custom Dataset Generator")

    st.markdown("""
    Generate custom datasets using Faker. Select the fields you want to include,
    choose the Faker method for each field, and specify the number of records to generate.
    """)

    # Get all Faker providers and methods
    providers = get_faker_providers()

    # Number of records to generate
    num_records = st.number_input("Number of records to generate:", min_value=1, max_value=100000, value=100)

    # Fields to include
    st.subheader("Fields")

    # Initialize session state for fields if not exists
    if 'custom_fields' not in st.session_state:
        st.session_state.custom_fields = []

    # Add field button
    if st.button("Add Field"):
        st.session_state.custom_fields.append({
            'name': f"field_{len(st.session_state.custom_fields) + 1}",
            'faker_method': faker_elements_list[0],
            'args': [],
            'kwargs': {}
        })

    # Display fields
    for i, field in enumerate(st.session_state.custom_fields):
        with st.expander(f"Field: {field['name']}", expanded=True):
            # Field name
            field['name'] = st.text_input(f"Field name", field['name'], key=f"field_name_{i}")

            # Faker method
            field['faker_method'] = st.selectbox(
                "Faker method",
                options=faker_elements_list,
                index=faker_elements_list.index(field['faker_method']) if field['faker_method'] in faker_elements_list else 0,
                key=f"faker_method_{i}"
            )

            # Show description of the selected method
            if field['faker_method'] in providers:
                st.info(providers[field['faker_method']]['description'])

            # Remove field button
            if st.button("Remove Field", key=f"remove_field_{i}"):
                st.session_state.custom_fields.pop(i)
                st.experimental_rerun()

    # Table name
    table_name = st.text_input("Table name:", "custom_dataset")

    # Generate button
    if st.button("Generate Custom Dataset"):
        if not st.session_state.custom_fields:
            st.warning("Please add at least one field.")
        else:
            # Prepare fields for generation
            fields = []
            for field in st.session_state.custom_fields:
                fields.append({
                    'name': field['name'],
                    'faker_method': field['faker_method'],
                    'args': field.get('args', []),
                    'kwargs': field.get('kwargs', {})
                })

            with st.spinner("Generating custom dataset..."):
                # Generate data
                df = generate_custom_data(num_records, fields)

                # Display preview
                st.subheader("Preview")
                st.dataframe(df.head(10))

                # Save to DuckDB
                if save_custom_data_to_duckdb(df, table_name):
                    st.success(f"Successfully generated {num_records} records and saved to table '{table_name}'.")

                    # Show SQL query to retrieve data
                    st.subheader("SQL Query")
                    st.code(f"SELECT * FROM {table_name};")

                    # Option to view all data
                    if st.button("View All Data"):
                        result = execute_duckdb_query(f"SELECT * FROM {table_name}")
                        st.dataframe(result)

                    # Download options
                    st.subheader("Download Data")
                    col1, col2 = st.columns(2)

                    # Get the full dataset for download
                    download_data = execute_duckdb_query(f"SELECT * FROM {table_name}")

                    # Clean the data by removing newline characters from string columns
                    for column in download_data.select_dtypes(include=['object']).columns:
                        download_data[column] = download_data[column].astype(str).str.replace('\n', ' ')

                    # CSV download
                    csv = download_data.to_csv(index=False)
                    col1.download_button(
                        label="Download as CSV",
                        data=csv,
                        file_name=f"{table_name}.csv",
                        mime="text/csv",
                    )

                    # JSON download
                    json = download_data.to_json(orient="records")
                    col2.download_button(
                        label="Download as JSON",
                        data=json,
                        file_name=f"{table_name}.json",
                        mime="application/json",
                    )

    # Example usage
    with st.expander("Example Usage"):
        st.markdown("""
        ### How to use the Custom Dataset Generator

        1. Click the "Add Field" button to add a new field to your dataset.
        2. Give the field a name (e.g., "first_name", "email", "address").
        3. Select a provider (e.g., "person", "internet", "address").
        4. Select a method from the provider (e.g., "name", "email", "street_address").
        5. Repeat steps 1-4 for each field you want in your dataset.
        6. Enter a name for your table.
        7. Click "Generate Custom Dataset" to create your dataset.

        ### Example Fields

        - **Name**: first_name, Provider: person, Method: first_name
        - **Email**: email, Provider: internet, Method: email
        - **Address**: address, Provider: address, Method: street_address
        - **Phone**: phone, Provider: phone_number, Method: phone_number
        - **Company**: company, Provider: company, Method: company
        - **Job**: job, Provider: job, Method: job
        - **Text**: text, Provider: lorem, Method: paragraph
        """)
