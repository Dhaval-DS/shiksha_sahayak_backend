from google import genai
from app.dto.testpaper_dto import TestSpecificationDTO, GeneratedTestResponseDTO

GEMINI_API_KEY = "AIzaSyCcY-pjt7SEFNSOkKhRBcrICNzTkXVDaiE"  # ← paste your key here

client = genai.Client(api_key=GEMINI_API_KEY)


# 🔹 Generate Test
def generate_test(data):
    dto = TestSpecificationDTO(data)

    prompt = f"""
    Generate a test paper for the following specifications:
    - Subject: {dto.subject}
    - Topics: {dto.topics}
    - Total Marks: {dto.total_marks}
    - Difficulty: {dto.difficulty}
    - Number of Questions: {dto.num_questions}

    Format the output clearly with question numbers, marks for each question.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        result = {
            "testContent": response.text,
            "subject": dto.subject,
            "totalMarks": dto.total_marks,
            "numQuestions": dto.num_questions
        }
        return GeneratedTestResponseDTO(result).to_dict(), 200
    except Exception as e:
        return {"error": str(e)}, 500