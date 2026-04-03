from app import db
from app.models.teacher_model import Teacher
from app.dto.teacher_dto import (
    TeacherInDTO,
    TeacherOutDTO,
    LoginRequestDTO,
    LoginResponseDTO
)
from app.auth.jwt_handler import create_token
import bcrypt


# 🔹 Register Teacher
def register_teacher(data):
    dto = TeacherInDTO(data)

    # Check if email already exists
    existing_teacher = Teacher.query.filter_by(email=dto.email).first()
    if existing_teacher:
        return {"error": "Email already registered"}, 400

    # Hash password
    hashed_password = bcrypt.hashpw(dto.password.encode("utf-8"), bcrypt.gensalt())

    # Create Teacher object
    teacher = Teacher(
        first_name=dto.first_name,
        last_name=dto.last_name,
        email=dto.email,
        password=hashed_password.decode("utf-8"),
        subject_taught=dto.subject_taught,
        teaching_experience=dto.teaching_experience,
        school_name=dto.school_name,
        role=data.get("role", "teacher")   # ✅ ADD THIS LINE
    )

    db.session.add(teacher)
    db.session.commit()

    return TeacherOutDTO(teacher).to_dict(), 201

# 🔹 Login Teacher
def login_teacher(data):
    dto = LoginRequestDTO(data)

    teacher = Teacher.query.filter_by(email=dto.email).first()

    if not teacher:
        return {"error": "Invalid email or password"}, 401

    # Check password
    if not bcrypt.checkpw(dto.password.encode("utf-8"), teacher.password.encode("utf-8")):
        return {"error": "Invalid email or password"}, 401

    # Generate JWT token
    token = create_token(teacher.email, "admin")

    return LoginResponseDTO(token, teacher.id).to_dict(), 200


# 🔹 Get Teacher by ID
def get_teacher_by_id(teacher_id):
    teacher = Teacher.query.get(teacher_id)

    if not teacher:
        return {"error": "Teacher not found"}, 404

    return TeacherOutDTO(teacher).to_dict(), 200


# 🔹 Get All Teachers
def get_all_teachers():
    teachers = Teacher.query.all()
    return [TeacherOutDTO(t).to_dict() for t in teachers], 200


# 🔹 Delete Teacher
def delete_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)

    if not teacher:
        return {"error": "Teacher not found"}, 404

    db.session.delete(teacher)
    db.session.commit()

    return {"message": "Teacher deleted successfully"}, 200

def update_teacher(teacher_id, data):
    teacher = Teacher.query.get(teacher_id)

    if not teacher:
        return {"error": "Teacher not found"}, 404

    teacher.first_name = data.get("firstName", teacher.first_name)
    teacher.last_name = data.get("lastName", teacher.last_name)
    teacher.subject_taught = data.get("subjectTaught", teacher.subject_taught)
    teacher.teaching_experience = data.get("teachingExperience", teacher.teaching_experience)
    teacher.school_name = data.get("schoolName", teacher.school_name)

    db.session.commit()

    return {"message": "Teacher updated successfully"}, 200