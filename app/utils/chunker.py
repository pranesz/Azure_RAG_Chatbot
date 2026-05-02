from typing import List

def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split long text into overlapping chunks.

    Args:
        text: Full document text
        chunk_size: Max characters per chunk
        overlap: Overlapping characters between chunks (for context continuity)

    Returns:
        List of text chunks
    """
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at sentence boundary
        if end < len(text):
            last_period = text.rfind(".", start, end)
            if last_period != -1 and last_period > start + (chunk_size // 2):
                end = last_period + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap  # Overlap for context continuity

    return chunks
