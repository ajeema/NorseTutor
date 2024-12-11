FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install MFA (if pip installable) and ffmpeg
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install montreal-forced-aligner==2.2.0  # specify a known working version

COPY . .

ENV FLASK_APP=app.py

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
