from flask import Flask
from modules.routes.main_routes import main_routes
from modules.routes.dashboard_routes import dashboard_routes
from modules.routes.export_routes import export_routes

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(main_routes)
app.register_blueprint(dashboard_routes, url_prefix="/dashboard")
app.register_blueprint(export_routes, url_prefix="/export")

if __name__ == "__main__":
    app.run(debug=True)
