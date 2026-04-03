from app import db

class SchoolClass(db.Model):
    __tablename__ = "school_classes"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Class Details
    grade = db.Column(db.String(50), nullable=False)
    section = db.Column(db.String(50), nullable=False)

    # Plain column — no ForeignKey until Teacher model is created
    teacher_id = db.Column(db.Integer, nullable=True)

    # Many-to-One → many classes = one teacher
    # @ManyToOne @JoinColumn(name = "teacher_id")
    # teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=True)
    # teacher_id = db.Column(db.Integer, nullable=True)
    # teacher = db.relationship("Teacher", backref="school_classes")

    # One-to-Many → one class = many students
    # @OneToMany(mappedBy = "schoolClass")
    # NOTE: 'students' backref is already defined in student_model.py
    # so we do NOT redefine it here — SQLAlchemy handles it automatically