import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db_path = os.path.join(app.instance_path, "moodlens.db")
    print("Database Path (absolute):", db_path)

    os.makedirs(app.instance_path, exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # Import models to register them with SQLAlchemy
    from modules.models import Role, UserRole
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
