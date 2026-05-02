import requests
from flask import Blueprint, request, jsonify, current_app
from langdetect import detect

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/api/ChatBot")

SYSTEM_PROMPT = """You are ShikshaSahayak, a helpful AI assistant for rural school teachers in India.

CRITICAL LANGUAGE RULES — YOU MUST FOLLOW THESE STRICTLY:
- Detect the language of the teacher's message
- If the message is in English → reply ONLY in English
- If the message is in Hindi → reply ONLY in Hindi (Devanagari script)
- If the message is in Marathi → reply ONLY in Marathi (Devanagari script)
- NEVER reply in a different language than the one used in the message
- NEVER mix languages in your response

YOUR ROLE:
- Help teachers with lesson planning and teaching methods
- Answer subject doubts (Math, Science, English, Hindi, Marathi)
- Suggest activities suitable for rural classroom settings
- Support teachers who may have limited resources
- Give short, clear, practical answers"""


@chatbot_bp.route("", methods=["GET"])
def get_chat_response():
    message = request.args.get("message")

    if not message:
        return jsonify({"error": "message parameter is required"}), 400

    try:
        # Detect language
        try:
            detected_lang = detect(message)
        except Exception:
            detected_lang = "en"

        lang_map = {
            "hi": "Hindi",
            "mr": "Marathi",
            "en": "English"
        }
        language = lang_map.get(detected_lang, "English")

        # Force language in user message explicitly
        forced_message = f"[IMPORTANT: Reply strictly in {language} only. Do not use any other language.]\n\n{message}"

        api_key = current_app.config["OPENROUTER_API_KEY"]
        api_url = current_app.config["OPENROUTER_API_URL"]
        model = current_app.config["OPENROUTER_MODEL"]

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://shiksha-sahayak.ai",
            "X-Title": "ShikshaSahayak ChatBot"
        }

        body = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": forced_message}
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }

        response = requests.post(api_url, json=body, headers=headers, timeout=30)
        response_data = response.json()

        if "error" in response_data:
            return jsonify({"error": str(response_data["error"])}), 500

        if "choices" in response_data and len(response_data["choices"]) > 0:
            content = response_data["choices"][0]["message"]["content"]
            return jsonify({
                "response": content,
                "detectedLanguage": language
            }), 200

        return jsonify({"response": "No response received from the model."}), 200

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out. Please try again."}), 504

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# POST endpoint for voice
@chatbot_bp.route("/voice", methods=["POST"])
def get_voice_chat_response():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "message is required in request body"}), 400
    message = data.get("message")
    with current_app.test_request_context(
        f'/api/ChatBot?message={message}'
    ):
        from flask import request as test_request
    request.environ['QUERY_STRING'] = f'message={message}'
    return get_chat_response()