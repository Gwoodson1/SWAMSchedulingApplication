from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True) #TODO Username and password should eventually be Not Nullable
    password = db.Column(db.String(80), nullable=True)
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
    gender = db.Column(db.String(100), nullable=True)
    languages = db.Column(db.String(100), nullable=True)
    swimmer_preference = db.Column(db.String(100), nullable=True)
    assigned_child_preference = db.Column(db.String(100), nullable=True)
    taught_lessons = db.Column(db.String(100), nullable=True)
    worked_with_disabilities = db.Column(db.String(100), nullable=True)
    relevant_experience = db.Column(db.String(100), nullable=True)
    expectations = db.Column(db.String(100), nullable=True)
    additional_info = db.Column(db.String(100), nullable=True)
    previous_swam_lessons = db.Column(db.String(100), nullable=True)
    lessons = db.relationship('InstructorLesson', back_populates='instructor', cascade='all, delete-orphan')
    __mapper_args__ = {
        'polymorphic_identity': 'instructor',
    }

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'gender': self.gender,
            'languages': self.languages,
            'swimmer_preference': self.swimmer_preference,
            'assigned_child_preference': self.assigned_child_preference,
            'taught_lessons': self.taught_lessons,
            'worked_with_disabilities': self.worked_with_disabilities,
            'relevant_experience': self.relevant_experience,
            'expectations': self.expectations,
            'additional_info': self.additional_info,
            'previous_swam_lessons': self.previous_swam_lessons,
        }

class Swimmer(db.Model):
    __tablename__ = 'swimmers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=True)
    age = db.Column(db.String(100), nullable=True)
    language = db.Column(db.String(100), nullable=True)
    instructor_preference = db.Column(db.String(100), nullable=True)
    previous_instructor = db.Column(db.String(100), nullable=True)
    availabilities = db.Column(db.String(100), nullable=True)
    level = db.Column(db.String, nullable=True)
    special_needs = db.Column(db.String(200), nullable=True)
    special_needs_info = db.Column(db.String(200), nullable=True)
    swim_experience = db.Column(db.String(200), nullable=True)
    experience_details = db.Column(db.String(200), nullable=True)
    previous_swam_lessons = db.Column(db.String(200), nullable=True)
    new_instructor_explanation = db.Column(db.String(200), nullable=True)
    lessons = db.relationship('SwimmerLesson', back_populates='swimmer', cascade='all, delete-orphan')
    parents = db.relationship('ParentSwimmer', back_populates='swimmer', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'language': self.language,
            'instructor_preference': self.instructor_preference,
            'previous_instructor': self.previous_instructor,
            'new_instructor_explanation': self.new_instructor_explanation,
            'availabilities': self.availabilities,
            'level': self.level,
            'special_needs': self.special_needs,
            'special_needs_info': self.special_needs_info,
            'swim_experience': self.swim_experience,
            'experience_details': self.experience_details,
            'previous_swam_lessons': self.previous_swam_lessons
        }

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    lesson_time = db.Column(db.String, nullable=True)  
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