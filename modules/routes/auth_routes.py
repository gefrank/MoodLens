from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from modules.services.auth_service import get_user_by_username

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    # print("Login route accessed")  # Debug: Confirm the route is being hit
    if request.method == "POST":
        # print("POST request received")  # Debug: Confirm POST method
        username = request.form.get("username")
        password = request.form.get("password")
        # print(f"Username: {username}, Password: {password}")  # Debug: Show form data

        user = get_user_by_username(username)
        # print(f"User fetched: {user}")  # Debug: Confirm if user is found

        if user and user.verify_password(password):
            # print("Password verified successfully")  # Debug
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard.dashboard"))
        else:
            # print("Invalid username or password")  # Debug
            flash("Invalid username or password.", "danger")
            return redirect(url_for("auth.login"))

    return render_template("login.html")

@auth_routes.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
