import tempfile

from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.audio.features import extract_features
from app.audio.transcribe import transcribe
from app.rag.retriever import retrieve
from app.agents.coach_agent import generate_feedback
from app.db.database import get_db
from app.db.models import PracticeSession, Feedback

app = FastAPI(title="Maestro")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(audio: UploadFile = File(...), db: Session = Depends(get_db)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name

    transcript = transcribe(tmp_path)
    features = extract_features(tmp_path)
    context = retrieve(transcript)
    feedback_text = generate_feedback(transcript, features, context)

    session = PracticeSession(
        user_id="anonymous",
        audio_path=tmp_path,
        transcript=transcript,
        **features,
    )
    db.add(session)
    db.flush()

    db.add(Feedback(session_id=session.id, content=feedback_text))
    db.commit()

    return {
        "transcript": transcript,
        "features": features,
        "feedback": feedback_text,
    }
