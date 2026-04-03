from datetime import datetime
from flask import abort
from app import db
from app.models.assignment_submission_model import AssignmentSubmission
from app.models.assignment_model import Assignment
from app.models.student_model import Student


class AssignmentSubmissionService:

    # ── SUBMIT ASSIGNMENT ────────────────────────────────────────────────────
    # replaces submitAssignment(AssignmentSubmissionInDto dto)
    def submit_assignment(self, submission_dto):

        # replaces assignmentRepository.findById().orElseThrow()
        assignment = Assignment.query.get(submission_dto.assignmentId)
        if not assignment:
            abort(404, description=f"Assignment not found with id: {submission_dto.assignmentId}")

        # replaces studentRepository.findById().orElseThrow()
        student = Student.query.get(submission_dto.studentId)
        if not student:
            abort(404, description=f"Student not found with id: {submission_dto.studentId}")

        # replaces AssignmentSubmissionMapper.toEntity(dto, assignment, student)
        submission = AssignmentSubmission(
            assignment_id=submission_dto.assignmentId,
            student_id=submission_dto.studentId,
            grade=submission_dto.grade,
            comment=submission_dto.comment,
            file_url=submission_dto.fileUrl,
            # replaces LocalDateTime — auto set to current time
            submitted_at=datetime.utcnow()
        )

        # replaces submissionRepository.save(entity)
        db.session.add(submission)
        db.session.commit()
        return submission

    # ── GET SUBMISSIONS BY ASSIGNMENT ────────────────────────────────────────
    # replaces getSubmissionsByAssignment(Long assignmentId)
    def get_submissions_by_assignment(self, assignment_id):
        # replaces submissionRepository.findByAssignmentId(assignmentId)
        return AssignmentSubmission.query.filter_by(
            assignment_id=assignment_id
        ).all()
