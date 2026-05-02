from sentence_transformers import SentenceTransformer  # type: ignore[import]
from typing import List
import numpy as np  # type: ignore[import] 

# Free local model — no API key needed
# Downloads once (~90MB), then runs fully offline
MODEL_NAME = "all-MiniLM-L6-v2"

_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(MODEL_NAME)
        print("Embedding model loaded.")
    return _model

def get_embeddings(texts: List[str]) -> List[np.ndarray]:
    """Convert list of text strings to vector embeddings."""
    model = get_model()
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings
