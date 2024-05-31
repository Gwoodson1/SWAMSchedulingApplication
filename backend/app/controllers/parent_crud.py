from flask import request, jsonify, abort
from models import db, Swimmer, Parent, Instructor, Lesson
from app import app

#CRUD for Parent Class
@app.route('/parents', methods=['POST'])
def create_parent():
    data = request.get_json()
    new_parent = Parent(username=data['username'], password=data['password'])
    db.session.add(new_parent)
    db.session.commit()
    return jsonify(new_parent.id), 201

@app.route('/parents/<int:id>', methods=['GET'])
def get_parent(id):
    parent = Parent.query.get_or_404(id)
    return jsonify({
        'id': parent.id,
        'username': parent.username
    })

@app.route('/parents/<int:id>', methods=['PUT'])
def update_parent(id):
    parent = Parent.query.get_or_404(id)
    data = request.get_json()
    parent.username = data.get('username', parent.username)
    parent.password = data.get('password', parent.password)
    db.session.commit()
    return jsonify({'id': parent.id}), 200

@app.route('/parents/<int:id>', methods=['DELETE'])
def delete_parent(id):
    parent = Parent.query.get_or_404(id)
    db.session.delete(parent)
    db.session.commit()
    return jsonify({'message': 'Parent deleted'}), 204