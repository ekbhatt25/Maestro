import tempfile

from fastapi import FastAPI, UploadFile, File

from app.audio.features import extract_features
from app.audio.transcribe import transcribe
from app.rag.retriever import retrieve
from app.agents.coach_agent import generate_feedback

app = FastAPI(title="Maestro")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(audio: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name

    transcript = transcribe(tmp_path)
    features = extract_features(tmp_path)
    context = retrieve(transcript)
    feedback = generate_feedback(transcript, features, context)

    return {
        "transcript": transcript,
        "features": features,
        "feedback": feedback,
    }
