from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from modules.models import User, Role, UserRole, db

admin_routes = Blueprint("admin", __name__)

@admin_routes.route("/manage_users", methods=["GET", "POST"])
@login_required
def manage_users():
    if not current_user.has_role("Admin"):
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for("main.index"))

    users = User.query.all()
    roles = Role.query.all()

    if request.method == "POST":
        action = request.form.get("action")
        user_id = request.form.get("user_id")
        role_id = request.form.get("role_id")

        if action == "assign":
            user = User.query.get(user_id)
            role = Role.query.get(role_id)
            if user and role and role not in user.roles:
                user.roles.append(role)
                db.session.commit()
                flash(f"Role '{role.name}' assigned to {user.username}.", "success")
        elif action == "remove":
            user_role = UserRole.query.filter_by(user_id=user_id, role_id=role_id).first()
            if user_role:
                db.session.delete(user_role)
                db.session.commit()
                flash("Role removed successfully.", "success")
        elif action == "delete":
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                flash(f"User '{user.username}' deleted successfully.", "success")
        return redirect(url_for("admin.manage_users"))

    return render_template("manage_users.html", users=users, roles=roles)
