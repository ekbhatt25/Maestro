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
| **Auth + Database** | Supabase (auth, PostgreSQL) |
| **ORM** | SQLAlchemy + Alembic |
| **Frontend** | Next.js + Tailwind CSS (Vercel) |
| **Deployment** | Render (backend + Postgres) |

## Project structure

```
main.py                   # FastAPI app and routes
app/
├── config.py             # pydantic-settings config
├── auth.py               # Supabase JWT middleware
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
docs/                     # Music theory knowledge base (10 .txt files)
frontend/                 # Next.js app (login, dashboard)
alembic/                  # DB migrations
```

## Local setup

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # fill in Groq, Supabase, and DB credentials
```

```bash
# Ingest music theory docs into ChromaDB
python3 -c "from app.rag.ingest import ingest; ingest()"

# Run DB migrations
python3 -m alembic upgrade head

# Run backend
uvicorn main:app --reload
```

```bash
# Run frontend
cd frontend
cp .env.local.example .env.local   # fill in Supabase and API URL
npm install
npm run dev
```

## API

All endpoints except `/health` require a Supabase JWT: `Authorization: Bearer <token>`.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/analyze` | Upload audio, returns transcript, features, and coach feedback |
| `GET` | `/sessions` | Returns the authenticated user's practice history |

## Deployment

**Backend (Render):** Connect repo at render.com → New → Blueprint. Reads `render.yaml` automatically. Fill in `GROQ_API_KEY`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and `SUPABASE_JWT_SECRET` in the Render dashboard. `DATABASE_URL` is auto-provisioned.

**Frontend (Vercel):** Connect repo at vercel.com, set root directory to `frontend/`, add `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, and `NEXT_PUBLIC_API_URL` as env vars.

Also add your Vercel URL to Supabase → Authentication → URL Configuration as a redirect URL.

## Status

- [x] Project config and auth (pydantic-settings, Supabase JWT)
- [x] Database models, migrations (SQLAlchemy + Alembic)
- [x] Audio processing pipeline (Whisper + librosa)
- [x] Music theory knowledge base + ChromaDB RAG
- [x] Coach agent (Groq LLM feedback)
- [x] REST API (`/health`, `/analyze`, `/sessions`)
- [x] Frontend (login, dashboard, session history)
- [x] Render deployment config (`render.yaml`)
- [ ] AWS S3 audio storage
