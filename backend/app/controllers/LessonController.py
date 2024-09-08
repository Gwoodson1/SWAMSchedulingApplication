import random
from .. import db
from collections import defaultdict
from ..models import Lesson, Instructor, Swimmer, InstructorLesson, SwimmerLesson

def create_lesson(data):
    instructor_ids = data.pop('instructor_ids', [])
    swimmer_ids = data.pop('swimmer_ids', [])

    new_lesson = Lesson(**data)
    db.session.add(new_lesson)
    db.session.commit()

    # Associate instructors with the lesson
    for instructor_id in instructor_ids:
        instructor = db.session.get(Instructor, instructor_id)
        if instructor:
            new_lesson.instructors.append(InstructorLesson(instructor=instructor))

    # Associate swimmers with the lesson
    for swimmer_id in swimmer_ids:
        swimmer = db.session.get(Swimmer, swimmer_id)
        if swimmer:
            new_lesson.swimmers.append(SwimmerLesson(swimmer=swimmer))

    db.session.commit()

    return new_lesson.to_dict()

def read_lesson(lesson_id):
    lesson = db.session.get(Lesson, lesson_id)
    if lesson:
        lesson_dict = lesson.to_dict()
        lesson_dict['instructors'] = [il.instructor_id for il in lesson.instructors]
        lesson_dict['swimmers'] = [sl.swimmer_id for sl in lesson.swimmers]
        return lesson_dict
    return None

def get_all_lessons():
    lessons = Lesson.query.all()
    all_lessons = []
    for lesson in lessons:
        lesson_dict = lesson.to_dict()
        lesson_dict['instructors'] = [il.instructor_id for il in lesson.instructors]
        lesson_dict['swimmers'] = [sl.swimmer_id for sl in lesson.swimmers]
        all_lessons.append(lesson_dict)
    return all_lessons

def update_lesson(lesson_id, data):
    lesson = db.session.get(Lesson, lesson_id)
    if lesson:
        instructor_ids = data.pop('instructor_ids', [])
        swimmer_ids = data.pop('swimmer_ids', [])

        for key, value in data.items():
            setattr(lesson, key, value)
        
        # Update instructors associations
        lesson.instructors.clear()
        for instructor_id in instructor_ids:
            instructor = db.session.get(Instructor, instructor_id)
            if instructor:
                lesson.instructors.append(InstructorLesson(instructor=instructor))
        
        # Update swimmers associations
        lesson.swimmers.clear()
        for swimmer_id in swimmer_ids:
            swimmer = db.session.get(Swimmer, swimmer_id)
            if swimmer:
                lesson.swimmers.append(SwimmerLesson(swimmer=swimmer))

        db.session.commit()

    return lesson.to_dict() if lesson else None

def delete_lesson(lesson_id):
    lesson = db.session.get(Lesson, lesson_id)
    if lesson:
        db.session.delete(lesson)
        db.session.commit()
    return lesson.to_dict() if lesson else None

import random
from collections import defaultdict
from ..models import Lesson, SwimmerLesson, Swimmer
from .. import db

def assign_times_to_lessons():
    # Define the available time slots
    time_slots = ['9:30 - 10:00', '10:00 - 10:30', '10:30 - 11:00', '11:00 - 11:30']
    
    # Track the distribution of time slots
    time_slot_distribution = defaultdict(int)
    
    # Fetch all lessons and their related swimmers
    lessons = Lesson.query.join(SwimmerLesson).join(Swimmer).all()
    
    # Shuffle the list of lessons to introduce randomness
    random.shuffle(lessons)

    for lesson in lessons:
        # Get the swimmer object associated with this lesson
        swimmer_lesson = lesson.swimmers[0]  # Assuming one swimmer per lesson
        swimmer = swimmer_lesson.swimmer  # Access the swimmer object
        available_times = swimmer.availabilities.split(', ')  # Get swimmer's availabilities

        # Find the least occupied time slot that the swimmer is available for
        selected_time_slot = None
        min_assigned = float('inf')
        
        # Randomly shuffle available times to vary assignments within each swimmer
        random.shuffle(available_times)

        for time_slot in available_times:
            if time_slot in time_slots and time_slot_distribution[time_slot] < min_assigned:
                selected_time_slot = time_slot
                min_assigned = time_slot_distribution[time_slot]

        # Assign the selected time slot if found
        if selected_time_slot:
            lesson.lesson_time = selected_time_slot
            time_slot_distribution[selected_time_slot] += 1

    # Commit the changes to the database
    db.session.commit()