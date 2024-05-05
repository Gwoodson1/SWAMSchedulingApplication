from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .views import init_views

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create sql tables for our data models

    init_views(app)  # Initialize views

    return app