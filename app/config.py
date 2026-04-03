# app/config.py
import os

class Config:
    # SQLite DB file will be created in project root
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '..','instance' ,'database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = ["http://localhost:5174"]  # Your frontend URL