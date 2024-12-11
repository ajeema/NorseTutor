import requests
from config import Config

def transcribe_audio_whisper(file_path: str) -> str:
    headers = {
        "Authorization": f"Bearer {Config.OPENAI_API_KEY}"
    }
    files = {
        "file": open(file_path, "rb")
    }
    data = {
        "model": "whisper-1",
        "language": "no"
    }
    response = requests.post(Config.WHISPER_API_URL, headers=headers, files=files, data=data)
    response.raise_for_status()
    transcript = response.json()["text"].strip()
    return transcript
