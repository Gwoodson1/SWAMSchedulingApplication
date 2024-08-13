from .. import db
from ..models import Swimmer, Parent, ParentSwimmer, Lesson, SwimmerLesson

def create_swimmer(data):
    parent_ids = data.get('parent_ids', [])
    lesson_ids = data.get('lesson_ids', [])

    new_swimmer = Swimmer(
        name=data.get('name'),
        level=data.get('level'),
        special_needs=data.get('special_needs')
    )
    db.session.add(new_swimmer)
    db.session.commit()

    # Add parents
    for parent_id in parent_ids:
        parent = db.session.get(Parent, parent_id)
        if parent:
            parent_swimmer = ParentSwimmer(parent_id=parent.id, swimmer_id=new_swimmer.id)
            db.session.add(parent_swimmer)

    # Add lessons
    for lesson_id in lesson_ids:
        lesson = db.session.get(Lesson, lesson_id)
        if lesson:
            swimmer_lesson = SwimmerLesson(lesson_id=lesson.id, swimmer_id=new_swimmer.id)
            db.session.add(swimmer_lesson)

    db.session.commit()

    return new_swimmer.to_dict()

def read_swimmer(swimmer_id):
    swimmer = db.session.get(Swimmer, swimmer_id)
    if swimmer:
        swimmer_dict = swimmer.to_dict()
        # Use the backref to get the parents and lessons directly
        swimmer_dict['parents'] = [ps.parent_id for ps in swimmer.parents]
        swimmer_dict['lessons'] = [sl.lesson_id for sl in swimmer.lessons]
        return swimmer_dict
    return None

def get_all_swimmers():
    swimmers = Swimmer.query.all()
    all_swimmers = []
    for swimmer in swimmers:
        swimmer_dict = swimmer.to_dict()
        # Use the backref to get the parents and lessons directly
        swimmer_dict['parents'] = [ps.parent_id for ps in swimmer.parents]
        swimmer_dict['lessons'] = [sl.lesson_id for sl in swimmer.lessons]
        all_swimmers.append(swimmer_dict)
    return all_swimmers

def update_swimmer(swimmer_id, data):
    swimmer = db.session.get(Swimmer, swimmer_id)
    if swimmer:
        for key, value in data.items():
            setattr(swimmer, key, value)
        db.session.commit()

        # Update parent associations if provided
        if 'parent_ids' in data:
            parent_ids = data['parent_ids']
            # Clear existing associations
            swimmer.parents.clear()
            # Add new associations
            for parent_id in parent_ids:
                parent = db.session.get(Parent, parent_id)
                if parent:
                    swimmer.parents.append(ParentSwimmer(parent_id=parent.id, swimmer_id=swimmer.id))

        # Update lesson associations if provided
        if 'lesson_ids' in data:
            lesson_ids = data['lesson_ids']
            # Clear existing associations
            swimmer.lessons.clear()
            # Add new associations
            for lesson_id in lesson_ids:
                lesson = db.session.get(Lesson, lesson_id)
                if lesson:
                    swimmer.lessons.append(SwimmerLesson(lesson_id=lesson.id, swimmer_id=swimmer.id))

        db.session.commit()

        return swimmer.to_dict()
    return None

def delete_swimmer(swimmer_id):
    swimmer = db.session.get(Swimmer, swimmer_id)
    if swimmer:
        db.session.delete(swimmer)
        db.session.commit()
    return swimmer.to_dict() if swimmer else None