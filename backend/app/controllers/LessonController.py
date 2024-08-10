from .. import db
from ..models import Lesson

def create_lesson(data):
    new_lesson = Lesson(**data)
    db.session.add(new_lesson)
    db.session.commit()
    return new_lesson.to_dict()

def read_lesson(lesson_id):
    lesson = db.session.get(Lesson, lesson_id)
    return lesson.to_dict() if lesson else None

def get_all_lessons():
    return [lesson.to_dict() for lesson in Lesson.query.all()]

def update_lesson(lesson_id, data):
    lesson = db.session.get(Lesson, lesson_id)
    if lesson:
        for key, value in data.items():
            setattr(lesson, key, value)
        db.session.commit()
    return lesson.to_dict() if lesson else None

def delete_lesson(lesson_id):
    lesson = db.session.get(Lesson, lesson_id)
    if lesson:
        db.session.delete(lesson)
        db.session.commit()
    return lesson.to_dict() if lesson else None
