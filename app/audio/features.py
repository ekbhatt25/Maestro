import librosa


def extract_features(audio_path: str) -> dict:
    y, sr = librosa.load(audio_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return {"tempo_bpm": float(tempo)}
