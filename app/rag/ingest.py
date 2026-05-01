import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "music_theory"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

_embedder = SentenceTransformer("all-MiniLM-L6-v2")
_client = chromadb.PersistentClient(path="chroma_db")


def ingest(docs_dir: str = "docs") -> None:
    loader = DirectoryLoader(docs_dir, glob="**/*.txt", loader_cls=TextLoader)
    docs = loader.load() # load knoweldge base

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(docs)

    collection = _client.get_or_create_collection(COLLECTION_NAME)
    texts = [c.page_content for c in chunks]
    embeddings = _embedder.encode(texts).tolist()
    ids = [str(i) for i in range(len(texts))]

    collection.upsert(documents=texts, embeddings=embeddings, ids=ids)
    print(f"Ingested {len(texts)} chunks into ChromaDB.")
