from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import UserProgress

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/stats', methods=['GET'])
@jwt_required()
def stats():
    user_id = get_jwt_identity()
    p = UserProgress.query.filter_by(user_id=user_id).first()
    if p is None:
        return jsonify({"error": "No progress found"}), 404
    return jsonify({
        "difficulty_level": p.difficulty_level,
        "successful_attempts": p.successful_attempts,
        "total_attempts": p.total_attempts,
        "average_pronunciation_score": p.average_pronunciation_score
    })

@progress_bp.route('/reset', methods=['POST'])
@jwt_required()
def reset_progress():
    user_id = get_jwt_identity()
    from models import db, ConversationHistory
    UserProgress.query.filter_by(user_id=user_id).delete()
    ConversationHistory.query.filter_by(user_id=user_id).delete()
    p = UserProgress(user_id=user_id, difficulty_level=1, successful_attempts=0, total_attempts=0)
    db.session.add(p)
    db.session.commit()
    return jsonify({"status": "reset", "difficulty": 1})
