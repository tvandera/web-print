
# Flask CUPS Printer Application

This application allows you to upload a file and print it using a network printer (configured with CUPS) from within a Docker container.

## Features

- Upload files of types `pdf`, `txt`, `jpg`, `jpeg`, and `png`.
- Automatically print uploaded files to a configured printer via IPP protocol.
- Uses CUPS for printing within the Docker container.

## Setup and Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Build the Docker image

```bash
docker build -t cups-flask-printer .
```

### 3. Run the Docker container

```bash
docker run -d -p 5000:5000 cups-flask-printer
```

### 4. Access the application

Open a web browser and navigate to:

```
http://localhost:5000
```

You can now upload a file and print it to the network printer.

## Printer Configuration

This setup uses an HP LaserJet 400 M401dw printer configured via IPP protocol at the following address:

```
ipp://10.25.0.218/ipp/print
```

### CUPS Configuration (Inside the Container)

The printer is automatically added to CUPS inside the container using the `lpadmin` command during container startup:

```bash
lpadmin -p HP_LaserJet_400_M401dw_6E99D5 -E -v ipp://10.25.0.218/ipp/print -m everywhere
```

### Verify Printer Configuration

To verify that the printer has been configured inside the container, you can use the following command:

```bash
docker exec -it <container-id> lpstat -p
```

This will list the available printers in the container.

## Troubleshooting

- Ensure that the printer is reachable at the specified IP address (`10.25.0.218`).
- If the application fails to print, check the logs using:

```bash
docker logs <container-id>
```

## License

This project is licensed under the MIT License.
