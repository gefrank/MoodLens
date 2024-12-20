import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from modules.utilities.database import db, init_db
from modules.routes.auth_routes import auth_routes
from modules.routes.dashboard_routes import dashboard_routes
from modules.routes.main_routes import main_routes
from modules.routes.export_routes import export_routes

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Set the Flask secret key
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback-key")

# Initialize database
init_db(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"  # Redirect to login page if not logged in

# Register Blueprints
app.register_blueprint(main_routes)
app.register_blueprint(auth_routes, url_prefix="/auth")
app.register_blueprint(dashboard_routes, url_prefix="/dashboard")
app.register_blueprint(export_routes, url_prefix="/export")

# Create database tables
with app.app_context():
    db.create_all()

# User loader for Flask-Login
from modules.services.auth_service import User  # Ensure the User model is imported
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)
