# app/controllers/SwimmerController.py
from .. import db
from ..models import Swimmer  # Assuming you have a model for Swimmer

def create_swimmer(data):
    new_swimmer = Swimmer(**data)
    db.session.add(new_swimmer)
    db.session.commit()
    return new_swimmer

def update_swimmer(swimmer_id, data):
    swimmer = Swimmer.query.get(swimmer_id)
    if swimmer:
        for key, value in data.items():
            setattr(swimmer, key, value)
        db.session.commit()
    return swimmer

def delete_swimmer(swimmer_id):
    swimmer = Swimmer.query.get(swimmer_id)
    if swimmer:
        db.session.delete(swimmer)
        db.session.commit()
