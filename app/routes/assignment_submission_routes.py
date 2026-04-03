from flask import Blueprint, request, jsonify
from app.services.assignment_submission_service import AssignmentSubmissionService
from app.dto.assignment_submission_dto import AssignmentSubmissionDTO

assignment_submission_bp = Blueprint(
    "assignment_submission",
    __name__,
    url_prefix="/api/submissions"
)
submission_service = AssignmentSubmissionService()


# POST /api/submissions/submit
# @RequestBody → request.get_json() (JSON body)
@assignment_submission_bp.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    submission_dto = AssignmentSubmissionDTO(data=data)
    created = submission_service.submit_assignment(submission_dto)
    return jsonify(AssignmentSubmissionDTO(submission=created).to_dict()), 200


# GET /api/submissions/assignment/<assignmentId>
# @PathVariable Long assignmentId → <int:assignment_id>
@assignment_submission_bp.route("/assignment/<int:assignment_id>", methods=["GET"])
def get_by_assignment(assignment_id):
    submissions = submission_service.get_submissions_by_assignment(assignment_id)
    return jsonify([AssignmentSubmissionDTO(submission=s).to_dict() for s in submissions]), 200