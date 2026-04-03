from flask import Blueprint, request, jsonify
from app.services.school_class_service import SchoolClassService
from app.dto.school_class_dto import SchoolClassDTO

school_class_bp = Blueprint("school_class", __name__, url_prefix="/api/classes")
school_class_service = SchoolClassService()


# POST /api/classes/createClass
# @RequestBody → request.get_json() (JSON body)
@school_class_bp.route("/createClass", methods=["POST"])
def create_school_class():
    data = request.get_json()
    school_class_dto = SchoolClassDTO(data=data)
    created = school_class_service.create_school_class(school_class_dto)
    return jsonify(SchoolClassDTO(school_class=created).to_dict()), 201


# GET /api/classes/getClassById/<id>
@school_class_bp.route("/getClassById/<int:id>", methods=["GET"])
def get_school_class_by_id(id):
    school_class = school_class_service.get_school_class_by_id(id)
    return jsonify(SchoolClassDTO(school_class=school_class).to_dict()), 200


# GET /api/classes/getAllClasses
@school_class_bp.route("/getAllClasses", methods=["GET"])
def get_all_school_classes():
    classes = school_class_service.get_all_school_classes()
    return jsonify([SchoolClassDTO(school_class=c).to_dict() for c in classes]), 200


# PUT /api/classes/updateClass/<id>
# @RequestBody → request.get_json()
@school_class_bp.route("/updateClass/<int:id>", methods=["PUT"])
def update_school_class(id):
    data = request.get_json()
    school_class_dto = SchoolClassDTO(data=data)
    updated = school_class_service.update_school_class(id, school_class_dto)
    return jsonify(SchoolClassDTO(school_class=updated).to_dict()), 200


# DELETE /api/classes/deleteClass/<id>
# ResponseEntity.noContent().build() → return "", 204
@school_class_bp.route("/deleteClass/<int:id>", methods=["DELETE"])
def delete_school_class(id):
    school_class_service.delete_school_class(id)
    return "", 204