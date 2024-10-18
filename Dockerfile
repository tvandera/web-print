# Step 1: Base image
FROM python:3.9-slim

# Step 2: Install system dependencies (CUPS and build tools)
RUN apt-get update && \
    apt-get install -y cups libcups2-dev build-essential && \
    apt-get clean

# Step 3: Install Flask and pycups
RUN pip install flask
RUN pip install pycups

# Step 4: Copy the application code
WORKDIR /app
COPY . /app

# Step 5: Expose the Flask port and the CUPS web interface port
EXPOSE 5000
EXPOSE 631

# Step 6: Start CUPS and run the Flask application
CMD service cups start && python3 app.py
