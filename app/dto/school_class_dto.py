class SchoolClassDTO:
    def __init__(self, data=None, school_class=None):
        if data:
            # Input — replaces SchoolClassInDto
            self.grade = data.get("grade")
            self.section = data.get("section")
            self.teacherId = data.get("teacherId")

        elif school_class:
            # Output — replaces SchoolClassOutDto
            self.id = school_class.id
            self.grade = school_class.grade
            self.section = school_class.section
            self.teacherId = school_class.teacher_id

            # TODO: uncomment when Teacher model + relationship is added
            # self.teacherName = (
            #     school_class.teacher.full_name
            #     if school_class.teacher else None
            # )
            self.teacherName = None  # placeholder until Teacher model exists

            # counts related students
            self.studentCount = len(school_class.students) if school_class.students else 0

    def to_dict(self):
        return {
            "id": getattr(self, "id", None),
            "grade": self.grade,
            "section": self.section,
            "teacherId": self.teacherId,
            "teacherName": getattr(self, "teacherName", None),
            "studentCount": getattr(self, "studentCount", 0)
        }