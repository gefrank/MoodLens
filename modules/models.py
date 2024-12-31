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
    current_model = db.Column(db.String(255), nullable=True)  

    def __init__(self, Input_Text, Sentiment, Confidence, current_model, Timestamp=None):
        self.Input_Text = Input_Text
        self.Sentiment = Sentiment.upper() 
        self.Confidence = Confidence
        self.current_model = current_model  # Set current model
        self.Timestamp = Timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"<SentimentLog {self.Input_Text[:20]}... - {self.Sentiment}>"
    
    
class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    last_interaction = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationship to User
    user = db.relationship('User', backref=db.backref('chat_sessions', lazy=True))
    # Relationship to messages
    messages = db.relationship('ChatMessage', backref='session', lazy=True)


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_sessions.id'), nullable=False)
    message_type = db.Column(db.String(10), nullable=False)  # 'user' or 'bot'
    content = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20), nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)

    
class AppConfig(db.Model):
    __tablename__ = 'app_config'
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<AppConfig key={self.key} value={self.value}>"    
