import os
import requests  # type: ignore[import]
from dotenv import load_dotenv  # type: ignore[import]
import time

load_dotenv()  # Load environment variables from .env file

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Free model on OpenRouter — no cost
MODEL = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"



def generate_answer(question: str, context: str) -> str:
    """Generate answer using OpenRouter free LLM based on retrieved context."""

    system_prompt = """You are a helpful assistant that answers questions based only on the provided document context.
If the answer is not found in the context, say "I could not find relevant information in the uploaded documents."
Do not use any outside knowledge. Be concise and accurate."""

    user_prompt = f"""Context from documents:
{context}

Question: {question}

Answer:"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "RAG Chatbot"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.3
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
