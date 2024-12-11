from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import User, db
import uuid

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(user_id=str(uuid.uuid4()), email=email)
        db.session.add(user)
        db.session.commit()

    token = create_access_token(identity=user.user_id)
    return jsonify({"access_token": token})
