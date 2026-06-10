from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from web_print.printers import list_available_printers, main, print_file


def print_pdf(pdf_path, printer_name):
    return print_file(pdf_path, printer_name)


if __name__ == "__main__":
    main()
