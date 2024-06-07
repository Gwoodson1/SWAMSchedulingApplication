# app/controllers/LessonController.py
from .. import db
from ..models import Lesson  # Assuming you have a model for Lesson

def create_lesson(data):
    new_lesson = Lesson(**data)
    db.session.add(new_lesson)
    db.session.commit()
    return new_lesson

def update_lesson(lesson_id, data):
    lesson = Lesson.query.get(lesson_id)
    if lesson:
        for key, value in data.items():
            setattr(lesson, key, value)
        db.session.commit()
    return lesson

def delete_lesson(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if lesson:
        db.session.delete(lesson)
        db.session.commit()
