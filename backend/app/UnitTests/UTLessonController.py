
import pytest
from backend.app.controllers.LessonController import create_lesson

@pytest.fixture
def test_swimmer_data():
    return({'id': 23, 'name': 'Khalil Omar', 'level': 3, 'special_needs': 'ADHD, ASD', 'parent_id': [45, 67]})

print("hello world")