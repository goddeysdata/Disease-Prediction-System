from flask import Blueprint, render_template, request, redirect, url_for, session
import pymysql

doctor_bp = Blueprint("doctor_bp", __name__)

# DB connection
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Stonecold.123",
        database="flask_project",
        cursorclass=pymysql.cursors.DictCursor
    )

# Doctor Dashboard
@doctor_bp.route("/doctor/dashboard")
def doctor_dashboard():
    if session.get("role") != "doctor":
        return redirect(url_for("home"))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role='patient'")
    patients = cursor.fetchall()
    conn.close()

    return render_template("doctor_dashboard.html", patients=patients)

# View All Patient Records
@doctor_bp.route("/doctor/view_patients")
def view_patients():
    if session.get("role") != "doctor":
        return redirect(url_for("home"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role='patient'")
    patients = cursor.fetchall()
    conn.close()

    return render_template("doctor/view_patients.html", patients=patients)


# View & Update a Patient Record
@doctor_bp.route("/doctor/patient/<int:patient_id>", methods=["GET", "POST"])
def update_patient(patient_id):
    if session.get("role") != "doctor":
        return redirect(url_for("home"))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        medical_history = request.form["medical_history"]
        cursor.execute(
            "UPDATE users SET medical_history=%s WHERE id=%s", 
            (medical_history, patient_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("doctor_bp.doctor_dashboard"))

    cursor.execute("SELECT * FROM users WHERE id=%s", (patient_id,))
    patient = cursor.fetchone()
    conn.close()

    return render_template("doctor/update_patient.html", patient=patient)
