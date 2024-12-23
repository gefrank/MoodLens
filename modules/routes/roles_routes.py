from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from modules.services.roles_service import get_roles, add_role, assign_role_to_user, get_user_roles
from forms import RoleForm, UserRoleForm

roles_routes = Blueprint("roles", __name__)

@roles_routes.route("/roles", methods=["GET", "POST"])
@login_required
def manage_roles():
    form = RoleForm()
    if form.validate_on_submit():
        success = add_role(name=form.name.data, description=form.description.data)
        if success:
            flash("Role added successfully!", "success")
        else:
            flash("Role already exists or failed to add.", "danger")
        return redirect(url_for("roles.manage_roles"))

    roles = get_roles()
    return render_template("roles.html", form=form, roles=roles)


@roles_routes.route("/user_roles", methods=["GET", "POST"])
@login_required
def manage_user_roles():
    form = UserRoleForm()
    form.role_id.choices = [(role.id, role.name) for role in get_roles()]

    if form.validate_on_submit():
        success = assign_role_to_user(user_id=form.user_id.data, role_id=form.role_id.data)
        if success:
            flash("Role assigned successfully!", "success")
        else:
            flash("Failed to assign role. Check user and role IDs.", "danger")
        return redirect(url_for("roles.manage_user_roles"))

    user_roles = get_user_roles()
    return render_template("user_roles.html", form=form, user_roles=user_roles)
