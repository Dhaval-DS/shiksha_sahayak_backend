from app.models.student_model import Student
from app import db

from app import db
from app.models.student_model import Student


def create_student(name, age):
    student = Student(name=name, age=age)
    db.session.add(student)
    db.session.commit()
    return student


def get_all_students():
    return Student.query.all()


def get_student_by_id(id):
    return Student.query.get(id)


def update_student(id, data):
    student = Student.query.get(id)
    if not student:
        return None

    student.name = data.get("name", student.name)
    student.age = data.get("age", student.age)

    db.session.commit()
    return student


def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return False

    db.session.delete(student)
    db.session.commit()
    return True