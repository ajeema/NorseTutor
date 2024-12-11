import parselmouth
from parselmouth.praat import call

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
