import pytest
from datetime import datetime #do we really need this
import backend.app.controllers.InstructorController as Instructor
import backend.app.controllers.LessonController as Lesson


@pytest.fixture
def test_lesson_data():
    return {
        'id': 23, 
        'lesson_time': datetime(2024, 6, 10, 9, 30),
        'swimmer_id': 13,
        'instructor_id': 9
        #missing swimmer relationship
        #missing instructor relationship
    }

@pytest.fixture
def test_instructor_data():
    return {
        'id': 9,
        'username': 'janeWer4',
        'password': 'swam_5'
    }

@pytest.fixture
def test_instructor2_data():
    return {
        'id': 98,
        'username': 'KyleDog',
        'password': 'sq3wq!'
    }

@pytest.fixture
def test_updated_instructor_data():
    return {
        'id': 9,
        'username': 'janeWer4',
        'password': 'swam_49'
    }

def test_create_instructor(app, test_instructor_data, test_lesson_data):
    with app.app_context():
        new_instructor = Instructor.create_instructor(test_instructor_data)
        lesson = Lesson.create_lesson(test_lesson_data)
        new_instructor.lessons = [lesson]

        assert new_instructor.id == 9
        assert new_instructor.username == 'janeWer4'
        assert new_instructor.password == 'swam_5'
        assert new_instructor.lessons == [lesson]


def test_read_instructor(app, test_instructor_data, test_lesson_data):
    with app.app_context():
        write_instructor = Instructor.create_instructor(test_instructor_data)
        lesson = Lesson.create_lesson(test_lesson_data)
        write_instructor.lessons = [lesson]

        read_instructor = Instructor.read_instructor(9)

        assert read_instructor.id == 9
        assert read_instructor.username == 'janeWer4'
        assert read_instructor.password == 'swam_5'
        assert read_instructor.lessons == [lesson]


def test_get_instructors(app, test_instructor_data, test_instructor2_data):
    with app.app_context():
        instructor = Instructor.create_instructor(test_instructor_data)
        instructor2 = Instructor.create_instructor(test_instructor2_data)
        list = Instructor.read_instructors()
        
        assert instructor in list
        assert instructor2 in list


#tests updating information on a specific instructor based on ID
def test_update_instructor(app, test_instructor_data, test_lesson_data, test_updated_instructor_data):
    with app.app_context():
        instructor = Instructor.create_instructor(test_instructor_data)
        lesson = Lesson.create_lesson(test_lesson_data)
        instructor.lessons = [lesson]

        updated_instructor = Instructor.update_instructor(9, test_updated_instructor_data)
        assert updated_instructor.id == 9
        assert updated_instructor.username == 'janeWer4'
        assert updated_instructor.password == 'swam_49'
        assert updated_instructor.lessons == [lesson]

#tests deleting a instructor based on ID
def test_delete_instructor(app, test_instructor_data):
    with app.app_context():
        Instructor.create_instructor(test_instructor_data)
        Instructor.delete_instructor(9)
        deleted_instructor = Instructor.read_instructor(9)
        assert deleted_instructor is None
