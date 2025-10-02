import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__, template_folder="frontend/templates")
app.secret_key = "super_secret_key_123"  # change to a stronger key in production

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "database", "attendance.db")

# ---------------- STUDENT PAGE ---------------- #
@app.route("/")
def student_page():
    return render_template("student.html")

@app.route("/submit", methods=["POST"])
def submit_attendance():
    name = request.form.get("name")
    roll_no = request.form.get("roll_no")

    if not name or not roll_no:
        flash("❌ Error: Missing name or roll number")
        return redirect(url_for("student_page"))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # check if roll number already exists (student already attended)
    cursor.execute("SELECT * FROM attendance WHERE roll_no = ?", (roll_no,))
    existing = cursor.fetchone()

    if existing:
        flash("⚠️ Attendance already submitted for this roll number!")
    else:
        cursor.execute("INSERT INTO attendance (name, roll_no) VALUES (?, ?)", (name, roll_no))
        conn.commit()
        flash("✅ Attendance submitted successfully!")

    conn.close()
    return redirect(url_for("student_page"))


# ---------------- ADMIN AUTH ---------------- #
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Replace this with DB check later
        if username == "Likla" and password == "Likla123":
            session["admin"] = True
            return redirect(url_for("admin_page"))
        else:
            return "❌ Invalid credentials"

    return render_template("login.html")

@app.route("/admin")
def admin_page():
    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, roll_no, timestamp FROM attendance ORDER BY timestamp DESC")
    records = cursor.fetchall()
    conn.close()

    return render_template("admin.html", records=records)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))

# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    if not os.path.exists(DB_NAME):
        print("⚠️ Database not found. Run 'python init_db.py' first.")
    app.run(debug=True)
