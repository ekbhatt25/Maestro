import tempfile

from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.audio.features import extract_features
from app.audio.transcribe import transcribe
from app.rag.retriever import retrieve
from app.agents.coach_agent import generate_feedback
from app.auth import get_current_user_id
from app.db.database import get_db
from app.db.models import PracticeSession, Feedback

app = FastAPI(title="Maestro")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(
    audio: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name

    transcript = transcribe(tmp_path)
    features = extract_features(tmp_path)
    context = retrieve(transcript, features)
    feedback_text = generate_feedback(transcript, features, context)

    session = PracticeSession(
        user_id=user_id,
        audio_path=tmp_path,
        transcript=transcript,
        **features,
    )
    db.add(session)
    db.flush()

    db.add(Feedback(session_id=session.id, content=feedback_text))
    db.commit()

    return {
        "session_id": session.id,
        "transcript": transcript,
        "features": features,
        "feedback": feedback_text,
    }


@app.get("/sessions")
def get_sessions(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    sessions = (
        db.query(PracticeSession)
        .filter(PracticeSession.user_id == user_id)
        .order_by(PracticeSession.created_at.desc())
        .all()
    )
    return [
        {
            "id": s.id,
            "created_at": s.created_at,
            "tempo_bpm": s.tempo_bpm,
            "pitch_hz": s.pitch_hz,
            "dynamic_rms": s.dynamic_rms,
            "feedback": s.feedback[0].content if s.feedback else None,
        }
        for s in sessions
    ]
