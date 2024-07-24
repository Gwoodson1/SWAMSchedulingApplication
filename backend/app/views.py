from flask import Blueprint, jsonify, request
from .models import Parent
from .controllers.InstructorController import create_instructor, update_instructor, delete_instructor
from .controllers.ParentController import create_parent, update_parent, delete_parent, get_all_parents, update_parent_by_username

# Initialize Blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/instructors', methods=['POST'])
def add_instructor():
    try:
        instructor_data = request.json
        new_instructor = create_instructor(instructor_data)
        return jsonify(new_instructor), 201
    except Exception as e:
        print(f"Error in add_instructor: {str(e)}")
        return jsonify(error=str(e)), 500

@api_bp.route('/instructors/<int:instructor_id>', methods=['PUT'])
def modify_instructor(instructor_id):
    try:
        instructor_data = request.json
        updated_instructor = update_instructor(instructor_id, instructor_data)
        return jsonify(updated_instructor), 200
    except Exception as e:
        print(f"Error in modify_instructor: {str(e)}")
        return jsonify(error=str(e)), 500

@api_bp.route('/instructors/<int:instructor_id>', methods=['DELETE'])
def remove_instructor(instructor_id):
    try:
        delete_instructor(instructor_id)
        return '', 204
    except Exception as e:
        print(f"Error in remove_instructor: {str(e)}")
        return jsonify(error=str(e)), 500

@api_bp.route('/parents', methods=['GET'])
def get_parents():
    try:
        parents = get_all_parents()
        return jsonify(parents), 200
    except Exception as e:
        print(f"Error in get_parents: {str(e)}")
        return jsonify(error=str(e)), 500

@api_bp.route('/parents', methods=['POST'])
def add_parent():
    try:
        parent_data = request.json
        new_parent = create_parent(parent_data)
        return jsonify(new_parent), 201
    except Exception as e:
        print(f"Error in add_parent: {str(e)}")
        return jsonify(error=str(e)), 500

@api_bp.route('/parents/<int:parent_id>', methods=['PUT'])
def modify_parent(parent_id):
    try:
        parent_data = request.json
        updated_parent = update_parent(parent_id, parent_data)
        return jsonify(updated_parent), 200
    except Exception as e:
        print(f"Error in modify_parent: {str(e)}")
        return jsonify(error=str(e)), 500

@api_bp.route('/parents/<int:parent_id>', methods=['DELETE'])
def remove_parent(parent_id):
    try:
        delete_parent(parent_id)
        return '', 204
    except Exception as e:
        print(f"Error in remove_parent: {str(e)}")
        return jsonify(error=str(e)), 500

@api_bp.route('/parents/username/<string:username>', methods=['GET'])
def get_parent_by_username(username):
    try:
        parent = Parent.query.filter_by(username=username).first()
        if parent:
            return jsonify(parent.to_dict()), 200
        else:
            return jsonify(error="Parent not found"), 404
    except Exception as e:
        print(f"Error in get_parent_by_username: {str(e)}")
        return jsonify(error=str(e)), 500

@api_bp.route('/parents/username/<string:username>', methods=['PUT'])
def modify_parent_by_username(username):
    try:
        parent_data = request.json
        updated_parent = update_parent_by_username(username, parent_data)
        return jsonify(updated_parent), 200
    except Exception as e:
        print(f"Error in modify_parent_by_username: {str(e)}")
        return jsonify(error=str(e)), 500
  