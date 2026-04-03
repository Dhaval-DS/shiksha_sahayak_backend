from app import db
from app.models.attendance_model import AttendanceRecord


# 🔹 Mark Attendance
def mark_attendance(data):
    record = AttendanceRecord(
        date=data.get("date"),
        status=data.get("status"),
        student_id=data.get("studentId"),
        teacher_id=data.get("teacherId"),
        class_id=data.get("classId")
    )
    db.session.add(record)
    db.session.commit()
    return {"message": "Attendance marked successfully"}, 201


# 🔹 Get Attendance by Student
def get_attendance_by_student(student_id):
    records = AttendanceRecord.query.filter_by(student_id=student_id).all()
    return [to_dict(r) for r in records], 200


# 🔹 Get Attendance by Date
def get_attendance_by_date(date):
    records = AttendanceRecord.query.filter_by(date=date).all()
    return [to_dict(r) for r in records], 200


# 🔹 Get Attendance by Teacher
def get_attendance_by_teacher(teacher_id):
    records = AttendanceRecord.query.filter_by(teacher_id=teacher_id).all()
    return [to_dict(r) for r in records], 200


# 🔹 Helper
def to_dict(record):
    return {
        "id": record.id,
        "date": record.date,
        "status": record.status,
        "studentId": record.student_id,
        "teacherId": record.teacher_id,
        "classId": record.class_id
    }