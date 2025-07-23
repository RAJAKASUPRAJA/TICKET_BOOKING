from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from datetime import datetime
import sqlite3, os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = "change-me"      # needed for flash messages
DB_PATH = "database.db"

def get_db():
    return sqlite3.connect(DB_PATH)

# ─────────────────── ROUTES ───────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        f = request.form
        try:
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO bookings (name, email, origin, destination, amount, created)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        f["name"],
                        f["email"],
                        f["origin"],
                        f["destination"],
                        float(f["amount"]),
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ),
                )
                booking_id = cur.lastrowid
            return redirect(url_for("confirmation", booking_id=booking_id))
        except Exception as e:
            flash(f"Error: {e}", "danger")
    return render_template("booking.html")

@app.route("/confirmation/<int:booking_id>")
def confirmation(booking_id):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM bookings WHERE id=?", (booking_id,))
        booking = cur.fetchone()
    if not booking:
        return "Booking not found", 404
    return render_template("confirmation.html", booking=booking)

@app.route("/download/<int:booking_id>")
def download(booking_id):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM bookings WHERE id=?", (booking_id,))
        row = cur.fetchone()
    if not row:
        return "Booking not found", 404

    (_id, name, email, origin, destination, amount, created) = row

    buf = BytesIO()
    pdf = canvas.Canvas(buf, pagesize=A4)
    pdf.setTitle(f"ticket_{_id}.pdf")

    y = 800
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "Ticket Confirmation")
    pdf.setFont("Helvetica", 12)
    y -= 40

    for line in (
        f"Booking ID : {_id}",
        f"Name       : {name}",
        f"Email      : {email}",
        f"From       : {origin}",
        f"To         : {destination}",
        f"Amount     : ₹{amount}",
        f"Created    : {created}",
    ):
        pdf.drawString(50, y, line)
        y -= 22

    pdf.showPage()
    pdf.save()
    buf.seek(0)

    return send_file(buf,
                     as_attachment=True,
                     download_name=f"ticket_{_id}.pdf",
                     mimetype="application/pdf")

# ──────────────────────────────────────────────
if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        from init_db import init_db
        init_db(DB_PATH)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

