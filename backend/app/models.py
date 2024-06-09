from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(50))  # Discriminator column
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

class Parent(User):
    __tablename__ = 'parents'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    children = db.relationship('Swimmer', back_populates='parent')
    __mapper_args__ = {
        'polymorphic_identity': 'parent',
    }

class Instructor(User):
    __tablename__ = 'instructors'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    lessons = db.relationship('Lesson', back_populates='instructor')
    __mapper_args__ = {
        'polymorphic_identity': 'instructor',
    }

class Swimmer(db.Model):
    __tablename__ = 'swimmers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    special_needs = db.Column(db.String(200), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'))
    parent = db.relationship('Parent', back_populates='children')
    lessons = db.relationship('Lesson', back_populates='swimmer')

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    lesson_time = db.Column(db.DateTime, nullable=False)
    swimmer_id = db.Column(db.Integer, db.ForeignKey('swimmers.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    swimmer = db.relationship('Swimmer', back_populates='lessons')
    instructor = db.relationship('Instructor', back_populates='lessons')