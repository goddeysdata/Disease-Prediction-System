from flask import Blueprint, render_template, redirect, url_for, request, session
import pymysql

# ✅ Create Blueprint
admin_bp = Blueprint("admin_bp", __name__)

# ✅ Database connection helper
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Stonecold.123",
        database="flask_project",
        cursorclass=pymysql.cursors.DictCursor
    )

# ✅ View all doctors and patients
@admin_bp.route("/admin/users")
def manage_users():
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role IN ('doctor', 'patient')")
    users = cursor.fetchall()
    conn.close()

    return render_template("admin/manage_users.html", users=users)

# ✅ Add new doctor or patient
@admin_bp.route("/admin/users/add", methods=["POST"])
def add_user():
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    role = request.form["role"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
        (name, email, password, role)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("admin_bp.manage_users"))

# ✅ Delete a doctor or patient
@admin_bp.route("/admin/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_bp.manage_users"))

# ✅ View all disease records
@admin_bp.route("/admin/data")
def manage_data():
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM disease_data")
    diseases = cursor.fetchall()
    conn.close()

    return render_template("admin/manage_data.html", diseases=diseases)

# ✅ Add new disease record
@admin_bp.route("/admin/data/add", methods=["POST"])
def add_disease():
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    patient_id = request.form["patient_id"]
    disease = request.form["disease"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO disease_data (patient_id, disease) VALUES (%s, %s)",
        (patient_id, disease)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("admin_bp.manage_data"))

# ✅ Delete a disease record
@admin_bp.route("/admin/data/delete/<int:id>")
def delete_disease(id):
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM disease_data WHERE id = %s", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_bp.manage_data"))

# inside admin_routes.py or wherever your admin blueprint is defined
@admin_bp.route('/index')
def index():
    return render_template('index.html')
