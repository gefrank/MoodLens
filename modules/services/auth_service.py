from modules.models import User
from modules.utilities.database import db

def create_user(username, password):
    """
    Create a new user with the provided username and hashed password.
    """
    if User.query.filter_by(username=username).first():
        return None  # Username already exists
    user = User(username=username, password_hash=User.hash_password(password))
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_username(username):
    """
    Fetch a user by their username.
    """
    return User.query.filter_by(username=username).first()
