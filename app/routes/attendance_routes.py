from flask import Blueprint, request, jsonify
from app.auth.jwt_handler import get_email_from_request
from app.services.attendance_service import (
    mark_attendance,
    get_attendance_by_student,
    get_attendance_by_date,
    get_attendance_by_teacher
)

attendance_bp = Blueprint("attendance_bp", __name__)


# 🔒 Mark Attendance (PROTECTED)
@attendance_bp.route("/attendance", methods=["POST"])
def mark():
    email = get_email_from_request()
    if not email:
        return {"error": "Unauthorized"}, 401

    data = request.get_json()
    response, status = mark_attendance(data)
    return jsonify(response), status


# 🔒 Get by Student
@attendance_bp.route("/attendance/student/<int:student_id>", methods=["GET"])
def by_student(student_id):
    email = get_email_from_request()
    if not email:
        return {"error": "Unauthorized"}, 401

    response, status = get_attendance_by_student(student_id)
    return jsonify(response), status


# 🔒 Get by Date
@attendance_bp.route("/attendance/date/<string:date>", methods=["GET"])
def by_date(date):
    email = get_email_from_request()
    if not email:
        return {"error": "Unauthorized"}, 401

    response, status = get_attendance_by_date(date)
    return jsonify(response), status


# 🔒 Get by Teacher
@attendance_bp.route("/attendance/teacher/<int:teacher_id>", methods=["GET"])
def by_teacher(teacher_id):
    email = get_email_from_request()
    if not email:
        return {"error": "Unauthorized"}, 401

    response, status = get_attendance_by_teacher(teacher_id)
    return jsonify(response), status