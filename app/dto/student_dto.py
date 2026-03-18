class StudentDTO:
    def __init__(self, student):
        self.id = student.id
        self.name = student.name
        self.age = student.age

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age
        }