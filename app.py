import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from scraper import scrape_url
from storage import init_db, get_all_results, delete_result, create_user, get_user_by_email, update_result_status
from auth import login_manager, User

app = Flask(__name__, template_folder="templates")
app.secret_key = os.environ.get("SECRET_KEY", "scraper_secret_key_2024")
login_manager.init_app(app)
init_db()

@app.route("/")
def landing():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("landing.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = generate_password_hash(request.form.get("password"))
        if create_user(name, email, password):
            flash("Account ban gaya! Ab login karo.")
            return redirect(url_for("login"))
        flash("Yeh email pehle se registered hai.")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_data = get_user_by_email(email)
        if user_data and check_password_hash(user_data["password"], password):
            user = User(user_data["id"], user_data["name"], user_data["email"], user_data["password"])
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Email ya password galat hai.")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("landing"))

@app.route("/dashboard")
@login_required
def dashboard():
    results = get_all_results(current_user.id)
    return render_template("index.html", results=results, user=current_user)

@app.route("/scrape", methods=["POST"])
@login_required
def scrape():
    url = request.json.get("url")
    depth = int(request.json.get("depth", 1))
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    if not url.startswith("http"):
        url = "https://" + url
    result = scrape_url(url, depth=depth, user_id=current_user.id)
    return jsonify(result)

@app.route("/delete/<int:result_id>", methods=["DELETE"])
@login_required
def delete(result_id):
    delete_result(result_id, current_user.id)
    return jsonify({"status": "deleted"})

@app.route("/update/<int:result_id>", methods=["POST"])
@login_required
def update(result_id):
    status = request.json.get("status")
    notes = request.json.get("notes", "")
    update_result_status(result_id, status, notes, current_user.id)
    return jsonify({"status": "updated"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
