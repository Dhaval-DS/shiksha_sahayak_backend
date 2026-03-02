from flask import Blueprint, request, jsonify
from app.services.student_service import create_student, get_all_students, get_student_by_id
from app.dto.student_dto import StudentDTO

student_bp = Blueprint("student_bp", __name__)

# GET all students
@student_bp.route("/students", methods=["GET"])
def list_students():
    students = get_all_students()
    dto_list = [StudentDTO(s).to_dict() for s in students]
    return jsonify(dto_list), 200

# POST create new student
@student_bp.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    student = create_student(data["name"], data["age"])
    dto = StudentDTO(student)
    return jsonify(dto.to_dict()), 201

