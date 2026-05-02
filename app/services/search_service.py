import faiss # type: ignore[import]
import numpy as np  # type: ignore[import]
import pickle
import os
from typing import List

# Paths to persist the FAISS index and metadata
INDEX_PATH = "faiss_index/index.bin"
META_PATH = "faiss_index/metadata.pkl"

# Dimension of all-MiniLM-L6-v2 embeddings
EMBEDDING_DIM = 384

_index = None
_metadata = []  # List of {"content": "...", "source": "..."}


def _load_index():
    global _index, _metadata
    if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
        _index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            _metadata = pickle.load(f)
    else:
        _index = faiss.IndexFlatL2(EMBEDDING_DIM)
        _metadata = []


def _save_index():
    os.makedirs("faiss_index", exist_ok=True)
    faiss.write_index(_index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(_metadata, f)


def add_to_index(chunks: List[str], embeddings: np.ndarray, source: str):
    """Add document chunks and their embeddings to FAISS index."""
    global _index, _metadata
    _load_index()

    vectors = np.array(embeddings).astype("float32")
    _index.add(vectors)

    for chunk in chunks:
        _metadata.append({"content": chunk, "source": source})

    _save_index()
    print(f"Added {len(chunks)} chunks from '{source}' to FAISS index.")


def search(query_embedding: np.ndarray, top_k: int = 5) -> List[dict]:
    """Search FAISS index and return top_k matching chunks."""
    global _index, _metadata
    _load_index()

    if _index.ntotal == 0:
        return []

    query_vector = np.array([query_embedding]).astype("float32")
    distances, indices = _index.search(query_vector, min(top_k, _index.ntotal))

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < len(_metadata):
            results.append({
                "content": _metadata[idx]["content"],
                "source": _metadata[idx]["source"],
                "score": float(dist)
            })

    return results
