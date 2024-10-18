import cups
import os

def print_pdf(pdf_path, printer_name=None):
    # Create a CUPS connection
    conn = cups.Connection()
    
    # Get a list of all printers
    printers = conn.getPrinters()
    
    if not printer_name:
        # Print available printers if printer_name is not provided
        print("Available printers:")
        for printer in printers:
            print(f" - {printer}")
        
        raise ValueError("No printer specified. Provide a printer name from the list above.")
    
    if printer_name not in printers:
        raise ValueError(f"Printer '{printer_name}' not found.")

    # Print the PDF file
    if os.path.exists(pdf_path) and pdf_path.endswith(".txt"):
        print(f"Printing {pdf_path} on {printer_name}")
        print_id = conn.printFile(printer_name, pdf_path, "Python Print Job", {})
        print(f"Print job created with ID {print_id}")
    else:
        raise FileNotFoundError(f"PDF file '{pdf_path}' not found or not a valid PDF.")

if __name__ == "__main__":
    # Specify the path to your PDF
    pdf_file_path = "test.txt"
    
    # Optional: specify your printer name (as seen in CUPS)
    # If left empty, the program will list available printers
    printer = "HP_LaserJet_400_M401dw_6E99D5"
    
    print_pdf(pdf_file_path, printer)
