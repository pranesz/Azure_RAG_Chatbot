import streamlit as st  # type: ignore[import]
import requests  # type: ignore[import]

API_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 RAG Chatbot")
st.caption("Upload your documents and ask questions based on them.")

# ─── SIDEBAR — Upload ─────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file:
        if st.button("Process Document", use_container_width=True):
            with st.spinner("Uploading and indexing document..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(f"{API_URL}/upload", files=files)
                    result = response.json()

                    if response.status_code == 200:
                        st.success(f"✅ Indexed {result['chunks_indexed']} chunks from **{result['filename']}**")
                    else:
                        st.error(f"Error: {result.get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

    st.divider()
    st.markdown("**How it works:**")
    st.markdown("1. Upload a PDF document")
    st.markdown("2. Ask any question about it")
    st.markdown("3. Get answers grounded in your document")
    st.divider()
    st.markdown("**Stack:**")
    st.markdown("- 🔵 Azure Blob Storage")
    st.markdown("- ⚡ FAISS Vector Search")
    st.markdown("- 🧠 OpenRouter Free LLM")
    st.markdown("- 🚀 FastAPI Backend")

# ─── CHAT ─────────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if question := st.chat_input("Ask a question about your document..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Get answer from API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"question": question}
                )
                result = response.json()

                if response.status_code == 200:
                    answer = result["answer"]
                    sources = result.get("sources", [])

                    st.markdown(answer)

                    # Show sources
                    if sources:
                        with st.expander("📚 View Sources"):
                            for i, src in enumerate(sources[:3], 1):
                                st.markdown(f"**Source {i}** — `{src['source']}`")
                                st.caption(src["content"][:300] + "...")
                                st.divider()

                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    error_msg = result.get("detail", "Something went wrong.")
                    st.error(error_msg)

            except Exception as e:
                st.error(f"Connection error: {e}. Make sure FastAPI is running.")
