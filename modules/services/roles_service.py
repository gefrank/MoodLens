from modules.utilities.database import db
from modules.models import Role, UserRole

def get_roles():
    """Fetch all roles from the database."""
    return Role.query.all()

def add_role(name, description):
    """Add a new role to the database."""
    if Role.query.filter_by(name=name).first():
        return False  # Role already exists
    new_role = Role(name=name, description=description)
    db.session.add(new_role)
    db.session.commit()
    return True

def assign_role_to_user(user_id, role_id):
    """Assign a role to a user."""
    if not Role.query.get(role_id):
        return False  # Role does not exist
    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.session.add(user_role)
    db.session.commit()
    return True

def get_user_roles():
    """Fetch all user-role relationships."""
    return UserRole.query.all()
