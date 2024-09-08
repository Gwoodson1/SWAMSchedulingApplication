from .. import db
from ..models import Parent, Swimmer, ParentSwimmer

def create_parent(data):
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    children_ids = data.get('children_ids', [])

    new_parent = Parent(username=username, password=password, name=name)

    # Add children associations using backreference
    for child_id in children_ids:
        child = db.session.get(Swimmer, child_id)
        if child:
            new_parent.swimmers.append(ParentSwimmer(swimmer=child))

    db.session.add(new_parent)
    db.session.commit()

    return new_parent.to_dict()

def read_parent(parent_id):
    parent = db.session.get(Parent, parent_id)
    if parent:
        parent_dict = parent.to_dict()
        # Use the backref to get the children directly
        parent_dict['children'] = [child.swimmer_id for child in parent.swimmers]
        return parent_dict
    return None

def get_all_parents():
    parents = Parent.query.all()
    all_parents = []
    for parent in parents:
        parent_dict = parent.to_dict()
        # Use the backref to get the children directly
        parent_dict['children'] = [child.swimmer_id for child in parent.swimmers]
        all_parents.append(parent_dict)
    return all_parents

def update_parent(parent_id, data):
    parent = db.session.get(Parent, parent_id)
    if parent:
        for key, value in data.items():
            setattr(parent, key, value)
        db.session.commit()

        # Update children associations if provided
        if 'children_ids' in data:
            # Clear existing associations
            parent.swimmers.clear()
            # Add new associations
            for child_id in data['children_ids']:
                child = db.session.get(Swimmer, child_id)
                if not child:
                    raise ValueError(f"Swimmer with ID {child_id} does not exist")
                parent.swimmers.append(ParentSwimmer(swimmer=child))
            db.session.commit()

        return parent.to_dict()
    return None

def delete_parent(parent_id):
    parent = db.session.get(Parent, parent_id)
    if parent:
        db.session.delete(parent)
        db.session.commit()
    return parent.to_dict() if parent else None

def update_parent_by_username(username, data):
    parent = Parent.query.filter_by(username=username).first()
    if parent:
        for key, value in data.items():
            setattr(parent, key, value)
        db.session.commit()
        return parent.to_dict()
    return None