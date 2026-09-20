import os
import streamlit as st
from dotenv import load_dotenv

from src.document_loader import extract_text_from_pdf, split_text
from src.vector_store import VectorStore
from src.rag_pipeline import generate_answer

load_dotenv()

st.set_page_config(
    page_title="IntelliDocs",
    page_icon="📚",
    layout="wide"
)

st.title("📚 IntelliDocs")
st.caption("AI-Powered Document Q&A using Retrieval-Augmented Generation (RAG)")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "document_name" not in st.session_state:
    st.session_state.document_name = None
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Document")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=os.getenv("GEMINI_API_KEY", "")
    )

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file is not None and st.button("Process Document", use_container_width=True):
        with st.spinner("Reading and indexing document..."):
            try:
                text = extract_text_from_pdf(uploaded_file)
                chunks = split_text(text)

                if not chunks:
                    st.error("No readable text was found in the PDF.")
                else:
                    store = VectorStore()
                    store.build(chunks)

                    st.session_state.vector_store = store
                    st.session_state.document_name = uploaded_file.name
                    st.session_state.messages = []

                    st.success(f"Processed {len(chunks)} text chunks.")
            except Exception as e:
                st.error(f"Processing failed: {e}")

    if st.session_state.document_name:
        st.info(f"Loaded: {st.session_state.document_name}")

st.subheader("Ask questions about your document")

if not st.session_state.vector_store:
    st.info("Upload a PDF and click 'Process Document' to begin.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            st.caption("Sources: " + ", ".join(message["sources"]))

question = st.chat_input("Ask something about your document...")

if question:
    if not api_key:
        st.warning("Please enter your Gemini API key in the sidebar.")
    elif not st.session_state.vector_store:
        st.warning("Please upload and process a PDF first.")
    else:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching the document and generating an answer..."):
                try:
                    results = st.session_state.vector_store.search(question, k=4)
                    answer = generate_answer(question, results, api_key)

                    sources = sorted({
                        f"chunk {item['chunk_id'] + 1}"
                        for item in results
                    })

                    st.markdown(answer)
                    st.caption("Sources: " + ", ".join(sources))

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                except Exception as e:
                    st.error(f"Generation failed: {e}")
