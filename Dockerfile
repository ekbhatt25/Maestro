FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pre-download Whisper base model so cold starts don't hit the network
RUN python -c "import whisper; whisper.load_model('base')"

# Bake music theory vectors into the image at build time
RUN python -c "from app.rag.ingest import ingest; ingest()"

EXPOSE 8000

# Run migrations then start the server; Railway injects $PORT
CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
