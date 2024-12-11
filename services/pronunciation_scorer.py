import subprocess
import os
import textgrid
import parselmouth
from parselmouth.praat import call

def run_forced_alignment(audio_path, text, dictionary_path, acoustic_model_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    text_file = os.path.join(output_dir, base_name + ".txt")
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(text.strip() + "\n")

    audio_temp_dir = os.path.join(output_dir, "audio")
    os.makedirs(audio_temp_dir, exist_ok=True)

    audio_symlink = os.path.join(audio_temp_dir, os.path.basename(audio_path))
    if not os.path.exists(audio_symlink):
        os.symlink(audio_path, audio_symlink)

    # Run MFA
    cmd = [
        "mfa", "align",
        audio_temp_dir,
        dictionary_path,
        acoustic_model_path,
        output_dir,
        "--clean", "--quiet"
    ]
    subprocess.run(cmd, check=True)

    textgrid_path = os.path.join(output_dir, base_name + ".TextGrid")
    if not os.path.exists(textgrid_path):
        raise FileNotFoundError("TextGrid not found after alignment.")

    return textgrid_path

def parse_textgrid_for_phonemes(textgrid_path):
    tg = textgrid.TextGrid.fromFile(textgrid_path)
    phone_tier = [t for t in tg if t.name.lower() == "phones"]
    if not phone_tier:
        raise ValueError("No phone tier found in TextGrid.")
    phone_tier = phone_tier[0]
    phoneme_intervals = [(interval.mark, interval.minTime, interval.maxTime)
                         for interval in phone_tier.intervals if interval.mark.strip()]
    return phoneme_intervals

def compute_pronunciation_score(phoneme_intervals, expected_phonemes):
    # Simple heuristic: count how many expected phonemes appear with sufficient duration
    matched = 0
    for expected_phoneme in expected_phonemes:
        matches = [p for p in phoneme_intervals if p[0] == expected_phoneme]
        if matches:
            duration = matches[0][2] - matches[0][1]
            if duration > 0.03:
                matched += 1
    if len(expected_phonemes) == 0:
        return 1.0
    return matched / len(expected_phonemes)

def analyze_pitch(wav_path):
    sound = parselmouth.Sound(wav_path)
    pitch = call(sound, "To Pitch", 0.0, 75, 600)
    min_p = call(pitch, "Get minimum", 0, 0, "Hertz", "Parabolic")
    max_p = call(pitch, "Get maximum", 0, 0, "Hertz", "Parabolic")
    mean_p = call(pitch, "Get mean", 0, 0, "Hertz")
    return {
        "min_pitch": min_p,
        "max_pitch": max_p,
        "mean_pitch": mean_p,
        "range": max_p - min_p
    }

def assess_performance(pron_score, pitch_info, difficulty):
    success = pron_score > 0.7
    if difficulty > 3 and pitch_info['range'] < 20.0:
        success = False
    return success
