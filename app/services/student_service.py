from app.models.student_model import Student
from app import db

def create_student(name, age):
    student = Student(name=name, age=age)
    db.session.add(student)
    db.session.commit()
    return student

def get_all_students():
    return Student.query.all()

def get_student_by_id(student_id):
    return Student.query.filter_by(id=student_id).first()