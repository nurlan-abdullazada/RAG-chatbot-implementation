FROM python:3.9-slim

WORKDIR /app

# Copy requirements from root directory  
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend directory contents
COPY frontend/ .

# Expose port
EXPOSE 8501

# Run app.py which should now be in the current directory
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]

