FROM python:3.11.12-bullseye

WORKDIR /opt/app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY streamlit_app/ ./streamlit_app/

# Create directories for data and exports
RUN mkdir -p exports

# Set environment variables
ENV PYTHONPATH=/opt/app
ENV PYTHONUNBUFFERED=1

# Expose port for Streamlit
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
