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
| **Database** | PostgreSQL + SQLAlchemy (users, sessions, feedback) |
| **Storage** | AWS S3 (audio files) |
| **Deployment** | AWS ECS + RDS |

## Project structure

```
app/
├── main.py               # FastAPI app and routes
├── config.py             # pydantic-settings config
├── pipeline.py           # Orchestrates audio → features → RAG → feedback
├── audio/
│   ├── transcribe.py     # Whisper transcription
│   └── features.py       # librosa feature extraction (tempo, pitch, dynamics)
├── rag/
│   ├── retriever.py      # ChromaDB vector store + LangChain retriever
│   └── ingest.py         # Music theory knowledge base ingestion
├── agents/
│   └── coach_agent.py    # LLM feedback generation
└── db/
    ├── database.py       # Engine and session factory
    └── models.py         # User, Session, Feedback
```

## Setup

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # add OpenAI key, DB URL, AWS credentials
```

```bash
# Create tables
python3 -c "from app.db.database import engine; from app.db.models import Base; Base.metadata.create_all(engine)"

# Run locally
uvicorn app.main:app --reload
```

## Status

- [ ] Audio processing pipeline (Whisper + librosa)
- [ ] Music theory knowledge base + ChromaDB ingestion
- [ ] RAG retriever (LangChain + ChromaDB)
- [ ] Coach agent (LLM feedback generation)
- [ ] FastAPI endpoints (upload, feedback, history)
- [ ] PostgreSQL persistence (users, sessions, feedback)
- [ ] AWS deployment (ECS + RDS + S3)
