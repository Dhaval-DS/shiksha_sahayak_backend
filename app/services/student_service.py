import magic  # pip install python-magic
from flask import abort, Response
from app import db
from app.models.student_model import Student
from app.dto.student_dto import StudentDTO


class StudentService:

    # ── CREATE ──────────────────────────────────────────────────────────────
    def create_student(self, student_dto):
        # Check if the class exists (replaces schoolClassRepository.findById)
        from app.models.school_class_model import SchoolClass
        school_class = SchoolClass.query.get(student_dto.classId)
        if not school_class:
            abort(404, description=f"SchoolClass not found with id: {student_dto.classId}")

        # Build the Student model from DTO (replaces StudentMapper.toEntity)
        student = Student(
            first_name=student_dto.firstName,
            last_name=student_dto.lastName,
            roll_number=student_dto.rollNumber,
            age=int(student_dto.age) if student_dto.age else None,  # convert string to int
            parent_name=student_dto.parentName,
            parent_contact=int(student_dto.parentContact) if student_dto.parentContact else None,
            parent_email=student_dto.parentEmail,
            parent_preferred_language=student_dto.parentPreferredLanguage,
            class_id=int(student_dto.classId) if student_dto.classId else None
        )

        db.session.add(student)
        db.session.commit()
        return student  # routes will wrap this in StudentDTO

    # ── GET BY ID ────────────────────────────────────────────────────────────
    def get_student_by_id(self, id):
        student = Student.query.get(id)
        if not student:
            abort(404, description=f"Student not found with id: {id}")
        return student

    # ── GET ALL (optional filter by classId) ────────────────────────────────
    def get_all_students(self, class_id=None):
        if class_id is not None:
            # replaces studentRepository.findBySchoolClass_Id(classId)
            students = Student.query.filter_by(class_id=class_id).all()
        else:
            students = Student.query.all()
        return students

    # ── UPDATE ───────────────────────────────────────────────────────────────
    def update_student(self, id, student_dto):
        # Find existing student
        student = Student.query.get(id)
        if not student:
            abort(404, description=f"Student not found with id: {id}")

        # Validate school class exists
        from app.models.school_class_model import SchoolClass
        school_class = SchoolClass.query.get(student_dto.classId)
        if not school_class:
            abort(404, description=f"SchoolClass not found with id: {student_dto.classId}")

        # Update fields (replaces all the existingStudent.setXxx() calls)
        student.first_name = student_dto.firstName
        student.last_name = student_dto.lastName
        student.roll_number = student_dto.rollNumber
        student.age = student_dto.age
        student.parent_name = student_dto.parentName
        student.parent_contact = student_dto.parentContact
        student.parent_email = student_dto.parentEmail
        student.parent_preferred_language = student_dto.parentPreferredLanguage
        student.class_id = student_dto.classId

        db.session.commit()
        return student

    # ── DELETE ───────────────────────────────────────────────────────────────
    def delete_student(self, id):
        student = Student.query.get(id)
        if not student:
            abort(404, description=f"Student not found with id: {id}")

        db.session.delete(student)
        db.session.commit()

    # ── UPLOAD PHOTO ─────────────────────────────────────────────────────────
    def upload_student_photo(self, id, file):
        student = Student.query.get(id)
        if not student:
            abort(404, description="Student not found")

        # replaces file.getBytes() + IOException handling
        try:
            student.photo = file.read()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error uploading photo: {str(e)}")

    # ── GET PHOTO ─────────────────────────────────────────────────────────────
    def get_student_photo(self, id):
        student = Student.query.get(id)
        if not student:
            abort(404, description="Student not found")

        if student.photo is None:
            abort(404, description="No photo found for this student")

        # Detect MIME type from bytes (replaces URLConnection.guessContentTypeFromStream)
        try:
            mime_type = magic.from_buffer(student.photo, mime=True)
            if not mime_type:
                mime_type = "application/octet-stream"
        except Exception:
            mime_type = "application/octet-stream"

        # Returns a Flask Response with image bytes (replaces ResponseEntity<byte[]>)
        return Response(
            student.photo,
            status=200,
            mimetype=mime_type
        )

