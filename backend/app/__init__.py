from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../../frontend/build', static_url_path='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create sql tables for our data models

    from .views import api_bp  # Import blueprint here
    app.register_blueprint(api_bp, url_prefix='/api')  # Register blueprint

    return app