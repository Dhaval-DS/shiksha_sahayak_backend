class PPTRequestDTO:
    def __init__(self, mode: str, slide_topics: list = None, slide_count: int = None):
        """
        mode: 'auto' | 'manual'
        slide_topics: list of topic strings (used in manual mode)
        slide_count: number of slides to generate (used in auto mode)
        """
        self.mode = mode
        self.slide_topics = slide_topics or []
        self.slide_count = slide_count or 8

    @staticmethod
    def from_form(form_data: dict):
        import json
        mode = form_data.get("mode", "auto")
        slide_count = int(form_data.get("slide_count", 8))
        raw_topics = form_data.get("slide_topics", "[]")
        try:
            slide_topics = json.loads(raw_topics) if isinstance(raw_topics, str) else raw_topics
        except Exception:
            slide_topics = []
        return PPTRequestDTO(mode=mode, slide_topics=slide_topics, slide_count=slide_count)


class PPTResponseDTO:
    def __init__(self, success: bool, file_path: str = None, message: str = None):
        self.success = success
        self.file_path = file_path
        self.message = message

    def to_dict(self):
        return {
            "success": self.success,
            "file_path": self.file_path,
            "message": self.message
        }