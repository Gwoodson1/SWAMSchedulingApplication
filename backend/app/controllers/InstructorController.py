from flask import request, jsonify, abort
from models import db, Swimmer, Parent, Instructor, Lesson
from app.run import app


#CRUD for instructor

@app.route('/instructors', methods=['POST'])
def create_instructor():
    data = request.get_json()
    new_instructor = Instructor(username=data['username'], password=data['password'], cert_time=data['cert_time'])
    db.session.add(new_instructor)
    db.session.commit()
    return jsonify(new_instructor.id), 201

@app.route('/instructors/<int:id>', methods=['GET'])
def get_instructor(id):
    instructor = Instructor.query.get_or_404(id)
    return jsonify({
        'id': instructor.id,
        'username': instructor.username,
        'cert_time': instructor.cert_time
    })

@app.route('/instructors/<int:id>', methods=['PUT'])
def update_instructor(id):
    instructor = Instructor.query.get_or_404(id)
    data = request.get_json()
    instructor.username = data.get('username', instructor.username)
    instructor.password = data.get('password', instructor.password)
    instructor.cert_time = data.get('cert_time', instructor.cert_time)
    db.session.commit()
    return jsonify({'id': instructor.id}), 200

@app.route('/instructors/<int:id>', methods=['DELETE'])
def delete_instructor(id):
    instructor = Instructor.query.get_or_404(id)
    db.session.delete(instructor)
    db.session.commit()
    return jsonify({'message': 'Instructor deleted'}), 204