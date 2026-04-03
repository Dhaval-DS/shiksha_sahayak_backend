from datetime import date
from flask import abort
from app import db
from app.models.assignment_model import Assignment
from app.models.school_class_model import SchoolClass


class AssignmentService:

    # ── CREATE ──────────────────────────────────────────────────────────────
    # replaces createAssignment(AssignmentInDto dto)
    def create_assignment(self, assignment_dto):

        # replaces schoolClassRepository.findById().orElseThrow()
        school_class = SchoolClass.query.get(assignment_dto.classId)
        if not school_class:
            abort(404, description=f"Class not found with id: {assignment_dto.classId}")

        # replaces AssignmentMapper.toEntity(dto, schoolClass)
        assignment = Assignment(
            title=assignment_dto.title,
            description=assignment_dto.description,
            # convert "YYYY-MM-DD" string from JSON to Python date object
            due_date=date.fromisoformat(assignment_dto.dueDate) if assignment_dto.dueDate else None,
            class_id=assignment_dto.classId
        )

        # replaces assignmentRepository.save(entity)
        db.session.add(assignment)
        db.session.commit()
        return assignment

    # ── GET ALL ──────────────────────────────────────────────────────────────
    # replaces getAllAssignments()
    def get_all_assignments(self):
        # replaces assignmentRepository.findAll()
        return Assignment.query.all()

    # ── GET BY ID ────────────────────────────────────────────────────────────
    # replaces getAssignmentById(Long id)
    def get_assignment_by_id(self, id):
        # replaces findById().orElseThrow()
        assignment = Assignment.query.get(id)
        if not assignment:
            abort(404, description=f"Assignment not found with id: {id}")
        return assignment

    # ── GET BY CLASS ─────────────────────────────────────────────────────────
    # replaces getAssignmentsByClass(Long classId)
    def get_assignments_by_class(self, class_id):
        # replaces assignmentRepository.findBySchoolClass_Id(classId)
        return Assignment.query.filter_by(class_id=class_id).all()

    # ── DELETE ───────────────────────────────────────────────────────────────
    # replaces deleteAssignment(Long id)
    def delete_assignment(self, id):
        assignment = Assignment.query.get(id)
        if not assignment:
            abort(404, description=f"Assignment not found with id: {id}")

        # replaces assignmentRepository.deleteById(id)
        db.session.delete(assignment)
        db.session.commit()