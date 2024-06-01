from flask import request, jsonify, abort
from app.models import db, Swimmer, Parent, Instructor, Lesson
from app.run import app

#Create, Read, Update, Delete Methods for Swimmer
@app.route('/swimmers', methods=['POST'])
def add_swimmer():
    data = request.get_json()
    new_swimmer = Swimmer(name=data['name'], level=data['level'], special_needs=data.get('special_needs', None))
    db.session.add(new_swimmer)
    db.session.commit()
    return jsonify(new_swimmer.to_dict()), 201

@app.route('/swimmers', methods=['GET'])
def get_swimmers():
    swimmers = Swimmer.query.all()
    return jsonify([swimmer.to_dict() for swimmer in swimmers])

@app.route('/swimmers/<int:id>', methods=['GET'])
def get_swimmer(id):
    swimmer = Swimmer.query.get_or_404(id)
    return jsonify(swimmer.to_dict())

@app.route('/swimmers/<int:id>', methods=['PUT'])
def update_swimmer(id):
    swimmer = Swimmer.query.get_or_404(id)
    data = request.get_json()
    swimmer.name = data.get('name', swimmer.name)
    swimmer.level = data.get('level', swimmer.level)
    swimmer.special_needs = data.get('special_needs', swimmer.special_needs)
    db.session.commit()
    return jsonify(swimmer.to_dict())

@app.route('/swimmers/<int:id>', methods=['DELETE'])
def delete_swimmer(id):
    swimmer = Swimmer.query.get_or_404(id)
    db.session.delete(swimmer)
    db.session.commit()
    return jsonify({'message': 'Deleted'})