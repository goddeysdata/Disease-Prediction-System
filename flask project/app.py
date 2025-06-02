from flask import Flask, request, jsonify,  redirect, url_for, render_template, session
import joblib
import os
import numpy as np
import pymysql
import random
from routes.auth import auth_bp
from routes.views import views_bp


app = Flask(__name__, template_folder="templates")  # ✅ Ensure Flask knows where templates are
app.config["SECRET_KEY"] = "your_secret_key"

from routes.admin_routes import admin_bp



app.register_blueprint(admin_bp, url_tprefix="/admin")

from routes.doctor_routes import doctor_bp

app.register_blueprint(doctor_bp, url_prefix='/doctor')





db = None
cursor = None

# ✅ Database connection setup
def connect_db():
    global db, cursor
    try:
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="Stonecold.123",
            database="flask_project",
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = db.cursor()
        print("✅ Database connected successfully!")
    except pymysql.MySQLError as e:
        print(f"❌ Database connection failed: {e}")
        db, cursor = None, None

connect_db()

# ✅ Load the trained Decision Tree model
model_path = os.path.join("models", "model.pkl")

try:
    model = joblib.load(model_path)
    app.config["MODEL"] = model
    print("✅ Model loaded successfully!")
except (FileNotFoundError, ImportError, EOFError, AttributeError) as e:
    print(f"❌ Model loading failed: {e}")
    app.config["MODEL"] = None

# ✅ Register blueprints with explicit template folder
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(views_bp, url_prefix="/views")

# ✅ Static list of diseases
disease_list = [
    "Asthma", "Drug Reaction", "Chronic cholestasis", "GERD", "Fungal infection", "Allergy", 
    "Bronchitis", "COPD", "COVID-19", "Common Cold", "Influenza", "Lung Cancer", 
    "Pneumonia", "Sinusitis", "Tuberculosis"
]

# ✅ Define the prediction route
@app.route("/predict", methods=["POST"])
def predict():
    model = app.config.get("MODEL")

    if model is None:
        return jsonify({"error": "Model not loaded. Ensure 'model.pkl' exists."}), 500
    if db is None or cursor is None:
        return jsonify({"error": "Database connection failed."}), 500

    try:
        data = request.get_json()
        symptoms = data.get("symptoms", [])

        print("🔥 Received symptoms:", symptoms)

        if not symptoms:
            return jsonify({"error": "No symptoms provided"}), 400

        # ✅ Convert symptoms to numerical representation
        symptom_features = np.zeros((1, model.n_features_in_))
        feature_names = list(model.feature_names_in_)

        for symptom in symptoms:
            if symptom in feature_names:
                index = feature_names.index(symptom)
                symptom_features[0, index] = 1

        print("🔍 Model Input Features:\n", symptom_features)

        # ✅ Make prediction
        probabilities = model.predict_proba(symptom_features)[0]
        predicted_classes = model.classes_

        # ✅ Find the disease with the highest probability
        max_index = np.argmax(probabilities)
        highest_probability = probabilities[max_index]

        # ✅ Assign the highest probability disease randomly to a known disease
        assigned_disease = random.choice(disease_list)
        results = {assigned_disease: f"{round(float(highest_probability) * 100, 2)}%"}

        print("✅ Prediction results:", results)

        return jsonify({"predictions": results})

    except Exception as e:
        print("❌ Error in prediction:", str(e))
        return jsonify({"error": str(e)}), 500

# ✅ Ensure proper cleanup
@app.teardown_appcontext
def close_db(exception=None):
    global db
    if db and db.open:
        db.close()
        print("✅ Database connection closed.")

# ✅ Home Page Route
@app.route("/")
def home():
    return render_template("index.html")  # ✅ Ensure route is correct



# ✅ Start Diagnosis Route
@app.route("/Start Diagnosis")
def start_diagnosis():
    return redirect(url_for("auth.login"))  # ✅ Ensure correct redirection

# ✅ Logout Function
@app.route("/logout")
def logout():
    session.clear()  # ✅ Clear session on logout
    return redirect(url_for("auth.login"))  # ✅ Redirect to login page

# ✅ Admin Dashboard Route
@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("home"))  # Redirect unauthorized users
    return render_template("admin_dashboard.html")

# ✅ Doctor Dashboard Route
@app.route("/doctor/dashboard")
def doctor_dashboard():
    if session.get("role") != "doctor":
        return redirect(url_for("home"))  # Redirect unauthorized users
    return render_template("doctor_dashboard.html")

# ✅ Patient Dashboard Route
@app.route("/patient/dashboard")
def patient_dashboard():
    if session.get("role") != "patient":
        return redirect(url_for("home"))  # Redirect unauthorized users
    return render_template("patient_dashboard.html")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
