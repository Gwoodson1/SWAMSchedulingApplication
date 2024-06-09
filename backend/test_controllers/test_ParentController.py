import pytest
import backend.app.controllers.SwimmerController as Swimmer
import backend.app.controllers.ParentController as Parent

@pytest.fixture
def test_swimmer_data():
    return {
        'id': 23, 
        'name': 'Khalil Omar', 
        'level': 3, 
        'special_needs': 'ADHD, ASD', 
        'parent_id': 45
    }

@pytest.fixture
def test_parent_data():
    return {
        'id': 45,
        'username': 'MOmar@gmail.com',
        'password': 'Kalil123',
        'name': 'Mohammed Omar',
    }

'''
@pytest.fixture
def test_parent2_data():
    return {
        'id': 41,
        'name': 'Sarah James',
        'children': 'Ben James', 
    }

@pytest.fixture
def test_updated_parent_data():
    return {
        'id': 45,
        'name': 'Mohammed Omar II',
        'children': 'Khalil Omar', 
    }

    '''

def test_create_parent(app, test_parent_data, test_swimmer_data):
    with app.app_context():
        new_parent = Parent.create_parent(test_parent_data)
        swimmer = Swimmer.create_swimmer(test_swimmer_data)
        new_parent.children = [swimmer]

        assert new_parent.id == 45
        assert new_parent.username == 'MOmar@gmail.com'
        assert new_parent.password == 'Kalil123'
        assert new_parent.name == 'Mohammed Omar'
        assert new_parent.children == [swimmer]

'''
def test_read_parent(app, test_parent_data):
    with app.app_context():
        Parent.create_parent(test_parent_data)
        parent = Parent.read_parent(45)
        assert parent.id == 45
        assert parent.name == 'Mohammed Omar'
        assert parent.children == 'Khalil Omar'


def test_get_parents(app, test_parent_data, test_parent2_data):
    with app.app_context():
        parent = Parent.create_parent(test_parent_data)
        parent2 = Parent.create_parent(test_parent2_data)
        list = Parent.read_parents()
        
        assert list == [parent, parent2]
        parent3 = list[1]
        assert parent3.name == 'Sarah James'


#tests updating information on a specific parent based on ID
def test_update_parent(app, test_parent_data, test_updated_parent_data):
    with app.app_context():
        Parent.create_parent(test_parent_data)
        updated_parent = Parent.update_parent(45, test_updated_parent_data)
        assert updated_parent.id == 45
        assert updated_parent.name == 'Mohammed Omar II'
        assert updated_parent.children == 'Khalil Omar'

#tests deleting a parent based on ID
def test_delete_parent(app, test_parent_data):
    with app.app_context():
        Parent.create_parent(test_parent_data)
        Parent.delete_parent(45)
        deleted_parent = Parent.read_parent(45)
        assert deleted_parent is None
        '''