# app/controllers/ParentController.py
from .. import db
from ..models import Parent

def create_parent(data):
    new_parent = Parent(**data)
    db.session.add(new_parent)
    db.session.commit()
    return new_parent

def read_parent(parent_id):
    parent = db.session.get(Parent, parent_id)
    return parent
    
def read_parents():
    list_of_parents = [o for o in db.session.query(Parent).all()]
    return list_of_parents

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
