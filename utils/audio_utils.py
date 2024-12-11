import uuid
import boto3
from pydub import AudioSegment
from config import Config

s3 = boto3.client('s3',
                  region_name=Config.AWS_REGION,
                  aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY)

def upload_to_s3(filename, data):
    s3.put_object(Bucket=Config.S3_BUCKET, Key=filename, Body=data, ContentType='audio/mpeg')
    return f"https://{Config.S3_BUCKET}.s3.amazonaws.com/{filename}"

def convert_webm_to_wav(input_path, output_path):
    audio = AudioSegment.from_file(input_path, format="webm")
    audio.export(output_path, format="wav")
