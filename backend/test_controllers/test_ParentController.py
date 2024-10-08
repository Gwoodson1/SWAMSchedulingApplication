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
def test_swimmer2_data():
    return {
        'id': 13, 
        'name': 'Ben James', 
        'level': 1, 
        'special_needs': 'ADHD, ODD', 
        'parent_id': 41
    }

@pytest.fixture
def test_parent_data():
    return {
        'id': 45,
        'username': 'MOmar@gmail.com',
        'password': 'Kalil123',
        'name': 'Mohammed Omar',
    }


@pytest.fixture
def test_parent2_data():
    return {
        'id': 41,
        'username': 'sarah.james68@gmail.com',
        'password': 'suMmer09',
        'name': 'Sarah James',
    }


@pytest.fixture
def test_updated_parent_data():
    return {
        'id': 45,
        'username': 'MOmar@gmail.com',
        'password': 'Kalil600!',
        'name': 'Mohammed Omar II',
    }


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


def test_read_parent(app, test_parent_data, test_swimmer_data):
    with app.app_context():
        write_parent = Parent.create_parent(test_parent_data)
        swimmer = Swimmer.create_swimmer(test_swimmer_data)
        write_parent.children = [swimmer]

        read_parent = Parent.read_parent(45)

        assert read_parent.id == 45
        assert read_parent.name == 'Mohammed Omar'
        assert read_parent.children == [swimmer]


def test_get_parents(app, test_parent_data, test_parent2_data):
    with app.app_context():
        parent = Parent.create_parent(test_parent_data)
        parent2 = Parent.create_parent(test_parent2_data)
        list = Parent.get_all_parents()
        
        assert parent in list
        assert parent2 in list


#tests updating information on a specific parent based on ID
def test_update_parent(app, test_parent_data, test_swimmer_data, test_updated_parent_data):
    with app.app_context():
        parent = Parent.create_parent(test_parent_data)
        swimmer = Swimmer.create_swimmer(test_swimmer_data)
        parent.children = [swimmer]

        updated_parent = Parent.update_parent(45, test_updated_parent_data)
        assert updated_parent.id == 45
        assert updated_parent.name == 'Mohammed Omar II'
        assert updated_parent.username == 'MOmar@gmail.com'
        assert updated_parent.password == 'Kalil600!'
        assert updated_parent.children == [swimmer]


#tests deleting a parent based on ID
def test_delete_parent(app, test_parent_data):
    with app.app_context():
        Parent.create_parent(test_parent_data)
        Parent.delete_parent(45)
        deleted_parent = Parent.read_parent(45)
        assert deleted_parent is None
