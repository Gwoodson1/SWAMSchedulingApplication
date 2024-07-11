from flask import Blueprint, jsonify, request
from .controllers.InstructorController import create_instructor, update_instructor, delete_instructor
from .controllers.ParentController import create_parent, update_parent, delete_parent, read_parents

# Initialize Blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/instructors', methods=['POST'])
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

@api_bp.route('/parents', methods=['GET'])
def get_parents():
    parents = read_parents()
    return jsonify(parents), 200

@api_bp.route('/parents', methods=['POST'])
def add_parent():
    parent_data = request.json
    new_parent = create_parent(parent_data)
    return jsonify(new_parent), 201

@api_bp.route('/parents/<int:parent_id>', methods=['PUT'])
def modify_parent(parent_id):
    parent_data = request.json
    updated_parent = update_parent(parent_id, parent_data)
    return jsonify(updated_parent), 200

@api_bp.route('/parents/<int:parent_id>', methods=['DELETE'])
def remove_parent(parent_id):
    delete_parent(parent_id)
    return '', 204
