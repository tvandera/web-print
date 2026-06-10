import argparse

import cups


def list_available_printers() -> None:
    conn = cups.Connection()
    printers = conn.getPrinters()

    if not printers:
        print("No printers found on the network.")
        return

    print("Available printers on the network:")
    for printer_name, printer_info in printers.items():
        print(f"Printer Name: {printer_name}")
        print(f"  Location: {printer_info.get('printer-location', 'Unknown')}")
        print(f"  Description: {printer_info.get('printer-info', 'No description available')}")
        print(f"  Status: {printer_info.get('printer-state-message', 'No status available')}")
        print()


def print_file(filepath: str, printer_name: str) -> None:
    conn = cups.Connection()
    printers = conn.getPrinters()

    if printer_name not in printers:
        raise ValueError(f"Printer '{printer_name}' not found.")

    conn.printFile(printer_name, filepath, "Python Print Job", {})
    print(f"Print job for '{filepath}' sent to '{printer_name}'")


def main() -> None:
    parser = argparse.ArgumentParser(description="List printers or print a file via CUPS.")
    parser.add_argument("--print-file", dest="print_file_path", help="Path to a file to print")
    parser.add_argument("--printer", dest="printer_name", help="Printer name for --print-file")
    args = parser.parse_args()

    if args.print_file_path:
        if not args.printer_name:
            parser.error("--printer is required when using --print-file")
        print_file(args.print_file_path, args.printer_name)
        return

    list_available_printers()


if __name__ == "__main__":
    main()
