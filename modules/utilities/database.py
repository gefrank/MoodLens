import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    # Use Flask's instance_path to ensure the database is always created in the correct location
    db_path = os.path.join(app.instance_path, "moodlens.db")
    print("Database Path (absolute):", db_path)  # Debugging output

    # Ensure the instance directory exists
    os.makedirs(app.instance_path, exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
