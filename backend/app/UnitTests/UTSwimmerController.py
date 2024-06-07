import pytest
import backend.app.controllers.SwimmerController as Swimmer

@pytest.fixture
def test_swimmer_data():
    return({'id': 23, 'name': 'Khalil Omar', 'level': 3, 'special_needs': 'ADHD, ASD', 'parent_id': [45, 67]})

#tests creation of a new swimmer
Swimmer.add_swimmer()

'''
#tests getting information on all swimmers
Swimmer.get_swimmers()

#tests getting information on a specific swimmer based on ID
Swimmer.get_swimmer()

#tests updating information on a specific swimmer based on ID
Swimmer.update_swimmer()

#tests deleting a swimmer based on ID
Swimmer.delete_swimmer()

'''