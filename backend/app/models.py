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

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'type': self.type,
        }

class Parent(User):
    __tablename__ = 'parents'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    swimmers = db.relationship('ParentSwimmer', back_populates='parent', cascade='all, delete-orphan')
    __mapper_args__ = {
        'polymorphic_identity': 'parent',
    }

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name
        }

class Instructor(User):
    __tablename__ = 'instructors'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lessons = db.relationship('InstructorLesson', back_populates='instructor', cascade='all, delete-orphan')
    __mapper_args__ = {
        'polymorphic_identity': 'instructor',
    }

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name
        }

class Swimmer(db.Model):
    __tablename__ = 'swimmers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    special_needs = db.Column(db.String(200), nullable=True)
    lessons = db.relationship('SwimmerLesson', back_populates='swimmer', cascade='all, delete-orphan')
    parents = db.relationship('ParentSwimmer', back_populates='swimmer', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'special_needs': self.special_needs
        }

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    lesson_time = db.Column(db.String, nullable=True)  # Kept as String for flexibility
    instructors = db.relationship('InstructorLesson', back_populates='lesson', cascade='all, delete-orphan')
    swimmers = db.relationship('SwimmerLesson', back_populates='lesson', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'lesson_time': self.lesson_time
        }

class SwimmerLesson(db.Model):  # Association Table
    __tablename__ = 'swimmer_lessons'
    swimmer_id = db.Column(db.Integer, db.ForeignKey('swimmers.id'), primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), primary_key=True)

    swimmer = db.relationship('Swimmer', back_populates='lessons')
    lesson = db.relationship('Lesson', back_populates='swimmers')

    def to_dict(self):
        return {
            'swimmer_id': self.swimmer_id,
            'lesson_id': self.lesson_id
        }

class InstructorLesson(db.Model):  # Association Table
    __tablename__ = 'instructor_lessons'
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), primary_key=True)

    instructor = db.relationship('Instructor', back_populates='lessons')
    lesson = db.relationship('Lesson', back_populates='instructors')

    def to_dict(self):
        return {
            'instructor_id': self.instructor_id,
            'lesson_id': self.lesson_id
        }

class ParentSwimmer(db.Model):  # Association Table
    __tablename__ = 'parent_swimmers'
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), primary_key=True)
    swimmer_id = db.Column(db.Integer, db.ForeignKey('swimmers.id'), primary_key=True)

    parent = db.relationship('Parent', back_populates='swimmers')
    swimmer = db.relationship('Swimmer', back_populates='parents')

    def to_dict(self):
        return {
            'parent_id': self.parent_id,
            'swimmer_id': self.swimmer_id
        }