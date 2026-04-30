import librosa
import numpy as np


def extract_features(audio_path: str) -> dict:
    y, sr = librosa.load(audio_path) # store audio in numpy array

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr) # estimate tempo
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_hz = float(pitches[magnitudes > magnitudes.mean()].mean()) if magnitudes.any() else 0.0 # most confident pitch candidates
    dynamic_rms = float(np.mean(librosa.feature.rms(y=y))) # avg loudness across track

    return {
        "tempo_bpm": float(tempo),
        "pitch_hz": round(pitch_hz, 2),
        "dynamic_rms": round(dynamic_rms, 4),
    }
