# Superset Standalone

This repository is designed to work with Apache Superset, 
providing a powerful dataset generation tool that creates 
realistic data which can be seamlessly imported into 
Superset for visualization and analysis. 
The generated datasets are ready to store in PostgreSQL 
that makes the data compatible with Superset's data 
exploration capabilities, enabling users to quickly 
build dashboards and perform data analysis without 
needing real production data.

The Superset instance can be deployed using Docker pulling: `jasonjimnz/superset_standalone` or going into:
[https://hub.docker.com/r/jasonjimnz/superset_standalone](https://hub.docker.com/r/jasonjimnz/superset_standalone)

**This tools are not production ready, logs can show data, 
if you wanna do a secure installation in your infrastructure, follow
[Apache Superset documentation](https://superset.apache.org/docs/intro)**

## Dataset Generator

A Streamlit application for generating realistic datasets using Faker. 
This application allows you to generate various types of datasets 
including customers, products, companies, and transactions, 
as well as custom datasets based on Faker providers.

## Features

- Generate customer data with various fields (name, email, address, etc.)
- Generate product data with various fields (name, price, category, etc.)
- Generate company data with various fields (name, industry, revenue, etc.)
- Generate transaction data with various fields (amount, date, payment method, etc.)
- Create custom datasets using any Faker provider
- Store data in DuckDB for local querying
- Connect to PostgreSQL for advanced database operations
- Export data to CSV files

## Requirements

- Docker and Docker Compose
- Python 3.11+ (if running locally)

## Quick Start with Docker

1. Clone this repository:
   ```shell
   git clone git@github.com:jasonjimnz/superset_standalone.git
   cd superset_standalone
   ```

2. Start the application using Docker Compose:
   ```shell
   docker-compose up -d
   ```

3. Access the application in your browser:
   ```
   http://localhost:8501
   ```

## Running Locally

1. Clone this repository:
   ```shell
   git clone git@github.com:jasonjimnz/superset_standalone.git
   cd superset_standalone
   ```

2. Create a virtual environment and install dependencies:
   ```shell
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```shell
   streamlit run streamlit_app/app.py
   ```

4. Access the application in your browser:
   ```shell
   http://localhost:8501
   ```

## Usage

### Generating Customer Data

1. Navigate to the "Customers" page
2. Select the fields you want to include in your dataset
3. Specify the number of records to generate
4. Enter a name for the table
5. Click "Generate Customer Data"

### Generating Product Data

1. Navigate to the "Products" page
2. Select the fields you want to include in your dataset
3. Specify the number of records to generate
4. Enter a name for the table
5. Click "Generate Product Data"

### Generating Company Data

1. Navigate to the "Companies" page
2. Select the fields you want to include in your dataset
3. Specify the number of records to generate
4. Enter a name for the table
5. Click "Generate Company Data"

### Generating Transaction Data

1. Navigate to the "Transactions" page
2. Select reference tables if you have already generated customer, product, or company data
3. Select the fields you want to include in your dataset
4. Specify the number of records to generate
5. Enter a name for the table
6. Click "Generate Transaction Data"

### Creating Custom Datasets

1. Navigate to the "Custom Dataset" page
2. Click "Add Field" to add a new field to your dataset
3. Give the field a name
4. Select a provider and method for the field
5. Repeat steps 2-4 for each field you want in your dataset
6. Enter a name for the table
7. Click "Generate Custom Dataset"

### Database Operations

1. Navigate to the "Database Operations" page
2. Use the "DuckDB Operations" tab to query your local DuckDB database
3. Use the "PostgreSQL Operations" tab to connect to and query a PostgreSQL database
4. Use the "Data Transfer" tab to transfer data from DuckDB to PostgreSQL or export to CSV

## Project Structure

- `streamlit_app/`: Main application directory
  - `app.py`: Entry point for the Streamlit application
  - `views/`: Directory containing view modules
    - `customers.py`: Customer data generation view
    - `products.py`: Product data generation view
    - `companies.py`: Company data generation view
    - `transactions.py`: Transaction data generation view
    - `custom.py`: Custom dataset generation view
    - `database.py`: Database operations view
- `requirements.txt`: Python dependencies
- `superset.Dockerfile`: Dockerfile for Superset application
- `streamlit.Dockerfile`: Dockerfile for the Streamlit application
- `docker-compose.yml`: Docker Compose configuration

## License

[MIT License](LICENSE.md)
