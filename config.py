import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change_me")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://user:pass@db:5432/mydb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    # Whisper API
    WHISPER_API_URL = "https://api.openai.com/v1/audio/transcriptions"

    # S3 Bucket for storing audio
    S3_BUCKET = os.environ.get("S3_BUCKET", "my-audio-bucket")

    # Redis URL (if used)
    REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")

    # TTS (Amazon Polly)
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

    # MFA paths
    MFA_DICTIONARY_PATH = os.environ.get("MFA_DICTIONARY_PATH", "/app/data/dictionary.txt")
    MFA_ACOUSTIC_MODEL_PATH = os.environ.get("MFA_ACOUSTIC_MODEL_PATH", "/app/data/acoustic_model/")
    MFA_OUTPUT_DIR = os.environ.get("MFA_OUTPUT_DIR", "/tmp/mfa_output")

    # Authentication (Placeholder)
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_API_AUDIENCE = os.environ.get("AUTH0_API_AUDIENCE")
