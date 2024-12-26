from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from modules.models import User, Role, UserRole
from modules.utilities.database import db
from modules.forms import UserRoleForm

admin_routes = Blueprint("admin", __name__)

@admin_routes.route("/manage_users", methods=["GET", "POST"])
@login_required
def manage_users():
    form = UserRoleForm()
    form.user_id.choices = [(user.id, user.username) for user in User.query.all()]
    form.role_id.choices = [(role.id, role.name) for role in Role.query.all()]

    if form.validate_on_submit():
        user = User.query.get(form.user_id.data)
        role = Role.query.get(form.role_id.data)
        if role not in user.roles:
            user.roles.append(role)
            db.session.commit()
            flash("Role assigned successfully!", "success")
        else:
            flash("User already has this role.", "warning")

    users = User.query.all()
    return render_template("manage_users.html", form=form, users=users)
