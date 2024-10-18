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

# Step 6: Define environment variables with defaults (can be overridden in docker run)
ENV PRINTER_NAME="HP_LaserJet_400_M401dw_6E99D5"
ENV PRINTER_IP="10.25.0.218"

# Step 7: Start CUPS and run the Flask app
CMD service cups start && \
    lpadmin -p $PRINTER_NAME -E -v ipp://$PRINTER_IP/ipp/print -m everywhere && \
    python app.py