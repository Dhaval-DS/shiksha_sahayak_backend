from flask import Blueprint, request, jsonify
from app.services.assignment_service import AssignmentService
from app.dto.assignment_dto import AssignmentDTO

assignment_bp = Blueprint("assignment", __name__, url_prefix="/api/assignments")
assignment_service = AssignmentService()


# POST /api/assignments/create
# @RequestBody → request.get_json() (JSON body, not form-data)
@assignment_bp.route("/create", methods=["POST"])
def create_assignment():
    data = request.get_json()  # Java uses @RequestBody so it's JSON not form-data
    assignment_dto = AssignmentDTO(data=data)
    created = assignment_service.create_assignment(assignment_dto)
    return jsonify(AssignmentDTO(assignment=created).to_dict()), 200


# GET /api/assignments/getAllAssignments
@assignment_bp.route("/getAllAssignments", methods=["GET"])
def get_all_assignments():
    assignments = assignment_service.get_all_assignments()
    return jsonify([AssignmentDTO(assignment=a).to_dict() for a in assignments]), 200


# GET /api/assignments/<id>
# @PathVariable Long id → <int:id>
@assignment_bp.route("/<int:id>", methods=["GET"])
def get_assignment_by_id(id):
    assignment = assignment_service.get_assignment_by_id(id)
    return jsonify(AssignmentDTO(assignment=assignment).to_dict()), 200


# GET /api/assignments/class/<classId>
@assignment_bp.route("/class/<int:class_id>", methods=["GET"])
def get_assignments_by_class(class_id):
    assignments = assignment_service.get_assignments_by_class(class_id)
    return jsonify([AssignmentDTO(assignment=a).to_dict() for a in assignments]), 200


# DELETE /api/assignments/<id>
# ResponseEntity.noContent().build() → return "", 204
@assignment_bp.route("/<int:id>", methods=["DELETE"])
def delete_assignment(id):
    assignment_service.delete_assignment(id)
    return "", 204