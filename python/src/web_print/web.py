import os

import cups
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

DEFAULT_ALLOWED_EXTENSIONS = {"pdf", "txt", "jpg", "jpeg", "png"}
PRINTER_STATE_LABELS = {
    3: "Idle",
    4: "Printing",
    5: "Stopped",
}
JOB_STATE_LABELS = {
    3: "Pending",
    4: "Held",
    5: "Processing",
    6: "Stopped",
    7: "Canceled",
    8: "Aborted",
    9: "Completed",
}
OFFLINE_REASON_MARKERS = (
    "offline",
    "connecting-to-device",
    "timed-out",
    "unreachable",
)
OFFLINE_MESSAGE_MARKERS = (
    "unable to connect",
    "connection timed out",
    "timed out",
    "offline",
    "unreachable",
)


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

    def _normalize_reasons(raw_reasons: object) -> list[str]:
        if isinstance(raw_reasons, str):
            values = [value.strip() for value in raw_reasons.split(",")]
        elif isinstance(raw_reasons, (list, tuple, set)):
            values = [str(value).strip() for value in raw_reasons]
        else:
            values = []
        return [value for value in values if value and value != "none"]

    def _is_offline(state_message: str, reasons: list[str]) -> bool:
        reasons_text = " ".join(reasons).lower()
        message_text = state_message.lower()
        reason_hit = any(marker in reasons_text for marker in OFFLINE_REASON_MARKERS)
        message_hit = any(marker in message_text for marker in OFFLINE_MESSAGE_MARKERS)
        return reason_hit or message_hit

    def get_printer_status(conn: cups.Connection, printer_name: str, printer_info: dict) -> dict:
        state_code = printer_info.get("printer-state")
        status_label = PRINTER_STATE_LABELS.get(state_code, f"Unknown ({state_code})")
        state_message = printer_info.get("printer-state-message", "")
        is_accepting = printer_info.get("printer-is-accepting-jobs", True)
        reasons = _normalize_reasons(printer_info.get("printer-state-reasons"))

        # getPrinters() may omit attributes depending on backend/cups version.
        if not reasons:
            try:
                attributes = conn.getPrinterAttributes(printer_name)
                reasons = _normalize_reasons(attributes.get("printer-state-reasons"))
                if not state_message:
                    state_message = str(attributes.get("printer-state-message", ""))
            except cups.IPPError:
                pass

        connectivity = "Offline" if _is_offline(state_message, reasons) else "Online"

        return {
            "name": printer_name,
            "state": status_label,
            "message": state_message or "No status message",
            "connectivity": connectivity,
            "accepting_jobs": "Yes" if is_accepting else "No",
            "reasons": ", ".join(reasons) if reasons else "none",
            "location": printer_info.get("printer-location", "Unknown"),
            "description": printer_info.get("printer-info", "No description available"),
        }

    def get_queue_for_printer(conn: cups.Connection, printer_name: str) -> list[dict]:
        queue: list[dict] = []
        jobs = conn.getJobs(which_jobs="not-completed")
        for job_id, job in jobs.items():
            printer_uri = job.get("job-printer-uri", "")
            if not printer_uri.endswith(f"/{printer_name}"):
                continue

            state_code = job.get("job-state")
            queue.append(
                {
                    "id": job_id,
                    "name": job.get("job-name", "Unnamed Job"),
                    "user": job.get("job-originating-user-name", "unknown"),
                    "state": JOB_STATE_LABELS.get(state_code, f"Unknown ({state_code})"),
                    "size_bytes": job.get("job-k-octets", 0) * 1024,
                }
            )
        return sorted(queue, key=lambda item: item["id"], reverse=True)

    @app.route("/", methods=["GET", "POST"])
    def upload_file():
        selected_printer = request.args.get("printer", "")

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

                return redirect(url_for("upload_file", printer=printer_name))

        conn = cups.Connection()
        printers = conn.getPrinters()

        if not selected_printer and printers:
            selected_printer = next(iter(printers.keys()))

        selected_printer_info = printers.get(selected_printer)
        printer_status = None
        queue = []
        if selected_printer_info:
            printer_status = get_printer_status(conn, selected_printer, selected_printer_info)
            queue = get_queue_for_printer(conn, selected_printer)

        return render_template(
            "upload.html",
            printers=printers,
            selected_printer=selected_printer,
            printer_status=printer_status,
            queue=queue,
        )

    return app


def main() -> None:
    app = create_app()
    host = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_RUN_PORT", "5000"))
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
