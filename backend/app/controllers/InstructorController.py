from .. import db
import pandas as pd
from ..models import Instructor, Lesson, InstructorLesson

def create_instructor(data):
    # Check if a instructor with the same name already exists
    existing_instructor = Instructor.query.filter_by(name=data.get('name')).first()
    
    if existing_instructor:
        raise ValueError(f"Swimmer with the name {data.get('name')} already exists.")
    
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    gender = data.get('gender')
    languages = data.get('languages')
    swimmer_preference = data.get('swimmer_preference')
    assigned_child_preference = data.get('assigned_child_preference')
    taught_lessons = data.get('taught_lessons')
    worked_with_disabilities = data.get('worked_with_disabilities')
    relevant_experience = data.get('relevant_experience')
    expectations = data.get('expectations')
    additional_info = data.get('additional_info')
    previous_swam_lessons = data.get('previous_swam_lessons')

    lesson_ids = data.get('lesson_ids', [])

    if not name:
        raise ValueError("Name is required")

    new_instructor = Instructor(username=username, password=password, name=name, gender=gender, languages=languages,
                                swimmer_preference=swimmer_preference, assigned_child_preference=assigned_child_preference,
                                taught_lessons=taught_lessons, worked_with_disabilities=worked_with_disabilities,
                                relevant_experience=relevant_experience, expectations=expectations, additional_info=additional_info,
                                previous_swam_lessons=previous_swam_lessons)
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

def insert_instructors_into_db(data):
    for record in data:
        # Check if the instructor name is present; if not, skip this row
        name = str(record.get("Preferred Name")) + " " + str(record.get("Last Name"))
        if not name or name == "nan nan":
            print(f"Skipping row with missing instructor name: {record}")
            continue
        
        swimmer_preference = record.get("If yes, would you like to be paired with your previous swimmer")
        if not swimmer_preference or pd.isna(swimmer_preference):
            swimmer_preference = 'N/A'

        instructor_data = {
            'name': name.title(),
            'gender': record.get("What is your gender"),
            'languages': record.get("Do you speak any other languages fluently enough to teach a lesson in it?"),
            'swimmer_preference': swimmer_preference,
            'assigned_child_preference': record.get('Would you prefer to have an assigned child or to be a substitute instructor? Please note that because we believe consistency is important if you plan on missing more than 1 lesson, you should select to be a substitute only.'),
            'taught_lessons': record.get('Have you previously taught swimming lessons?'),
            'worked_with_disabilities': record.get('Have you previously worked with individuals with disabilities?'),
            'relevant_experience': record.get('If you answered yes to either of the previous two questions, please elaborate on your experience.'),
            'expectations': record.get('What are you looking forward to most about volunteering with S.W.A.M.?'),
            'additional_info': record.get('Is there anything else you would like us to know?'),
            'previous_swam_lessons': record.get('How many total S.W.A.M. Semesters have you instructed in the past?'),
        }
        
        try:
            create_instructor(instructor_data)
        except Exception as e:
            print(f"Failed to insert record: {record} due to error: {e}")
            continue