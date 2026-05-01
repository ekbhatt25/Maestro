import chromadb
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "music_theory"
TOP_K = 5

_embedder = SentenceTransformer("all-MiniLM-L6-v2")
_client = chromadb.PersistentClient(path="chroma_db")


def retrieve(query: str) -> str:
    collection = _client.get_or_create_collection(COLLECTION_NAME)
    embedding = _embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=TOP_K)
    chunks = results["documents"][0]
    return "\n\n".join(chunks)
