FROM python:3.9-slim

WORKDIR /app

# Copy requirements from root directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all necessary files from root directory
COPY main.py .
COPY models.py .
COPY config.py .
COPY bedrock_service.py .
COPY aws_bedrock_degub.py .
COPY aws_test.py .

# Copy backend directory contents (if any)
COPY backend/ ./backend/

# Expose port
EXPOSE 8000

# Run the main.py from root
CMD ["python", "main.py"]
