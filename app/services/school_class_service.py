from flask import abort
from app import db
from app.models.school_class_model import SchoolClass


class SchoolClassService:

    # ── CREATE ──────────────────────────────────────────────────────────────
    # replaces createSchoolClass(SchoolClassInDto classDto)
    def create_school_class(self, class_dto):

        # TODO: uncomment when Teacher model is created
        # replaces teacherRepository.findById().orElseThrow()
        # from app.models.teacher_model import Teacher
        # teacher = Teacher.query.get(class_dto.teacherId)
        # if not teacher:
        #     abort(404, description=f"Teacher not found with id: {class_dto.teacherId}")

        # replaces SchoolClassMapper.toEntity(classDto, teacher)
        new_class = SchoolClass(
            grade=class_dto.grade,
            section=class_dto.section,
            teacher_id=class_dto.teacherId  # stored as plain id for now
        )

        # replaces schoolClassRepository.save(newClass)
        db.session.add(new_class)
        db.session.commit()
        return new_class

    # ── GET BY ID ────────────────────────────────────────────────────────────
    # replaces getSchoolClassById(Long id)
    def get_school_class_by_id(self, id):
        # replaces schoolClassRepository.findById().orElseThrow()
        school_class = SchoolClass.query.get(id)
        if not school_class:
            abort(404, description=f"SchoolClass not found with id: {id}")
        return school_class

    # ── GET ALL ──────────────────────────────────────────────────────────────
    # replaces getAllSchoolClasses()
    def get_all_school_classes(self):
        # replaces schoolClassRepository.findAll()
        return SchoolClass.query.all()

    # ── UPDATE ───────────────────────────────────────────────────────────────
    # replaces updateSchoolClass(Long id, SchoolClassInDto classDto)
    def update_school_class(self, id, class_dto):
        # replaces schoolClassRepository.findById().orElseThrow()
        existing_class = SchoolClass.query.get(id)
        if not existing_class:
            abort(404, description=f"SchoolClass not found with id: {id}")

        # TODO: uncomment when Teacher model is created
        # replaces teacherRepository.findById().orElseThrow()
        # from app.models.teacher_model import Teacher
        # teacher = Teacher.query.get(class_dto.teacherId)
        # if not teacher:
        #     abort(404, description=f"Teacher not found with id: {class_dto.teacherId}")

        # replaces existingClass.setGrade(), setSection(), setTeacher()
        existing_class.grade = class_dto.grade
        existing_class.section = class_dto.section
        existing_class.teacher_id = class_dto.teacherId  # stored as plain id for now

        # replaces schoolClassRepository.save(existingClass)
        db.session.commit()
        return existing_class

    # ── DELETE ───────────────────────────────────────────────────────────────
    # replaces deleteSchoolClass(Long id)
    def delete_school_class(self, id):
        # replaces schoolClassRepository.existsById(id)
        existing_class = SchoolClass.query.get(id)
        if not existing_class:
            abort(404, description=f"SchoolClass not found with id: {id}")

        # replaces schoolClassRepository.deleteById(id)
        db.session.delete(existing_class)
        db.session.commit()
