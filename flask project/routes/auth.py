from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_config import get_db_connection  # Ensure correct database import
import os

auth_bp = Blueprint("auth", __name__, template_folder="../templates")  # Ensure templates are found

# ✅ Login Route
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    print("🔥 Login route accessed!")  # Debugging print
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            return render_template("login.html", error="Please provide both email and password.")

        print(f"🔍 Attempting login for: {email}")  # Debugging

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        conn.close()

        # ✅ Check if user exists & validate password correctly
        if user and check_password_hash(user["password"], password):
            print("✅ Login successful!")
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session.permanent = True  # Keep session active

            # ✅ Redirect based on user role
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))  # Ensure correct mapping
            elif user["role"] == "doctor":
                return redirect(url_for("doctor_dashboard"))  # Ensure correct mapping
            else:
                return redirect(url_for("patient_dashboard"))  # Ensure correct mapping

        print("❌ Invalid login attempt!")  # Debugging
        return render_template("login.html", error="Invalid credentials. Don't have an account? <a href='{}'>Sign Up</a>".format(url_for('auth.signup')))

    return render_template("login.html")


# ✅ Signup Route
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    print("🔥 Signup route accessed!")  # Debugging print
    
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        if not name or not email or not password or not role:
            return render_template("signup.html", error="All fields are required.")

        print(f"📝 Signup attempt for: {email} as {role}")  # Debugging

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # ✅ Check if user already exists
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                print("❌ Email already registered!")
                return render_template("signup.html", error="Email already registered. Please log in.")

            # ✅ Hash the password before storing it
            hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

            # ✅ Insert into `users` table
            cursor.execute(
                "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                (name, email, hashed_password, role),
            )
            conn.commit()

            # ✅ Handle different roles
            cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
            user_id = cursor.fetchone()["id"]

            if role == "patient":
                patient_id = request.form.get("patient_id")
                gender = request.form.get("gender")
                date_of_birth = request.form.get("date_of_birth")
                age = request.form.get("age")
                height = request.form.get("height")
                weight = request.form.get("weight")
                medical_history = request.form.get("medical_history")

                cursor.execute(
                    """INSERT INTO patients 
                    (user_id, patient_id, gender, date_of_birth, age, height, weight, medical_history) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (user_id, patient_id, gender, date_of_birth, age, height, weight, medical_history),
                )

            elif role == "doctor":
                specialization = request.form.get("specialization")
                license_number = request.form.get("license_number")

                cursor.execute(
                    "INSERT INTO doctors (user_id, specialization, license_number) VALUES (%s, %s, %s)",
                    (user_id, specialization, license_number),
                )

            print("✅ Signup successful! Redirecting to login.")
            conn.commit()
            return redirect(url_for("auth.login"))

        except Exception as e:
            print(f"❌ Error in signup: {e}")  # Debugging
            return render_template("signup.html", error=f"Error: {str(e)}")

        finally:
            conn.close()

    return render_template("signup.html")


# ✅ Logout Route
@auth_bp.route("/logout")
def logout():
    session.clear()  # ✅ Clears session data
    return redirect(url_for("auth.login"))  # ✅ Redirects to login page

