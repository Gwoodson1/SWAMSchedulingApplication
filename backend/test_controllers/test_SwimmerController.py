import pytest
import backend.app.controllers.SwimmerController as Swimmer

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
        'id': 31, 
        'name': 'Garrett Woodson', 
        'level': 5, 
        'special_needs': 'Goated', 
        'parent_id': 13
    }

@pytest.fixture
def test_updated_swimmer_data():
    return {
        'id': 23, 
        'name': 'Khalil Omar', 
        'level': 4, 
        'special_needs': 'ADHD, ASD', 
        'parent_id': 45
    }

def test_create_swimmer(app, test_swimmer_data):
    with app.app_context():
        new_swimmer = Swimmer.create_swimmer(test_swimmer_data)
        assert new_swimmer.id == 23
        assert new_swimmer.name == 'Khalil Omar'
        assert new_swimmer.level == 3
        assert new_swimmer.special_needs == 'ADHD, ASD'
        assert new_swimmer.parent_id == 45

def test_read_swimmer(app, test_swimmer_data):
    with app.app_context():
        Swimmer.create_swimmer(test_swimmer_data)
        swimmer = Swimmer.read_swimmer(23)
        assert swimmer.id == 23 
        assert swimmer.name == 'Khalil Omar'
        assert swimmer.level == 3
        assert swimmer.special_needs == 'ADHD, ASD'
        assert swimmer.parent_id == 45


def test_get_swimmers(app, test_swimmer_data, test_swimmer2_data):
    with app.app_context():
        swimmer = Swimmer.create_swimmer(test_swimmer_data)
        swimmer2 = Swimmer.create_swimmer(test_swimmer2_data)
        list = Swimmer.read_swimmers()
        
        assert list == [swimmer, swimmer2]
        swimmer3 = list[1]
        assert swimmer3.name == 'Garrett Woodson'


#tests updating information on a specific swimmer based on ID
def test_update_swimmer(app, test_swimmer_data, test_updated_swimmer_data):
    with app.app_context():
        Swimmer.create_swimmer(test_swimmer_data)
        updated_swimmer = Swimmer.update_swimmer(23, test_updated_swimmer_data)
        assert updated_swimmer.id == 23 
        assert updated_swimmer.name == 'Khalil Omar'
        assert updated_swimmer.level == 4
        assert updated_swimmer.special_needs == 'ADHD, ASD'
        assert updated_swimmer.parent_id == 45

#tests deleting a swimmer based on ID
def test_delete_swimmer(app, test_swimmer_data):
    with app.app_context():
        Swimmer.create_swimmer(test_swimmer_data)
        Swimmer.delete_swimmer(23)
        deleted_swimmer = Swimmer.read_swimmer(23)
        assert deleted_swimmer is None