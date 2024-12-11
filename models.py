from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    user_id = db.Column(db.String, primary_key=True)
    difficulty_level = db.Column(db.Integer, default=1)
    successful_attempts = db.Column(db.Integer, default=0)
    total_attempts = db.Column(db.Integer, default=0)
    last_interaction = db.Column(db.DateTime, default=datetime.utcnow)
    average_pronunciation_score = db.Column(db.Float, default=0.0)

class ConversationHistory(db.Model):
    __tablename__ = 'conversation_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String, index=True)
    role = db.Column(db.String)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
