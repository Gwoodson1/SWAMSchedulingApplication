from .. import db
from ..models import Swimmer, Parent, ParentSwimmer

def create_swimmer(data):
    parent_id = data.get('parent_id')
    new_swimmer = Swimmer(
        name=data.get('name'),
        level=data.get('level'),
        special_needs=data.get('special_needs')
    )
    db.session.add(new_swimmer)
    db.session.commit()

    if parent_id:
        parent = db.session.get(Parent, parent_id)
        if parent:
            parent_swimmer = ParentSwimmer(parent_id=parent_id, swimmer_id=new_swimmer.id)
            db.session.add(parent_swimmer)
            db.session.commit()

    return new_swimmer.to_dict()

def read_swimmer(swimmer_id):
    swimmer = db.session.get(Swimmer, swimmer_id)
    if swimmer:
        swimmer_dict = swimmer.to_dict()
        parent_swimmers = ParentSwimmer.query.filter_by(swimmer_id=swimmer.id).all()
        swimmer_dict['parents'] = [ps.parent_id for ps in parent_swimmers]
        return swimmer_dict
    return None

def get_all_swimmers():
    swimmers = Swimmer.query.all()
    all_swimmers = []
    for swimmer in swimmers:
        swimmer_dict = swimmer.to_dict()
        parent_swimmers = ParentSwimmer.query.filter_by(swimmer_id=swimmer.id).all()
        swimmer_dict['parents'] = [ps.parent_id for ps in parent_swimmers]
        all_swimmers.append(swimmer_dict)
    return all_swimmers

def update_swimmer(swimmer_id, data):
    swimmer = db.session.get(Swimmer, swimmer_id)
    if swimmer:
        for key, value in data.items():
            setattr(swimmer, key, value)
        db.session.commit()

        # Update parent association if provided
        if 'parent_id' in data:
            parent_id = data['parent_id']
            # Delete existing associations
            ParentSwimmer.query.filter_by(swimmer_id=swimmer.id).delete()
            # Add new association
            parent = db.session.get(Parent, parent_id)
            if parent:
                parent_swimmer = ParentSwimmer(parent_id=parent_id, swimmer_id=swimmer.id)
                db.session.add(parent_swimmer)
                db.session.commit()

        return swimmer.to_dict()
    return None

def delete_swimmer(swimmer_id):
    swimmer = db.session.get(Swimmer, swimmer_id)
    if swimmer:
        # Delete associated ParentSwimmer records
        ParentSwimmer.query.filter_by(swimmer_id=swimmer.id).delete()
        db.session.delete(swimmer)
        db.session.commit()
    return swimmer.to_dict() if swimmer else None

