from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, UserProgress, ConversationHistory
from services.stt_service import transcribe_audio_whisper
from services.llm_service import generate_llm_response
from services.tts_service import synthesize_speech
from services.pronunciation_scorer import run_forced_alignment, parse_textgrid_for_phonemes, compute_pronunciation_score, analyze_pitch, assess_performance
from utils.audio_utils import convert_webm_to_wav
from utils.phoneme_utils import get_expected_phonemes
import uuid
import os

conversation_bp = Blueprint('conversation', __name__)

@conversation_bp.route('/upload_audio', methods=['POST'])
@jwt_required()
def upload_audio():
    user_id = get_jwt_identity()
    prog = UserProgress.query.filter_by(user_id=user_id).first()
    if not prog:
        prog = UserProgress(user_id=user_id, difficulty_level=1)
        db.session.add(prog)
        db.session.commit()

    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    webm_filename = f"{uuid.uuid4()}.webm"
    webm_path = f"/tmp/{webm_filename}"
    audio_file.save(webm_path)

    wav_filename = f"{uuid.uuid4()}.wav"
    wav_path = f"/tmp/{wav_filename}"
    convert_webm_to_wav(webm_path, wav_path)

    user_text = transcribe_audio_whisper(wav_path)

    # Retrieve conversation history
    history_rows = (ConversationHistory.query
                    .filter_by(user_id=user_id)
                    .order_by(ConversationHistory.id.desc())
                    .limit(10)
                    .all())
    history = [{"role": h.role, "content": h.content} for h in reversed(history_rows)]

    llm_response = generate_llm_response(user_text, prog.difficulty_level, history)

    # Get expected phonemes for the given user_text
    # For demo, we assume a function get_expected_phonemes that returns a list of phonemes
    expected_phonemes = get_expected_phonemes(user_text)  # Implement as needed

    from config import Config
    textgrid_path = run_forced_alignment(
        wav_path, user_text, 
        dictionary_path=Config.MFA_DICTIONARY_PATH, 
        acoustic_model_path=Config.MFA_ACOUSTIC_MODEL_PATH, 
        output_dir=Config.MFA_OUTPUT_DIR
    )
    phoneme_intervals = parse_textgrid_for_phonemes(textgrid_path)
    pron_score = compute_pronunciation_score(phoneme_intervals, expected_phonemes)

    pitch_info = analyze_pitch(wav_path)
    was_successful = assess_performance(pron_score, pitch_info, prog.difficulty_level)

    prog.total_attempts += 1
    old_avg = prog.average_pronunciation_score
    new_avg = ((old_avg * (prog.total_attempts - 1)) + pron_score) / prog.total_attempts
    prog.average_pronunciation_score = new_avg

    if was_successful:
        prog.successful_attempts += 1
        if prog.successful_attempts % 3 == 0:
            prog.difficulty_level += 1

    db.session.commit()

    db.session.add(ConversationHistory(user_id=user_id, role="user", content=user_text))
    db.session.add(ConversationHistory(user_id=user_id, role="assistant", content=llm_response))
    db.session.commit()

    audio_url = synthesize_speech(llm_response)

    coaching_tip = ""
    if not was_successful:
        if pitch_info['range'] < 20.0:
            coaching_tip = "Prøv å variere intonasjonen litt mer."
        elif pron_score < 0.7:
            coaching_tip = "Forsøk å uttale ordene mer tydelig. Lytt nøye og gjenta."
        else:
            coaching_tip = "Prøv å uttale ordene litt langsommere og klarere."

    return jsonify({
        "user_text": user_text,
        "llm_response": llm_response,
        "difficulty": prog.difficulty_level,
        "audio_url": audio_url,
        "coaching_tip": coaching_tip,
        "pitch_info": pitch_info,
        "pronunciation_score": pron_score
    })
