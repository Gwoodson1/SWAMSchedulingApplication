import sys
sys.path.append('/Users/benjamin/Documents/SWAM Application/SWAMSchedulingApplication/backend/app/controllers/swimmer_crud.py')

import pytest
from swimmer_crud import add_swimmer, get_swimmer, get_swimmers, update_swimmer, delete_swimmer

@pytest.fixture
def test_swimmer_data():
    return({'id': 23, 'name': 'Khalil Omar', 'level': 3, 'special_needs': 'ADHD, ASD', 'parent_id': [45, 67]})

#def test_add_swimmer()
    add_swimmers