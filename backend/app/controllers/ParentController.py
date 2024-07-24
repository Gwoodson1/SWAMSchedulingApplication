# app/controllers/ParentController.py
from .. import db
from ..models import Parent

def create_parent(data):
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    if not username or not password or not name:
        raise ValueError("Username, password, and name are required")

    new_parent = Parent(username=username, password=password, name=name)
    db.session.add(new_parent)
    db.session.commit()
    return new_parent.to_dict()

def read_parent(parent_id):
    parent = db.session.get(Parent, parent_id)
    return parent.to_dict() if parent else None

def get_all_parents():
    return [parent.to_dict() for parent in Parent.query.all()]

def update_parent(parent_id, data):
    parent = db.session.get(Parent, parent_id)
    if parent:
        for key, value in data.items():
            setattr(parent, key, value)
        db.session.commit()
    return parent.to_dict() if parent else None

def delete_parent(parent_id):
    parent = db.session.get(Parent, parent_id)
    if parent:
        db.session.delete(parent)
        db.session.commit()
    return parent.to_dict() if parent else None

def update_parent_by_username(username, data):
    parent = Parent.query.filter_by(username=username).first()
    if parent:
        if 'password' in data:
            parent.password = data['password']
        if 'name' in data:
            parent.name = data['name']
        db.session.commit()
    return parent.to_dict() if parent else None
