from .. import db
from ..models import Instructor, Lesson, InstructorLesson

def create_instructor(data):
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    lesson_ids = data.get('lesson_ids', [])

    if not username or not password or not name:
        raise ValueError("Username, password, and name are required")

    new_instructor = Instructor(username=username, password=password, name=name)
    db.session.add(new_instructor)
    db.session.commit()

    # Associate lessons with the instructor
    for lesson_id in lesson_ids:
        lesson = db.session.get(Lesson, lesson_id)
        if lesson:
            new_instructor.lessons.append(InstructorLesson(lesson=lesson))

    db.session.commit()

    return new_instructor.to_dict()

def read_instructor(instructor_id):
    instructor = db.session.get(Instructor, instructor_id)
    if instructor:
        instructor_dict = instructor.to_dict()
        instructor_dict['lessons'] = [il.lesson_id for il in instructor.lessons]
        return instructor_dict
    return None

def get_all_instructors():
    instructors = Instructor.query.all()
    all_instructors = []
    for instructor in instructors:
        instructor_dict = instructor.to_dict()
        instructor_dict['lessons'] = [il.lesson_id for il in instructor.lessons]
        all_instructors.append(instructor_dict)
    return all_instructors

def update_instructor(instructor_id, data):
    instructor = db.session.get(Instructor, instructor_id)
    if instructor:
        lesson_ids = data.pop('lesson_ids', [])

        for key, value in data.items():
            setattr(instructor, key, value)
        
        # Update lessons associations
        instructor.lessons.clear()
        for lesson_id in lesson_ids:
            lesson = db.session.get(Lesson, lesson_id)
            if lesson:
                instructor.lessons.append(InstructorLesson(lesson=lesson))

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
        lesson_ids = data.pop('lesson_ids', [])

        for key, value in data.items():
            setattr(instructor, key, value)
        
        # Update lessons associations
        instructor.lessons.clear()
        for lesson_id in lesson_ids:
            lesson = db.session.get(Lesson, lesson_id)
            if lesson:
                instructor.lessons.append(InstructorLesson(lesson=lesson))

        db.session.commit()

    return instructor.to_dict() if instructor else None
