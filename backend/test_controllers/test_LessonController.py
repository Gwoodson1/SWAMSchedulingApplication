
import pytest
from datetime import datetime
import backend.app.controllers.LessonController as Lesson
import backend.app.controllers.SwimmerController as Swimmer
import backend.app.controllers.InstructorController as Instructor


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
def test_instructor_data():
    return {
        'id': 9,
        'username': 'janeWer4',
        'password': 'swam_5'
    }

@pytest.fixture
def test_lesson_data():
    return {
        'id': 51, 
        'lesson_time': datetime(2024, 6, 10, 9, 30),
        'swimmer_id': 23,
        'instructor_id': 9
    }


@pytest.fixture
def test_lesson2_data():
    return {
        'id': 15, 
        'lesson_time': datetime(2024, 6, 11, 9, 30),
        'swimmer_id': 64,
        'instructor_id': 9
    }

@pytest.fixture
def test_updated_lesson_data():
    return {
        'id': 51, 
        'lesson_time': datetime(2024, 6, 10, 10, 30),
        'swimmer_id': 23,
        'instructor_id': 9
        #missing swimmer relationship
        #missing instructor relationship
    }


def test_create_lesson(app, test_lesson_data, test_swimmer_data, test_instructor_data):
    with app.app_context():
        new_lesson = Lesson.create_lesson(test_lesson_data)
        swimmer = Swimmer.create_swimmer(test_swimmer_data)
        instructor = Instructor.create_instructor(test_instructor_data)
        new_lesson.swimmer = swimmer
        new_lesson.instructor = instructor

        assert new_lesson.id == 51
        assert new_lesson.lesson_time == datetime(2024, 6, 10, 9, 30)
        assert new_lesson.swimmer_id == 23
        assert new_lesson.instructor_id == 9
        assert new_lesson.swimmer == swimmer
        assert new_lesson.instructor == instructor


def test_read_lesson(app, test_lesson_data, test_swimmer_data, test_instructor_data):
    with app.app_context():
        write_lesson = Lesson.create_lesson(test_lesson_data)
        swimmer = Swimmer.create_swimmer(test_swimmer_data)
        instructor = Instructor.create_instructor(test_instructor_data)
        write_lesson.swimmer = swimmer
        write_lesson.instructor = instructor

        read_lesson = Lesson.read_lesson(51)

        assert read_lesson.id == 51
        assert read_lesson.lesson_time == datetime(2024, 6, 10, 9, 30)
        assert read_lesson.swimmer_id == 23
        assert read_lesson.instructor_id == 9
        assert read_lesson.swimmer == swimmer
        assert read_lesson.instructor == instructor


def test_get_lessons(app, test_lesson_data, test_lesson2_data, test_swimmer_data, test_instructor_data):
    with app.app_context():
        lesson = Lesson.create_lesson(test_lesson_data)
        lesson2 = Lesson.create_lesson(test_lesson2_data)
        swimmer = Swimmer.create_swimmer(test_swimmer_data)
        instructor = Instructor.create_instructor(test_instructor_data)
        lesson.swimmer = swimmer
        lesson2.instructor = instructor
        list = Lesson.read_lessons()
        
        assert lesson in list
        assert lesson2 in list


#tests updating information on a specific lesson based on ID
def test_update_lesson(app, test_lesson_data, test_swimmer_data, test_instructor_data, test_updated_lesson_data):
    with app.app_context():
        lesson = Lesson.create_lesson(test_lesson_data)
        swimmer = Swimmer.create_swimmer(test_swimmer_data)
        instructor = Instructor.create_instructor(test_instructor_data)
        lesson.swimmer = swimmer
        lesson.instructor = instructor


        updated_lesson = Lesson.update_lesson(51, test_updated_lesson_data)

        assert updated_lesson.id == 51
        assert updated_lesson.lesson_time == datetime(2024, 6, 10, 10, 30)
        assert updated_lesson.swimmer_id == 23
        assert updated_lesson.instructor_id == 9
        assert updated_lesson.swimmer == swimmer
        assert updated_lesson.instructor == instructor

#tests deleting a lesson based on ID
def test_delete_lesson(app, test_lesson_data):
    with app.app_context():
        Lesson.create_lesson(test_lesson_data)
        Lesson.delete_lesson(51)
        deleted_lesson = Lesson.read_lesson(51)
        assert deleted_lesson is None


