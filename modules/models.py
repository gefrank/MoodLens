from .utilities.database import db
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()

# Association table for many-to-many relationship
class UserRole(db.Model):
    __tablename__ = 'user_roles'

    # Composite primary key using user_id and role_id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)

    def __repr__(self):
        return f"<UserRole user_id={self.user_id} role_id={self.role_id}>"


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    # Define a many-to-many relationship with Role
    roles = db.relationship(
        'Role',
        secondary='user_roles',  # Reference the user_roles table
        backref=db.backref('users', lazy='dynamic')  # Allows querying users from a role
    )


    def has_role(self, role_name):
        if not self.roles:  # Handle None or empty list
            return False
        return any(role.name == role_name for role in self.roles)
    

    @staticmethod
    def hash_password(password):
        """Generate a hashed password."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify a hashed password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f"<Role {self.name}>"


class SentimentLog(db.Model):
    __tablename__ = "sentiment_logs"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key
    Timestamp = db.Column(db.Text, nullable=False)
    Input_Text = db.Column(db.Text, nullable=False)
    Sentiment = db.Column(db.Text, nullable=False)
    Confidence = db.Column(db.Float, nullable=False)

    def __init__(self, Input_Text, Sentiment, Confidence, Timestamp=None):
        self.Input_Text = Input_Text
        self.Sentiment = Sentiment
        self.Confidence = Confidence
        self.Timestamp = Timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"<SentimentLog {self.Input_Text[:20]}... - {self.Sentiment}>"
