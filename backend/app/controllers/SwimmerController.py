from .. import db
import re
import pandas as pd
from ..models import Swimmer, Parent, ParentSwimmer, Lesson, SwimmerLesson
import unicodedata

def create_swimmer(data):

    # Check if a swimmer with the same name already exists
    existing_swimmer = Swimmer.query.filter_by(name=data.get('name')).first()
    
    if existing_swimmer:
        raise ValueError(f"Swimmer with the name {data.get('name')} already exists.")
    
    parent_ids = data.get('parent_ids', [])
    lesson_ids = data.get('lesson_ids', [])

    new_swimmer = Swimmer(
        name=data.get('name'),
        gender=data.get('gender'),
        age=data.get('age'),
        language=data.get('language'),
        instructor_preference=data.get('instructor_preference'),
        previous_instructor=data.get('previous_instructor'),
        availabilities=data.get('availabilities'),
        level=data.get('level'),
        special_needs=data.get('special_needs'),
        special_needs_info=data.get('special_needs_info'),
        swim_experience=data.get('swim_experience'),
        experience_details=data.get('experience_details'),
        previous_swam_lessons=data.get('previous_swam_lessons'),
        new_instructor_explanation=data.get('new_instructor_explanation'),
    )
    db.session.add(new_swimmer)
    db.session.commit()

    # Add parents
    for parent_id in parent_ids:
        parent = db.session.get(Parent, parent_id)
        if parent:
            parent_swimmer = ParentSwimmer(parent_id=parent.id, swimmer_id=new_swimmer.id)
            db.session.add(parent_swimmer)

    # Add lessons
    for lesson_id in lesson_ids:
        lesson = db.session.get(Lesson, lesson_id)
        if lesson:
            new_swimmer.lessons.append(SwimmerLesson(lesson=lesson))
           # swimmer_lesson = SwimmerLesson(lesson_id=lesson.id, swimmer_id=new_swimmer.id)
           # db.session.add(swimmer_lesson)

    db.session.commit()

    return new_swimmer.to_dict()

def read_swimmer(swimmer_id):
    swimmer = db.session.get(Swimmer, swimmer_id)
    if swimmer:
        swimmer_dict = swimmer.to_dict()
        # Use the backref to get the parents and lessons directly
        swimmer_dict['parents'] = [ps.parent_id for ps in swimmer.parents]
        swimmer_dict['lessons'] = [sl.lesson_id for sl in swimmer.lessons]
        return swimmer_dict
    return None

def get_all_swimmers():
    swimmers = Swimmer.query.all()
    all_swimmers = []
    for swimmer in swimmers:
        swimmer_dict = swimmer.to_dict()
        # Use the backref to get the parents and lessons directly
        swimmer_dict['parents'] = [ps.parent_id for ps in swimmer.parents]
        swimmer_dict['lessons'] = [sl.lesson_id for sl in swimmer.lessons]
        all_swimmers.append(swimmer_dict)
    return all_swimmers

def update_swimmer(swimmer_id, data):
    swimmer = db.session.get(Swimmer, swimmer_id)
    if swimmer:
        for key, value in data.items():
            setattr(swimmer, key, value)
        db.session.commit()

        # Update parent associations if provided
        if 'parent_ids' in data:
            parent_ids = data['parent_ids']
            # Clear existing associations
            swimmer.parents.clear()
            # Add new associations
            for parent_id in parent_ids:
                parent = db.session.get(Parent, parent_id)
                if parent:
                    swimmer.parents.append(ParentSwimmer(parent_id=parent.id, swimmer_id=swimmer.id))

        # Update lesson associations if provided
        if 'lesson_ids' in data:
            lesson_ids = data['lesson_ids']
            # Clear existing associations
            swimmer.lessons.clear()
            # Add new associations
            for lesson_id in lesson_ids:
                lesson = db.session.get(Lesson, lesson_id)
                if lesson:
                    swimmer.lessons.append(SwimmerLesson(lesson_id=lesson.id, swimmer_id=swimmer.id))

        db.session.commit()

        return swimmer.to_dict()
    return None

def delete_swimmer(swimmer_id):
    swimmer = db.session.get(Swimmer, swimmer_id)
    if swimmer:
        db.session.delete(swimmer)
        db.session.commit()
    return swimmer.to_dict() if swimmer else None

def insert_data_into_db(data):
    for record in data:
        name = str(record.get("Swimmer's First Name // Prénom du nageur")) + " " + str(record.get("Swimmer's Last Name // Nom du nageur"))
        if not name or name == "nan nan":
            print(f"Skipping row with missing swimmer name: {record}")
            continue
        
        # Extract the first number from the level description
        level_description = record.get('Which of the below descriptions sounds the most like your swimmer? // Laquelle des descriptions ci-dessous ressemble le plus à votre nageur?')
        level_match = re.match(r'^\d+', level_description)  # Match the first number
        level = level_match.group(0) if level_match else None  # Extract the number or set to None if no match

        swimmer_data = {
            'name': name.title(),
            'gender': record.get("Gender // Sexe"),
            'language': record.get("Will a lesson done in English work for your swimmer? If no, please specify which language is needed. // Est-ce que votre nageur peut suivre ses leçons en anglais? Si non, veuillez spécifier quelle langue est requise."),
            'instructor_preference': record.get("If you participated in the Fall 2023 lessons, would you like to keep the same instructor? // Si vous avez participé aux cours d'automne 2023, aimeriez-vous garder le même instructeur?"),
            'availabilities': record.get("Please select ALL the lesson times that are convenient. If a time is not an option below, it means it is already full.  // Veuillez sélectionner TOUTES heures de cours qui sont pratique. Si une heure n'est pas une option ci-dessous, cela signifie qu'elle est déjà pleine."),
            'age': record.get('Age of swimmer // Âge du nageur'),
            'level': level, 
            'special_needs': record.get("What is your child's clinical diagnosis?  Check all that apply. // Quel est le diagnostic clinique de votre enfant? Cochez toutes les cases qui s'appliquent."),
            'special_needs_info': record.get("Please provide any other details on your child's clinical diagnosis, disabilities, or special needs. // Veuillez fournir tout autre détail relatif au diagnostic clinique, aux handicaps ou aux besoins spéciaux de votre enfant."),
            'swim_experience': record.get("What is your child's level of swimming experience?  Check all that apply. // Quel est le niveau d'expérience de votre enfant en matière de natation? Cochez toutes les cases qui s'appliquent."),
            'experience_details': record.get("Please provide any other detail on your child's swimming ability. // Veuillez fournir tout autre détail sur l’habileté de nage de votre enfant."),
            'previous_swam_lessons': record.get("How many S.W.A.M. lessons has your child participated in? // À combien de S.W.A.M. leçons  votre enfant a-t-il participé?"),
            'new_instructor_explanation': record.get("If you would like a new instructor, please briefly explain why. If you know the name of the instructor you would like, please include their name. // Si vous souhaitez un nouvel instructeur, veuillez expliquer brièvement pourquoi. Si vous connaissez le nom de l'instructeur que vous souhaitez, veuillez inclure son nom.")
        }

        try:
            create_swimmer(swimmer_data)
        except Exception as e:
            print(f"Failed to insert record: {record} due to error: {e}")
            continue

def process_previous_pairings(filepath):
    """Process the Excel file and update the swimmers' previous instructors."""
    try:
        # Load the Excel file, specifying that the header is in the third row (index 2, since it's 0-based)
        df = pd.read_excel(filepath, sheet_name='tentative schedule', header=2)

        # Print the column names to confirm they're correct now
        print("Columns found in Excel:", df.columns.tolist())

        # Iterate through the rows where instructor-swimmer pairings exist
        for _, row in df.iterrows():
            instructor = row['Instructor']
            swimmer = row['Swimmer']

            # Skip any rows without valid pairings (NaN values)
            if pd.isna(instructor) or pd.isna(swimmer):
                continue

            # Update the swimmer's 'previous_instructor' in the database
            update_swimmer_previous_instructor(swimmer, instructor)

    except Exception as e:
        raise Exception(f"Error processing Excel file: {str(e)}")

def update_swimmer_previous_instructor(swimmer_name, instructor_name):
    """
    Check if the swimmer exists in the database (case and accent-insensitive) and update their 'previous_instructor'.
    If the swimmer does not exist, skip the update.
    """
    # Normalize the swimmer name from the Excel sheet to be case and accent insensitive
    normalized_swimmer_name = normalize_string(swimmer_name)

    # Query the database for the swimmer, comparing names in a case and accent-insensitive way
    swimmers = Swimmer.query.all()  # Retrieve all swimmers (this could be optimized with case-insensitive filtering)

    # Perform case and accent-insensitive search manually by normalizing swimmer names in the database
    for swimmer in swimmers:
        if normalize_string(swimmer.name) == normalized_swimmer_name:
            # Update the 'previous_instructor' field
            swimmer.previous_instructor = instructor_name
            db.session.commit()
            break  # Stop after the first match

    # If no swimmer matches, we simply skip updating
    return

def normalize_string(s):
    """
    Normalize a string by removing diacritics and converting to lowercase.
    """
    # Decompose the unicode string into base characters and diacritics
    nfkd_form = unicodedata.normalize('NFKD', s)
    # Filter out diacritic marks (category starts with 'Mn') and convert to lowercase
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)]).lower().strip()
