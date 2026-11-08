
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "data-shapers-secret-key"

# Database path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / "complaints.db"


# Database connection
def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Complaint registration
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        customer = request.form.get("customer", "").strip()
        complaint = request.form.get("complaint", "").strip()
        category = request.form.get("category", "")
        urgency = request.form.get("urgency", "")

        if not customer or not complaint or not category or urgency not in ["High", "Medium", "Low"]:
            flash("Please fill in all fields correctly.")
            return redirect(url_for("register"))

        # Assign priority
        if urgency == "High":
            priority = "Immediate Attention"
        elif urgency == "Medium":
            priority = "Normal Attention"
        else:
            priority = "Low Attention"

        connection = get_connection()
        cursor = connection.cursor()

        # Generate complaint ID
        cursor.execute(
            "SELECT MAX(Complaint_ID) FROM complaints"
        )
        result = cursor.fetchone()[0]
        new_id = (result or 1000) + 1

        cursor.execute("""
            INSERT INTO complaints
            (Complaint_ID, Customer, Complaint, Category,
             Urgency, Priority_Status, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            new_id,
            customer,
            complaint,
            category,
            urgency,
            priority,
            "Pending"
        ))

        connection.commit()
        connection.close()

        flash(f"Complaint registered successfully! Your Complaint ID is {new_id}.")
        return redirect(url_for("home"))

    return render_template("complaint_form.html")


# Dashboard
@app.route("/dashboard")
def dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    # Total complaints
    cursor.execute("SELECT COUNT(*) FROM complaints")
    total = cursor.fetchone()[0]

    # Status-wise counts
    cursor.execute("""
        SELECT Status, COUNT(*)
        FROM complaints
        GROUP BY Status
    """)
    status_counts = dict(cursor.fetchall())

    pending = status_counts.get("Pending", 0)
    progress = status_counts.get("In Progress", 0)
    resolved = status_counts.get("Resolved", 0)

    # Category-wise analysis
    cursor.execute("""
        SELECT Category, COUNT(*)
        FROM complaints
        GROUP BY Category
    """)
    category_data = cursor.fetchall()

    # Urgency-wise analysis
    cursor.execute("""
        SELECT Urgency, COUNT(*)
        FROM complaints
        GROUP BY Urgency
    """)
    urgency_data = cursor.fetchall()

    # Complaint details
    cursor.execute("""
        SELECT Complaint_ID, Customer, Complaint, Category,
               Urgency, Priority_Status, Status
        FROM complaints
        ORDER BY Complaint_ID DESC
    """)
    complaints = cursor.fetchall()

    connection.close()

    return render_template(
        "dashboard.html",
        total=total,
        pending=pending,
        progress=progress,
        resolved=resolved,
        category_data=[list(row) for row in category_data],
        urgency_data=[list(row) for row in urgency_data],
        complaints=[dict(row) for row in complaints]
    )


# Update complaint status
@app.route("/update_status", methods=["POST"])
def update_status():

    complaint_id = request.form.get("complaint_id")
    new_status = request.form.get("status")

    allowed_statuses = ["Pending", "In Progress", "Resolved"]

    if new_status not in allowed_statuses:
        flash("Invalid complaint status.")
        return redirect(url_for("dashboard"))

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE complaints
        SET Status = ?
        WHERE Complaint_ID = ?
    """, (new_status, complaint_id))

    connection.commit()
    connection.close()

    flash("Complaint status updated successfully!")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)

