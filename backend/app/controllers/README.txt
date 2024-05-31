#README: Old CRUD methods file from before refactor

from flask import request, jsonify, abort
from models import db, Swimmer, Parent, Instructor, Lesson
from app import app



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

#CRUD for Lesson
@app.route('/lessons', methods=['POST'])
def create_lesson():
    data = request.get_json()
    new_lesson = Lesson(
        lesson_time=data['lesson_time'],
        swimmer_id=data['swimmer_id'],
        instructor_id=data['instructor_id']
    )
    db.session.add(new_lesson)
    db.session.commit()
    return jsonify(new_lesson.id), 201

@app.route('/lessons/<int:id>', methods=['GET'])
def get_lesson(id):
    lesson = Lesson.query.get_or_404(id)
    return jsonify({
        'id': lesson.id,
        'lesson_time': lesson.lesson_time,
        'swimmer_id': lesson.swimmer_id,
        'instructor_id': lesson.instructor_id
    })

@app.route('/lessons/<int:id>', methods=['PUT'])
def update_lesson(id):
    lesson = Lesson.query.get_or_404(id)
    data = request.get_json()
    lesson.lesson_time = data.get('lesson_time', lesson.lesson_time)
    lesson.swimmer_id = data.get('swimmer_id', lesson.swimmer_id)
    lesson.instructor_id = data.get('instructor_id', lesson.instructor_id)
    db.session.commit()
    return jsonify({'id': lesson.id}), 200

@app.route('/lessons/<int:id>', methods=['DELETE'])
def delete_lesson(id):
    lesson = Lesson.query.get_or_404(id)
    db.session.delete(lesson)
    db.session.commit()
    return jsonify({'message': 'Lesson deleted'}), 204

