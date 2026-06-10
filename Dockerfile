# Step 1: Build wheel with build dependencies
FROM python:3.12-slim AS builder

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends build-essential libcups2-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY python .
COPY README.md LICENSE ./
RUN pip wheel --no-cache-dir --wheel-dir /wheels .

# Step 2: Runtime image without build dependencies
FROM python:3.12-slim

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends cups libcups2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl && rm -rf /wheels

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Step 3: Expose the Flask port and the CUPS web interface port
EXPOSE 5000
EXPOSE 631

# Step 4: Define environment variables with defaults (can be overridden in docker run)
ENV PRINTER_NAME="HP_LaserJet_400_M401dw_6E99D5"
ENV PRINTER_IP="10.25.0.218"

# Step 5: Start CUPS and run the Flask app
ENTRYPOINT ["docker-entrypoint.sh"]