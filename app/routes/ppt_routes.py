import os
from flask import Blueprint, request, jsonify, send_file
from app.dto.ppt_dto import PPTRequestDTO
from app.services.ppt_service import generate_ppt
# Replace the top import line in app/routes/ppt_routes.py

from app.auth.jwt_handler import jwt_required as token_required

# reuse existing JWT guard

ppt_bp = Blueprint("ppt", __name__, url_prefix="/api/ppt")


@ppt_bp.route("/generate", methods=["POST"])
@token_required
def generate_ppt_route():
    """
    POST /api/ppt/generate
    Form-data fields:
      - file       : .txt or .pdf (required)
      - mode       : "auto" | "manual"  (default: "auto")
      - slide_count: int  (default: 8, used in auto mode)
      - slide_topics: JSON array string e.g. '["Topic A","Topic B"]' (used in manual mode)

    Returns the generated .pptx file as a download.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded. Send a .txt or .pdf as 'file' field."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename."}), 400

    allowed = (".txt", ".pdf")
    if not file.filename.lower().endswith(allowed):
        return jsonify({"error": "Only .txt and .pdf files are supported."}), 400

    dto = PPTRequestDTO.from_form(request.form)

    try:
        output_path = generate_ppt(
            file_storage=file,
            mode=dto.mode,
            slide_topics=dto.slide_topics,
            slide_count=dto.slide_count
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    return send_file(
        output_path,
        as_attachment=True,
        download_name=os.path.basename(output_path),
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )