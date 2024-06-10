# app/controllers/LessonController.py
from .. import db
from ..models import Lesson  # Assuming you have a model for Lesson

def create_lesson(data):
    new_lesson = Lesson(**data)
    db.session.add(new_lesson)
    db.session.commit()
    return new_lesson

def read_lesson(lesson_id):
    lesson = db.session.get(Lesson, lesson_id)
    return lesson
    
def read_lessons():
    list_of_lessons = [o for o in db.session.query(Lesson).all()]
    return list_of_lessons

def update_lesson(lesson_id, data):
    lesson = db.session.get(Lesson, lesson_id)
    if lesson:
        for key, value in data.items():
            setattr(lesson, key, value)
        db.session.commit()
    return lesson

def delete_lesson(lesson_id):
    lesson = db.session.get(Lesson, lesson_id)
    if lesson:
        db.session.delete(lesson)
        db.session.commit()
