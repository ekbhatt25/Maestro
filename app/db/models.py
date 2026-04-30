from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False)  # Supabase auth UUID
    audio_path: Mapped[str] = mapped_column(String(512), nullable=False)
    transcript: Mapped[str | None] = mapped_column(Text)
    tempo_bpm: Mapped[float | None] = mapped_column(Float)
    pitch_hz: Mapped[float | None] = mapped_column(Float)
    dynamic_rms: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    feedback: Mapped[list["Feedback"]] = relationship(back_populates="session")


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("practice_sessions.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session: Mapped["PracticeSession"] = relationship(back_populates="feedback")
