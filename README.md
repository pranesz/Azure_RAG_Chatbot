# RAG Chatbot — Azure + FAISS + OpenRouter

AI-powered chatbot that answers questions from your uploaded documents.

## Stack
- **Streamlit** — Frontend UI
- **FastAPI** — Backend API
- **Azure Blob Storage** — Document storage
- **FAISS** — Local vector search (free)
- **OpenRouter** — Free LLM (Llama 3.2)
- **sentence-transformers** — Free local embeddings

---

## Setup

### 1. Clone and install
```bash
git clone https://github.com/yourusername/rag-chatbot.git
cd rag-chatbot
pip install -r requirements.txt
```

### 2. Add your API keys
Copy `.env` and fill in your keys:
```bash
cp .env .env.local
```
Edit `.env` with:
- `OPENROUTER_API_KEY` — from https://openrouter.ai (free signup)
- `AZURE_STORAGE_CONNECTION_STRING` — from Azure Portal

### 3. Run FastAPI backend
```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Run Streamlit frontend (new terminal)
```bash
streamlit run streamlit_app.py
```

### 5. Open browser
- Streamlit UI: http://localhost:8501
- FastAPI docs: http://localhost:8000/docs

---

## How to Use
1. Upload a PDF using the sidebar
2. Click "Process Document"
3. Ask any question in the chat
4. Get answers grounded in your document

---

## Deployment (Azure Container Apps)
See `.github/workflows/deploy.yml` for CI/CD setup.
Add these GitHub Secrets:
- `AZURE_CREDENTIALS`
- `ACR_NAME`
- `RESOURCE_GROUP`
