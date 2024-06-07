from .. import db
from ..models import Instructor  # Assuming you have a model for Instructor

def create_instructor(data):
    new_instructor = Instructor(**data)
    db.session.add(new_instructor)
    db.session.commit()
    return new_instructor

def update_instructor(instructor_id, data):
    instructor = Instructor.query.get(instructor_id)
    if instructor:
        for key, value in data.items():
            setattr(instructor, key, value)
        db.session.commit()
    return instructor

def delete_instructor(instructor_id):
    instructor = Instructor.query.get(instructor_id)
    if instructor:
        db.session.delete(instructor)
        db.session.commit()
