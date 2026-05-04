# Maestro

**AI-powered music practice coach.** Record yourself playing, get instant feedback on technique, timing, and theory — like having a teacher available 24/7.

## What it does

1. User uploads an audio recording (voice or instrument)
2. Whisper transcribes and librosa extracts audio features (tempo, pitch, dynamics)
3. A RAG pipeline retrieves relevant music theory and technique context
4. An LLM generates personalized, structured feedback
5. Progress is tracked over time across sessions

## Stack

| | |
|---|---|
| **Framework** | FastAPI |
| **Audio processing** | Whisper (transcription), librosa (feature extraction) |
| **RAG pipeline** | LangChain + ChromaDB + sentence-transformers (embeddings) |
| **LLM** | Groq (llama-3.3-70b-versatile) |
| **Auth + Database** | Supabase (auth, PostgreSQL, free tier) |
| **ORM** | SQLAlchemy + Alembic |
| **Storage** | AWS S3 (audio files) |
| **Deployment** | AWS ECS |

## Project structure

```
main.py                   # FastAPI app and routes
app/
├── config.py             # pydantic-settings config
├── audio/
│   ├── transcribe.py     # Whisper transcription
│   └── features.py       # librosa feature extraction (tempo, pitch, dynamics)
├── rag/
│   ├── retriever.py      # ChromaDB similarity search
│   └── ingest.py         # Music theory knowledge base ingestion
├── agents/
│   └── coach_agent.py    # LLM feedback generation
└── db/
    ├── database.py       # Engine and session factory
    └── models.py         # PracticeSession, Feedback
```

## Setup

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # add Groq key, Supabase credentials, AWS credentials
```

```bash
# Ingest music theory docs into ChromaDB
python3 -c "from app.rag.ingest import ingest; ingest()"

# Create tables
python3 -c "from app.db.database import engine; from app.db.models import Base; Base.metadata.create_all(engine)"

# Run locally
uvicorn main:app --reload
```

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Server health check |
| `POST` | `/analyze` | Upload audio, get back transcript, features, and coach feedback |

## Status

- [x] Project config (pydantic-settings)
- [x] Database models (PracticeSession, Feedback)
- [x] Database engine + session factory
- [x] Audio processing pipeline (Whisper + librosa)
- [x] Music theory knowledge base + ChromaDB ingestion
- [x] RAG retriever (ChromaDB similarity search)
- [x] Coach agent (Groq LLM feedback generation)
- [x] FastAPI endpoints (`/health`, `/analyze`)
- [ ] Auth (Supabase user ID)
- [ ] AWS S3 storage + deployment
