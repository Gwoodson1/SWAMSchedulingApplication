from flask import Blueprint, jsonify, request
from .models import Parent, Instructor, Swimmer, Lesson
from .controllers.InstructorController import (
    create_instructor, read_instructor, update_instructor, 
    delete_instructor, get_all_instructors, update_instructor_by_username
)
from .controllers.ParentController import (
    create_parent, update_parent, delete_parent, 
    get_all_parents, update_parent_by_username
)
from .controllers.LessonController import (
    create_lesson, read_lesson, get_all_lessons, 
    update_lesson, delete_lesson
)
from .controllers.SwimmerController import (
    create_swimmer, read_swimmer, get_all_swimmers, 
    update_swimmer, delete_swimmer
)

# Initialize Blueprint
api_bp = Blueprint('api', __name__)

# Instructor Routes
@api_bp.route('/instructors', methods=['POST'])
def add_instructor():
    try:
        instructor_data = request.json
        new_instructor = create_instructor(instructor_data)
        return jsonify(new_instructor), 201
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/instructors/<int:instructor_id>', methods=['GET'])
def get_instructor(instructor_id):
    try:
        instructor = read_instructor(instructor_id)
        if instructor:
            return jsonify(instructor), 200
        return jsonify(error="Instructor not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/instructors', methods=['GET'])
def get_instructors():
    try:
        instructors = get_all_instructors()
        return jsonify(instructors), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/instructors/<int:instructor_id>', methods=['PUT'])
def modify_instructor(instructor_id):
    try:
        instructor_data = request.json
        updated_instructor = update_instructor(instructor_id, instructor_data)
        if updated_instructor:
            return jsonify(updated_instructor), 200
        return jsonify(error="Instructor not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/instructors/<int:instructor_id>', methods=['DELETE'])
def remove_instructor(instructor_id):
    try:
        deleted_instructor = delete_instructor(instructor_id)
        if deleted_instructor:
            return jsonify(deleted_instructor), 200
        return jsonify(error="Instructor not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/instructors/username/<string:username>', methods=['PUT'])
def modify_instructor_by_username(username):
    try:
        instructor_data = request.json
        updated_instructor = update_instructor_by_username(username, instructor_data)
        if updated_instructor:
            return jsonify(updated_instructor), 200
        return jsonify(error="Instructor not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/instructors/username/<string:username>', methods=['GET'])
def get_instructors_by_username(username):
    try:
        instructor = Instructor.query.filter_by(username=username).first()
        if instructor:
            return jsonify(instructor.to_dict()), 200
        return jsonify(error="Instructor not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500
    
# Parent Routes
@api_bp.route('/parents', methods=['GET'])
def get_parents():
    try:
        parents = get_all_parents()
        return jsonify(parents), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/parents', methods=['POST'])
def add_parent():
    try:
        parent_data = request.json
        new_parent = create_parent(parent_data)
        return jsonify(new_parent), 201
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/parents/<int:parent_id>', methods=['PUT'])
def modify_parent(parent_id):
    try:
        parent_data = request.json
        updated_parent = update_parent(parent_id, parent_data)
        if updated_parent:
            return jsonify(updated_parent), 200
        return jsonify(error="Parent not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/parents/<int:parent_id>', methods=['DELETE'])
def remove_parent(parent_id):
    try:
        deleted_parent = delete_parent(parent_id)
        if deleted_parent:
            return jsonify(deleted_parent), 200
        return jsonify(error="Parent not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/parents/username/<string:username>', methods=['GET'])
def get_parent_by_username(username):
    try:
        parent = Parent.query.filter_by(username=username).first()
        if parent:
            return jsonify(parent.to_dict()), 200
        return jsonify(error="Parent not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/parents/username/<string:username>', methods=['PUT'])
def modify_parent_by_username(username):
    try:
        parent_data = request.json
        updated_parent = update_parent_by_username(username, parent_data)
        if updated_parent:
            return jsonify(updated_parent), 200
        return jsonify(error="Parent not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

# Swimmer Routes
@api_bp.route('/swimmers', methods=['POST'])
def add_swimmer():
    try:
        swimmer_data = request.json
        new_swimmer = create_swimmer(swimmer_data)
        return jsonify(new_swimmer), 201
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/swimmers/<int:swimmer_id>', methods=['GET'])
def get_swimmer(swimmer_id):
    try:
        swimmer = read_swimmer(swimmer_id)
        if swimmer:
            return jsonify(swimmer), 200
        return jsonify(error="Swimmer not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/swimmers', methods=['GET'])
def get_swimmers():
    try:
        swimmers = get_all_swimmers()
        return jsonify(swimmers), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/swimmers/<int:swimmer_id>', methods=['PUT'])
def modify_swimmer(swimmer_id):
    try:
        swimmer_data = request.json
        updated_swimmer = update_swimmer(swimmer_id, swimmer_data)
        if updated_swimmer:
            return jsonify(updated_swimmer), 200
        return jsonify(error="Swimmer not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/swimmers/<int:swimmer_id>', methods=['DELETE'])
def remove_swimmer(swimmer_id):
    try:
        deleted_swimmer = delete_swimmer(swimmer_id)
        if deleted_swimmer:
            return jsonify(deleted_swimmer), 200
        return jsonify(error="Swimmer not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

# Lesson Routes
@api_bp.route('/lessons', methods=['POST'])
def add_lesson():
    try:
        lesson_data = request.json
        new_lesson = create_lesson(lesson_data)
        return jsonify(new_lesson), 201
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/lessons/<int:lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    try:
        lesson = read_lesson(lesson_id)
        if lesson:
            return jsonify(lesson), 200
        return jsonify(error="Lesson not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/lessons', methods=['GET'])
def get_lessons():
    try:
        lessons = get_all_lessons()
        return jsonify(lessons), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/lessons/<int:lesson_id>', methods=['PUT'])
def modify_lesson(lesson_id):
    try:
        lesson_data = request.json
        updated_lesson = update_lesson(lesson_id, lesson_data)
        if updated_lesson:
            return jsonify(updated_lesson), 200
        return jsonify(error="Lesson not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

@api_bp.route('/lessons/<int:lesson_id>', methods=['DELETE'])
def remove_lesson(lesson_id):
    try:
        deleted_lesson = delete_lesson(lesson_id)
        if deleted_lesson:
            return jsonify(deleted_lesson), 200
        return jsonify(error="Lesson not found"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500
