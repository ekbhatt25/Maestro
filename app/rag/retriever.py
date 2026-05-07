import chromadb
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "music_theory"
TOP_K = 5

_embedder = SentenceTransformer("all-MiniLM-L6-v2")
_client = chromadb.PersistentClient(path="chroma_db")


def retrieve(query: str, features: dict | None = None) -> str:
    if not query and features:
        tempo = features.get("tempo_bpm", 0)
        rms = features.get("dynamic_rms", 0)
        query = f"tempo {tempo:.0f} BPM dynamics rhythm timing technique"
        if rms < 0.01:
            query += " soft quiet playing dynamics control"
        elif rms > 0.1:
            query += " loud forte dynamics expression"

    if not query:
        query = "music practice technique rhythm pitch dynamics"

    collection = _client.get_or_create_collection(COLLECTION_NAME)
    embedding = _embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=TOP_K)
    chunks = results["documents"][0]
    return "\n\n".join(chunks)
