
from flask import request, jsonify, abort
from models import db, Swimmer, Parent, Instructor, Lesson
from app import app

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

