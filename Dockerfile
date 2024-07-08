# Use Python base image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy all files to the working directory in the container
COPY . .

# Expose the port that Flask is running on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
