import os
import cups
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt', 'jpg', 'jpeg', 'png'}  # Add more as needed

# CUPS connection
conn = cups.Connection()

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Print the file
def print_file(filepath, printer_name=None):
    printers = conn.getPrinters()

    if not printer_name or printer_name not in printers:
        raise ValueError(f"Printer '{printer_name}' not found or not specified.")
    
    print(f"Printing {filepath} on {printer_name}")
    print_id = conn.printFile(printer_name, filepath, "Flask Print Job", {})
    print(f"Print job created with ID {print_id}")

# Flask route to handle file upload
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the user does not select a file, browser also
        # submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save the uploaded file
            file.save(filepath)

            # Get the printer name from the form
            printer_name = request.form.get('printer')

            try:
                # Send the file to the printer
                print_file(filepath, printer_name)
                flash(f"File {filename} sent to printer {printer_name}!")
            except Exception as e:
                flash(f"Failed to print the file: {str(e)}")

            return redirect(url_for('upload_file'))
    
    # Display the available printers in the dropdown
    printers = conn.getPrinters()
    return render_template("upload.html", printers=printers)

if __name__ == "__main__":
    app.secret_key = 'supersecretkey'  # For flashing messages
    app.run(host="0.0.0.0", port=5000)
