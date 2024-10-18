# Step 1: Base image
FROM python:3.9-slim

# Step 2: Install system dependencies (CUPS and build tools)
RUN apt-get update && \
    apt-get install -y cups libcups2-dev build-essential && \
    apt-get clean

# Step 3: Install pycups for Python
RUN pip install pycups

# Step 4: Copy your Python application into the container
WORKDIR /app
COPY . /app

# Step 5: Expose CUPS web interface port
EXPOSE 631

# Step 6: Start CUPS service and run the Python application
CMD service cups start && python3 app.py
