import boto3
import uuid
from config import Config
from utils.audio_utils import upload_to_s3

def synthesize_speech(text: str, voice_id="Liv"):
    polly = boto3.client('polly',
                         region_name=Config.AWS_REGION,
                         aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY)
    response = polly.synthesize_speech(OutputFormat='mp3', Text=text, VoiceId=voice_id, LanguageCode='nb-NO')
    audio_data = response['AudioStream'].read()
    filename = f"{uuid.uuid4()}.mp3"
    s3_url = upload_to_s3(filename, audio_data)
    return s3_url
