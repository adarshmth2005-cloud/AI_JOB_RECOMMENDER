
from flask import Blueprint, request, jsonify, current_app
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from sqlalchemy import func
from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def get_serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not name or not email or not password:
        return jsonify({
            "status": "error",
            "message": "Name, email and password are required."
        }), 400

    if len(password) < 8:
        return jsonify({
            "status": "error",
            "message": "Password must be at least 8 characters."
        }), 400

    if "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({
            "status": "error",
            "message": "Please enter a valid email address."
        }), 400

    existing_user = User.query.filter(
        func.lower(User.email) == email
    ).first()

    if existing_user:
        return jsonify({
            "status": "error",
            "message": "This email is already registered."
        }), 409

    user = User(name=name, email=email)
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Registration failed. Please try again."
        }), 500

    return jsonify({
        "status": "success",
        "message": "Registration successful.",
        "user": user.to_dict()
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({
            "status": "error",
            "message": "Email and password are required."
        }), 400

    user = User.query.filter(
        func.lower(User.email) == email
    ).first()

    if not user or not user.check_password(password):
        return jsonify({
            "status": "error",
            "message": "Invalid email or password."
        }), 401

    token = get_serializer().dumps({
        "user_id": user.id
    })

    return jsonify({
        "status": "success",
        "message": "Login successful.",
        "token": token,
        "user": user.to_dict()
    }), 200


@auth_bp.route("/verify", methods=["GET"])
def verify_token():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return jsonify({
            "status": "error",
            "message": "Authentication token is missing."
        }), 401

    token = auth_header.split(" ", 1)[1].strip()

    try:
        payload = get_serializer().loads(token, max_age=86400)
    except SignatureExpired:
        return jsonify({
            "status": "error",
            "message": "Session expired. Please login again."
        }), 401
    except BadSignature:
        return jsonify({
            "status": "error",
            "message": "Invalid authentication token."
        }), 401

    user = db.session.get(User, payload.get("user_id"))

    if not user:
        return jsonify({
            "status": "error",
            "message": "User not found."
        }), 404

    return jsonify({
        "status": "success",
        "user": user.to_dict()
    }), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    # Token-based logout is completed on the frontend
    # by deleting the saved token.
    return jsonify({
        "status": "success",
        "message": "Logout successful. Please clear the saved token."
    }), 200
