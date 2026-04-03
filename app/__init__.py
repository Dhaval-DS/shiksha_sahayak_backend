# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from app.config import Config
    app.config.from_object(Config)

    CORS(app, origins=app.config["CORS_ORIGINS"])

    db.init_app(app)

    # Import models so tables get created ← THIS PART IS CRITICAL
    from app.models.student_model import Student
    from app.models.teacher_model import Teacher
    from app.models.attendance_model import AttendanceRecord
    from app.routes.ppt_routes import ppt_bp
    # Register routes
    from app.routes.student_routes import student_bp
    app.register_blueprint(student_bp, url_prefix="/api")

    from app.routes.teacher_routes import teacher_bp
    app.register_blueprint(teacher_bp, url_prefix="/api")

    from app.routes.attendance_routes import attendance_bp
    app.register_blueprint(attendance_bp, url_prefix="/api")

    from app.routes.test_routes import test_bp
    app.register_blueprint(test_bp, url_prefix="/api")

    from app.routes.ppt_routes import ppt_bp
    app.register_blueprint(ppt_bp)

    return app