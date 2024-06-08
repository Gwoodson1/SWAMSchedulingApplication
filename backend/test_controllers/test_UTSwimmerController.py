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
def test_new_swimmer_data():
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

'''
def test_get_swimmers(app, test_swimmer_data):
    with app.app_context():
        new_swimmer = Swimmer.create_swimmer(test_swimmer_data)
        swimmer_data = Swimmer.

#tests getting information on all swimmers
Swimmer.get_swimmers()

#tests getting information on a specific swimmer based on ID
Swimmer.get_swimmer()
'''

#tests updating information on a specific swimmer based on ID
def test_update_swimmer(app, test_swimmer_data, test_new_swimmer_data):
    with app.app_context():
        new_swimmer = Swimmer.create_swimmer(test_swimmer_data)
        updated_swimmer = Swimmer.update_swimmer(23, test_new_swimmer_data)
        assert updated_swimmer.id == 23
        assert updated_swimmer.level == 4

#tests deleting a swimmer based on ID
#Swimmer.delete_swimmer()