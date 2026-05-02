from fastapi import APIRouter, HTTPException  # type: ignore[import]
from pydantic import BaseModel # type: ignore[import]
from app.services import embed_service, search_service, chat_service

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        question = request.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty.")

        # 1. Embed the user question
        question_embedding = embed_service.get_embeddings([question])[0]

        # 2. Search FAISS for top relevant chunks
        results = search_service.search(question_embedding, top_k=5)

        if not results:
            return {
                "answer": "No relevant documents found. Please upload a document first.",
                "sources": []
            }

        # 3. Build context from retrieved chunks
        context = "\n\n".join([r["content"] for r in results])

        # 4. Generate answer using OpenRouter LLM
        answer = chat_service.generate_answer(question, context)

        return {
            "answer": answer,
            "sources": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
