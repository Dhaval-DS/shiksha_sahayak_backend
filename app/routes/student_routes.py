from flask import Blueprint, request, jsonify
from app.services.student_service import StudentService
from app.dto.student_dto import StudentDTO

student_bp = Blueprint("student", __name__, url_prefix="/api/students")
student_service = StudentService()


# POST /api/students/createStudent
@student_bp.route("/createStudent", methods=["POST"])
def create_student():
    data = request.form.to_dict()
    photo = request.files.get("photo")  # optional

    student_dto = StudentDTO(data=data)

    created_student = student_service.create_student(student_dto)

    if photo and photo.filename != "":
        student_service.upload_student_photo(created_student.id, photo)

    return jsonify(StudentDTO(student=created_student).to_dict()), 201


# GET /api/students/getStudentById/<id>
@student_bp.route("/getStudentById/<int:id>", methods=["GET"])
def get_student_by_id(id):
    student = student_service.get_student_by_id(id)
    return jsonify(StudentDTO(student=student).to_dict()), 200


# GET /api/students/getAllStudents?classId=<classId>
@student_bp.route("/getAllStudents", methods=["GET"])
def get_all_students():
    class_id = request.args.get("classId", type=int)  # optional query param
    students = student_service.get_all_students(class_id)
    return jsonify([StudentDTO(student=s).to_dict() for s in students]), 200


# PUT /api/students/updateStudent/<id>
@student_bp.route("/updateStudent/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.form.to_dict()
    photo = request.files.get("photo")  # optional

    student_dto = StudentDTO(data=data)

    updated_student = student_service.update_student(id, student_dto)

    if photo and photo.filename != "":
        student_service.upload_student_photo(updated_student.id, photo)

    return jsonify(StudentDTO(student=updated_student).to_dict()), 200


# DELETE /api/students/deleteStudent/<id>
@student_bp.route("/deleteStudent/<int:id>", methods=["DELETE"])
def delete_student(id):
    student_service.delete_student(id)
    return "", 204


# POST /api/students/StudentPhoto/<id>
@student_bp.route("/StudentPhoto/<int:id>", methods=["POST"])
def upload_photo(id):
    file = request.files.get("file")
    if not file or file.filename == "":
        return jsonify({"error": "No file provided"}), 400

    student_service.upload_student_photo(id, file)
    return jsonify({"message": "Photo uploaded successfully"}), 200


# GET /api/students/StudentPhoto/<id>
@student_bp.route("/StudentPhoto/<int:id>", methods=["GET"])
def get_photo(id):
    return student_service.get_student_photo(id)