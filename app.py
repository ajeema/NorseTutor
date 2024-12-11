from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from config import Config
from utils.db import init_db
from routes.auth import auth_bp
from routes.conversation import conversation_bp
from routes.progress import progress_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    init_db(app)

    jwt = JWTManager(app)

    @app.route('/')
    def index():
        return "Norwegian Coaching App Running"

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(conversation_bp, url_prefix="/conversation")
    app.register_blueprint(progress_bp, url_prefix="/progress")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
