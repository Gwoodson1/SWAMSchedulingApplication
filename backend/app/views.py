from flask import Blueprint, jsonify, request
from .controllers.InstructorController import create_instructor, update_instructor, delete_instructor

# Initialize Blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/instructor', methods=['POST'])
def add_instructor():
    instructor_data = request.json
    new_instructor = create_instructor(instructor_data)
    return jsonify(new_instructor), 201

@api_bp.route('/instructors/<int:instructor_id>', methods=['PUT'])
def modify_instructor(instructor_id):
    instructor_data = request.json
    updated_instructor = update_instructor(instructor_id, instructor_data)
    return jsonify(updated_instructor), 200

@api_bp.route('/instructors/<int:instructor_id>', methods=['DELETE'])
def remove_instructor(instructor_id):
    delete_instructor(instructor_id)
    return '', 204