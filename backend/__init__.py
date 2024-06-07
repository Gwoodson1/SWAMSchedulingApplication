# app/__init__.py
from flask import Flask
from backend.app.views import api_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register Blueprints
    app.register_blueprint(api_bp)

    # Additional app configuration and initialization
    return app
