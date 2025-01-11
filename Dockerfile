# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr \
    ffmpeg \
    libsm6 \
    libxext6 \
    poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install any Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Streamlit will run on
EXPOSE 8501

# Run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
