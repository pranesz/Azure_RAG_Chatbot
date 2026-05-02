from fastapi import APIRouter, UploadFile, File, HTTPException # type: ignore[import]
from app.services import blob_service, embed_service, search_service
from app.utils.chunker import split_text
import fitz  # PyMuPDF  # type: ignore[import]
import io
import hashlib

uploaded_hashes = set()
router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    
    
    try:
        # 1. Read file bytes
        file_bytes = await file.read()

         # ─── DUPLICATE CHECK ──────────────────────────────────────────
        file_hash = hashlib.md5(file_bytes).hexdigest()

        if file_hash in uploaded_hashes:
            raise HTTPException(
                status_code=400,
                detail=f"'{file.filename}' already uploaded. Skipping duplicate."
            )

        uploaded_hashes.add(file_hash)
        # ──────────────────────────────────────────────────────────────


        # 2. Upload to Azure Blob Storage
        blob_url = blob_service.upload_file(file.filename, file_bytes)

        # 3. Extract text from PDF
        text = extract_text_from_pdf(file_bytes)
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from document.")

        # 4. Split text into chunks
        chunks = split_text(text)

        # 5. Generate embeddings for each chunk
        embeddings = embed_service.get_embeddings(chunks)
        print("Number of embeddings:", len(embeddings))
        print("Embedding dimension:", len(embeddings[0]))
        print("First embedding:", embeddings[0])

        # 6. Store in FAISS index
        search_service.add_to_index(chunks, embeddings, file.filename)

        return {
            "status": "success",
            "filename": file.filename,
            "blob_url": blob_url,
            "chunks_indexed": len(chunks)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text
