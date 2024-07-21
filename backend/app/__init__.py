from flask import Flask, jsonify
from flask_cors import CORS
from backend.app.models import db

def create_app():
    app = Flask(__name__, static_folder='../../frontend/build', static_url_path='/')

    # Enable CORS for the entire app
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Configuration for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the database with the app
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Import and register the API blueprint
    from .views import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
