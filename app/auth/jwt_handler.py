import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 60


# 🔹 Create JWT token
def create_token(email, role):
    payload = {
        "sub": email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


# 🔹 Verify JWT token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None


# 🔹 Protect routes with JWT
def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "success": False,
                "message": "Authorization header missing"
            }), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({
                "success": False,
                "message": "Invalid Authorization format. Use: Bearer <token>"
            }), 401

        token = auth_header.split(" ")[1]
        payload = verify_token(token)

        if not payload:
            return jsonify({
                "success": False,
                "message": "Invalid or expired token"
            }), 401

        request.user_email = payload.get("sub")
        request.user_role = payload.get("role")

        return f(*args, **kwargs)

    return decorated


# 🔹 Get email from request
def get_email_from_request():
    return getattr(request, "user_email", None)


# 🔹 Get role from request
def get_role_from_request():
    return getattr(request, "user_role", None)