import pytest
from backend.app import create_app
from backend.app.models import db

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    with app.app_context():
        db.create_all()  # Create the database tables
        yield app
        db.session.remove()
        db.drop_all()  # Drop the database tables after the test

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()