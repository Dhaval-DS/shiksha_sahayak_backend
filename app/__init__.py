from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from app.config import Config
    app.config.from_object(Config)
    from app.routes.chatbot_routes import chatbot_bp
    app.register_blueprint(chatbot_bp)

    CORS(app, origins=app.config["CORS_ORIGINS"])

    db.init_app(app)

    # Models in dependency order
    from app.models.school_class_model import SchoolClass
    from app.models.student_model import Student
    from app.models.assignment_model import Assignment
    from app.models.assignment_submission_model import AssignmentSubmission

    # Blueprints
    from app.routes.student_routes import student_bp
    from app.routes.school_class_routes import school_class_bp
    from app.routes.assignment_routes import assignment_bp
    from app.routes.assignment_submission_routes import assignment_submission_bp

    app.register_blueprint(student_bp)
    app.register_blueprint(school_class_bp)
    app.register_blueprint(assignment_bp)
    app.register_blueprint(assignment_submission_bp)

    with app.app_context():
        db.create_all()

    return app
