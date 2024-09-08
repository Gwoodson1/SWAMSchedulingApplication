import os
from . import db
import pandas as pd
from io import BytesIO
from .models import Lesson, Swimmer, Instructor, SwimmerLesson, InstructorLesson
import csv
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_uploaded_file(filepath):
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    elif filepath.endswith('.xlsx'):
        df = pd.read_excel(filepath)
    else:
        raise ValueError("Unsupported file format")

    data = df.to_dict(orient='records')
    return data

def save_file(file, upload_folder):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return filepath
    else:
        raise ValueError("Invalid file type")
    
def export_lessons_to_file(file_type='csv'):
    # Query lessons along with related swimmer and instructor data
    lessons = db.session.query(Lesson).join(SwimmerLesson).join(Swimmer).join(InstructorLesson).join(Instructor).all()

    # Prepare the data for export
    data = []
    for lesson in lessons:
        for swimmer_lesson in lesson.swimmers:
            for instructor_lesson in lesson.instructors:
                data.append({
                    'Lesson Time': lesson.lesson_time or '',  # Replace None with an empty string
                    'Swimmer Name': swimmer_lesson.swimmer.name,
                    'Instructor Name': instructor_lesson.instructor.name
                })

    if file_type == 'xlsx':
        # Export to Excel
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue(), 'lessons.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    
    else:
        # Export to CSV
        output = BytesIO()
        writer = csv.DictWriter(output, fieldnames=['Lesson Time', 'Swimmer Name', 'Instructor Name'])
        writer.writeheader()
        writer.writerows(data)
        output.seek(0)  # Move the cursor to the start of the file
        return output.getvalue(), 'lessons.csv', 'text/csv'