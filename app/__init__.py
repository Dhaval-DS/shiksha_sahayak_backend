# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load config
    from app.config import Config
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, origins=app.config["CORS_ORIGINS"])

    # Initialize DB
    db.init_app(app)

    # Register routes
    from app.routes.student_routes import student_bp
    app.register_blueprint(student_bp, url_prefix="/api")

    return app