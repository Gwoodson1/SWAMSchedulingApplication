from .. import db
from ..models import Instructor

def create_instructor(data):
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    if not username or not password or not name:
        raise ValueError("Username, password, and name are required")

    new_instructor = Instructor(username=username, password=password, name=name)
    db.session.add(new_instructor)
    db.session.commit()
    return new_instructor.to_dict()

def read_instructor(instructor_id):
    instructor = db.session.get(Instructor, instructor_id)
    return instructor.to_dict() if instructor else None

def get_all_instructors():
    return [instructor.to_dict() for instructor in Instructor.query.all()]

def update_instructor(instructor_id, data):
    instructor = db.session.get(Instructor, instructor_id)
    if instructor:
        for key, value in data.items():
            setattr(instructor, key, value)
        db.session.commit()
    return instructor.to_dict() if instructor else None

def delete_instructor(instructor_id):
    instructor = db.session.get(Instructor, instructor_id)
    if instructor:
        db.session.delete(instructor)
        db.session.commit()
    return instructor.to_dict() if instructor else None

def update_instructor_by_username(username, data):
    instructor = Instructor.query.filter_by(username=username).first()
    if instructor:
        if 'password' in data:
            instructor.password = data['password']
        if 'name' in data:
            instructor.name = data['name']
        db.session.commit()
    return instructor.to_dict() if instructor else None
