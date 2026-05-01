import whisper

_model = None


def get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")
    return _model


def transcribe(audio_path: str) -> str:
    result = get_model().transcribe(audio_path)
    return result["text"].strip()
