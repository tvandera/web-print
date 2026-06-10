
# Flask CUPS Printer Application

This Docker image provides a Flask web application that allows users to upload files and print them using a network printer via CUPS (Common Unix Printing System). The printer is configured via the IPP protocol (Internet Printing Protocol).

## Features

- **File Upload**: Supports `pdf`, `txt`, `jpg`, `jpeg`, and `png` formats.
- **Network Printing**: Print files to a network printer using IPP.
- **Environment Variable Support**: Customize printer name and IP address via environment variables.
- **CUPS Integration**: Manages print jobs through CUPS within the Docker container.

## Python Package Usage

This repository is now a standard Python package using a `pyproject.toml` and `src` layout.

Install locally:

```bash
pip install .
```

Run the web app:

```bash
web-print
```

List printers (or print a file) from CLI:

```bash
web-print-printers
web-print-printers --print-file /path/to/file.pdf --printer "Printer_Name"
```

## How to Use

### Step 1: Pull the Docker Image

You can pull the image from Docker Hub using the following command:

```bash
docker pull <your-dockerhub-username>/cups-flask-printer:latest
```

### Step 2: Run the Docker Container

Run the container with default printer configuration:

```bash
docker run -d -p 5000:5000 <your-dockerhub-username>/cups-flask-printer
```

This command will:
- Launch the Flask web application on port `5000`.
- Automatically configure a network printer with the default IPP protocol at `ipp://10.25.0.218/ipp/print`.

### Step 3: Access the Web Application

Once the container is running, open a web browser and navigate to:

```
http://localhost:5000
```

You can upload files through the web interface and print them to the configured network printer.

### Customizing the Printer

If you want to override the default printer configuration (name or IP address), you can pass environment variables to the container when starting it:

```bash
docker run -d -p 5000:5000 \
  -e PRINTER_NAME="My_Printer" \
  -e PRINTER_IP="192.168.1.100" \
  <your-dockerhub-username>/cups-flask-printer
```

In this example:
- **PRINTER_NAME**: Specifies the printer name.
- **PRINTER_IP**: Specifies the IP address of the network printer.

### Printer Configuration (Inside the Container)

The printer is automatically added to CUPS inside the container using the `lpadmin` command during container startup:

```bash
lpadmin -p $PRINTER_NAME -E -v ipp://$PRINTER_IP/ipp/print -m everywhere
```

### Verify Printer Configuration

To verify that the printer has been configured inside the container, you can use the following command:

```bash
docker exec -it <container-id> lpstat -p
```

This will list the available printers in the container.

## Example Usage

1. Upload a file (e.g., PDF) through the web interface.
2. The file will be printed using the specified network printer.

## Troubleshooting

- **Ensure Printer is Reachable**: Verify that the printer is accessible at the specified IP address (`10.25.0.218` by default).
- **Check Container Logs**: View the logs inside the container for any errors:
   ```bash
   docker logs <container-id>
   ```
- **Check CUPS Status**: Use the following command to verify the status of CUPS inside the container:
   ```bash
   docker exec -it <container-id> lpstat -r
   ```

## License

This project is licensed under the MIT License.
