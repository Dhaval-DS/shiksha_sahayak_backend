class TestSpecificationDTO:
    def __init__(self, data):
        self.subject = data.get("subject")
        self.topics = data.get("topics")
        self.total_marks = data.get("totalMarks")
        self.difficulty = data.get("difficulty")
        self.num_questions = data.get("numQuestions")

    def to_dict(self):
        return {
            "subject": self.subject,
            "topics": self.topics,
            "totalMarks": self.total_marks,
            "difficulty": self.difficulty,
            "numQuestions": self.num_questions
        }


class GeneratedTestResponseDTO:
    def __init__(self, data):
        self.test_content = data.get("testContent")
        self.subject = data.get("subject")
        self.total_marks = data.get("totalMarks")
        self.num_questions = data.get("numQuestions")

    def to_dict(self):
        return {
            "testContent": self.test_content,
            "subject": self.subject,
            "totalMarks": self.total_marks,
            "numQuestions": self.num_questions
        }