from flask import Blueprint, render_template, session, redirect, url_for, current_app  

views_bp = Blueprint("views", __name__, template_folder="../templates")  # Ensure correct template path

@views_bp.route("/")
def home():
    print("🔥 Home route accessed!")  # Debugging print
    try:
        return render_template("index.html")
    except Exception as e:
        print(f"❌ Error loading index.html: {e}")
        return "Template Not Found", 500

@views_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        print("🔒 User not logged in. Redirecting to login page...")
        return redirect(url_for("auth.login"))  # Ensure this route exists in auth.py
    
    user_role = session.get("role", "unknown")
    print(f"✅ Dashboard accessed by user with role: {user_role}")
    
    # Redirect to respective dashboards
    if user_role == "admin":
        return redirect(url_for("views.admin_dashboard"))
    elif user_role == "doctor":
        return redirect(url_for("views.doctor_dashboard"))
    else:
        return redirect(url_for("views.patient_dashboard"))  # Default patient dashboard

@views_bp.route("/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))
    return render_template("admin_dashboard.html")

@views_bp.route("/doctor/dashboard")
def doctor_dashboard():
    if "user_id" not in session or session.get("role") != "doctor":
        return redirect(url_for("auth.login"))
    return render_template("doctor_dashboard.html")

@views_bp.route("/patient/dashboard")
def patient_dashboard():
    if "user_id" not in session or session.get("role") != "patient":
        return redirect(url_for("auth.login"))
    return render_template("patient_dashboard.html")  # Default for patients
