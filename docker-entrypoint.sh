#!/bin/sh
set -e

service cups start

# Register the printer in the background, retrying until the printer is reachable
(
    until lpadmin -p "$PRINTER_NAME" -E -v "ipp://$PRINTER_IP/ipp/print" -m everywhere 2>/dev/null; do
        echo "Printer not reachable, retrying in 15s..."
        sleep 15
    done
    echo "Printer '$PRINTER_NAME' registered successfully."
) &

exec web-print
