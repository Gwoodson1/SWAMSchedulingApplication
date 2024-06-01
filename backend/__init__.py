# app/__init__.py
from flask import Flask
from app.views import api_bp

def create_app():
    app = Flask(__name__)
    
    # Register Blueprints
    app.register_blueprint(api_bp)

    # Additional app configuration and initialization
    return app
