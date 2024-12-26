from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from modules.services.auth_service import get_user_by_username, create_user
from modules.models import Role
from modules.utilities.database import db
from modules.forms import RegistrationForm  # Assuming the RegistrationForm is defined in forms.py

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = get_user_by_username(username)
        if user and user.verify_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for("auth.login"))

    return render_template("login.html")

@auth_routes.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

@auth_routes.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if the username already exists
        if get_user_by_username(username):
            flash("Username already exists. Please choose a different username.", "danger")
            return redirect(url_for("auth.register"))

        # Create a new user
        user = create_user(username, password)

        # Assign the default "Basic User" role
        basic_role = Role.query.filter_by(name="Basic User").first()
        if basic_role:
            user.roles.append(basic_role)

        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)
