import os

import cups
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

DEFAULT_ALLOWED_EXTENSIONS = {"pdf", "txt", "jpg", "jpeg", "png"}


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates")
    app.config["UPLOAD_FOLDER"] = "/tmp"
    app.config["ALLOWED_EXTENSIONS"] = DEFAULT_ALLOWED_EXTENSIONS
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")

    def allowed_file(filename: str) -> bool:
        return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

    def print_file(filepath: str, printer_name: str | None = None) -> None:
        conn = cups.Connection()
        printers = conn.getPrinters()

        if not printer_name or printer_name not in printers:
            raise ValueError(f"Printer '{printer_name}' not found or not specified.")

        print(f"Printing {filepath} on {printer_name}")
        print_id = conn.printFile(printer_name, filepath, "Flask Print Job", {})
        print(f"Print job created with ID {print_id}")

    @app.route("/", methods=["GET", "POST"])
    def upload_file():
        if request.method == "POST":
            if "file" not in request.files:
                flash("No file part")
                return redirect(request.url)

            file = request.files["file"]

            if file.filename == "":
                flash("No selected file")
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)

                printer_name = request.form.get("printer")

                try:
                    print_file(filepath, printer_name)
                    flash(f"File {filename} sent to printer {printer_name}!")
                except Exception as e:
                    flash(f"Failed to print the file: {str(e)}")

                return redirect(url_for("upload_file"))

        conn = cups.Connection()
        printers = conn.getPrinters()
        return render_template("upload.html", printers=printers)

    return app


def main() -> None:
    app = create_app()
    host = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_RUN_PORT", "5000"))
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
