# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY app.py .
COPY templates ./templates
COPY static ./static

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]