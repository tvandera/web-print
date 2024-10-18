import cups

def list_available_printers():
    # Create a CUPS connection
    conn = cups.Connection()
    
    # Get all printers and their information
    printers = conn.getPrinters()

    if not printers:
        print("No printers found on the network.")
        return

    # List printers
    print("Available printers on the network:")
    for printer_name, printer_info in printers.items():
        print(f"Printer Name: {printer_name}")
        print(f"  Location: {printer_info.get('printer-location', 'Unknown')}")
        print(f"  Description: {printer_info.get('printer-info', 'No description available')}")
        print(f"  Status: {printer_info.get('printer-state-message', 'No status available')}")
        print()

def print_pdf(pdf_path, printer_name):
    # Create a CUPS connection
    conn = cups.Connection()
    
    # Get the list of all printers
    printers = conn.getPrinters()
    
    if printer_name not in printers:
        raise ValueError(f"Printer '{printer_name}' not found.")
    
    # Print the PDF file
    conn.printFile(printer_name, pdf_path, "Python Print Job", {})
    print(f"Print job for '{pdf_path}' sent to '{printer_name}'")

if __name__ == "__main__":
    # Scan for available network printers
    list_available_printers()

    # Uncomment the following lines to test the print function after selecting a printer
    # pdf_file_path = "/path/to/your/file.pdf"
    # printer = "Your-Printer-Name"
    # print_pdf(pdf_file_path, printer)
