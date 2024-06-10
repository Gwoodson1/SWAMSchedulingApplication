# app/controllers/SwimmerController.py
from .. import db
from ..models import Swimmer 

def create_swimmer(data):
    new_swimmer = Swimmer(**data)
    db.session.add(new_swimmer)
    db.session.commit()
    return new_swimmer

def read_swimmer(swimmer_id):
    swimmer = db.session.get(Swimmer, swimmer_id)
    return swimmer
    
def read_swimmers():
    list_of_swimmers = [o for o in db.session.query(Swimmer).all()]
    return list_of_swimmers
    

def update_swimmer(swimmer_id, data):
    swimmer = db.session.get(Swimmer, swimmer_id)
    if swimmer:
        for key, value in data.items():
            setattr(swimmer, key, value)
        db.session.commit()
    return swimmer

def delete_swimmer(swimmer_id):
    swimmer = db.session.get(Swimmer, swimmer_id)
    if swimmer:
        db.session.delete(swimmer)
        db.session.commit()
