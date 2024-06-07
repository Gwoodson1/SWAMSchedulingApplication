# app/controllers/ParentController.py
from .. import db
from ..models import Parent  # Assuming you have a model for Parent

def create_parent(data):
    new_parent = Parent(**data)
    db.session.add(new_parent)
    db.session.commit()
    return new_parent

def update_parent(parent_id, data):
    parent = Parent.query.get(parent_id)
    if parent:
        for key, value in data.items():
            setattr(parent, key, value)
        db.session.commit()
    return parent

def delete_parent(parent_id):
    parent = Parent.query.get(parent_id)
    if parent:
        db.session.delete(parent)
        db.session.commit()
