from flask import Blueprint, request, jsonify
from app.services.student_service import (
    create_student,
    get_all_students,
    get_student_by_id,
    update_student,
    delete_student
)
from app.dto.student_dto import StudentDTO
import logging

student_bp = Blueprint("student_bp", __name__, url_prefix="/api")

# Logging setup
logging.basicConfig(level=logging.INFO)


# CREATE
@student_bp.route("/students", methods=["POST"])
def add_student():
    try:
        data = request.get_json()

        if not data:
            logging.warning("No data provided in request")
            return jsonify({"error": "No data provided"}), 400

        name = data.get("name")
        age = data.get("age")

        if not name or not age:
            logging.warning("Missing name or age")
            return jsonify({"error": "Name and Age are required"}), 400

        logging.info(f"Creating student: {name}, Age: {age}")

        student = create_student(name, age)

        logging.info(f"Student created with ID: {student.id}")

        return jsonify({
            "status": "success",
            "data": StudentDTO(student).to_dict()
        }), 201

    except Exception as e:
        logging.error(f"Error creating student: {str(e)}")
        return jsonify({"error": str(e)}), 500


# GET ALL
@student_bp.route("/students", methods=["GET"])
def list_students():
    try:
        logging.info("Fetching all students")

        students = get_all_students()

        return jsonify({
            "status": "success",
            "data": [StudentDTO(s).to_dict() for s in students]
        }), 200

    except Exception as e:
        logging.error(f"Error fetching students: {str(e)}")
        return jsonify({"error": str(e)}), 500


# GET BY ID
@student_bp.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    try:
        logging.info(f"Fetching student with ID: {id}")

        student = get_student_by_id(id)

        if not student:
            logging.warning(f"Student not found with ID: {id}")
            return jsonify({"error": "Student not found"}), 404

        return jsonify({
            "status": "success",
            "data": StudentDTO(student).to_dict()
        }), 200

    except Exception as e:
        logging.error(f"Error fetching student: {str(e)}")
        return jsonify({"error": str(e)}), 500


# UPDATE
@student_bp.route("/students/<int:id>", methods=["PUT"])
def update_student_api(id):
    try:
        data = request.get_json()

        if not data:
            logging.warning("No data provided for update")
            return jsonify({"error": "No data provided"}), 400

        logging.info(f"Updating student ID: {id}")

        student = update_student(id, data)

        if not student:
            logging.warning(f"Student not found for update: {id}")
            return jsonify({"error": "Student not found"}), 404

        logging.info(f"Student updated: {id}")

        return jsonify({
            "status": "success",
            "data": StudentDTO(student).to_dict()
        }), 200

    except Exception as e:
        logging.error(f"Error updating student: {str(e)}")
        return jsonify({"error": str(e)}), 500


# DELETE
@student_bp.route("/students/<int:id>", methods=["DELETE"])
def delete_student_api(id):
    try:
        logging.info(f"Deleting student ID: {id}")

        result = delete_student(id)

        if not result:
            logging.warning(f"Student not found for deletion: {id}")
            return jsonify({"error": "Student not found"}), 404

        logging.info(f"Student deleted: {id}")

        return jsonify({
            "status": "success",
            "message": "Student deleted"
        }), 200

    except Exception as e:
        logging.error(f"Error deleting student: {str(e)}")
        return jsonify({"error": str(e)}), 500