# app/views.py
from flask import Blueprint, jsonify, request
from app.controllers.instructor_crud import get_users, create_user, update_user, delete_user
from app.controllers.lesson_crud import get_lessons, create_lesson, update_lesson, delete_lesson
# Import other controllers as needed

# Initialize Blueprint
api_bp = Blueprint('api', __name__)

# User Routes
@api_bp.route('/api/users', methods=['GET'])
def list_users():
    users = get_users()
    return jsonify(users), 200

@api_bp.route('/api/users', methods=['POST'])
def add_user():
    user_data = request.json
    new_user = create_user(user_data)
    return jsonify(new_user), 201

@api_bp.route('/api/users/<int:user_id>', methods=['PUT'])
def modify_user(user_id):
    user_data = request.json
    updated_user = update_user(user_id, user_data)
    return jsonify(updated_user), 200

@api_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    delete_user(user_id)
    return '', 204

# Lesson Routes
@api_bp.route('/api/lessons', methods=['GET'])
def list_lessons():
    lessons = get_lessons()
    return jsonify(lessons), 200

@api_bp.route('/api/lessons', methods=['POST'])
def add_lesson():
    lesson_data = request.json
    new_lesson = create_lesson(lesson_data)
    return jsonify(new_lesson), 201

@api_bp.route('/api/lessons/<int:lesson_id>', methods=['PUT'])
def modify_lesson(lesson_id):
    lesson_data = request.json
    updated_lesson = update_lesson(lesson_id, lesson_data)
    return jsonify(updated_lesson), 200

@api_bp.route('/api/lessons/<int:lesson_id>', methods=['DELETE'])
def remove_lesson(lesson_id):
    delete_lesson(lesson_id)
    return '', 204
\