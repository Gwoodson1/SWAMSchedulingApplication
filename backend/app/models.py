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
    lesson_time = db.Column(db.String, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'lesson_time': self.lesson_time
        }

class SwimmerLesson(db.Model):  # Association Table
    __tablename__ = 'swimmer_lessons'
    id = db.Column(db.Integer, primary_key=True)
    swimmer_id = db.Column(db.Integer, db.ForeignKey('swimmers.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))

    def to_dict(self):
        return {
            'swimmer_id': self.swimmer_id,
            'lesson_id': self.lesson_id
        }

class InstructorLesson(db.Model):  # Association Table
    __tablename__ = 'instructor_lessons'
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))

    def to_dict(self):
        return {
            'instructor_id': self.instructor_id,
            'lesson_id': self.lesson_id
        }

class ParentSwimmer(db.Model):  # Association Table
    __tablename__ = 'parent_swimmers'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'))
    swimmer_id = db.Column(db.Integer, db.ForeignKey('swimmers.id'))

    def to_dict(self):
        return {
            'parent_id': self.parent_id,
            'swimmer_id': self.swimmer_id
        }
