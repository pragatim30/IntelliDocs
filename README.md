# IntelliDocs – AI-Powered Document Q&A Assistant

IntelliDocs is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their contents.

The application retrieves semantically relevant sections from the uploaded document and provides them as context to Google's Gemini LLM. This helps produce document-grounded answers instead of relying only on the model's general knowledge.

## Features

- PDF document upload
- Text extraction and chunking
- Sentence-transformer embeddings
- FAISS vector similarity search
- Gemini LLM integration
- Structured prompt engineering
- Context-grounded question answering
- Conversational chat interface
- Source chunk references
- Simple Streamlit UI

## Architecture

```text
                ┌─────────────────┐
                │   PDF Upload    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Text Extraction │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Text Chunking   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Embeddings    │
                │ MiniLM Model    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  FAISS Index    │
                └────────┬────────┘
                         │
               User Question
                         │
                         ▼
                ┌─────────────────┐
                │ Similarity      │
                │ Search          │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Context +       │
                │ Structured      │
                │ Prompt          │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Gemini LLM     │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Grounded Answer │
                └─────────────────┘
```

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- Sentence Transformers
- FAISS
- PyMuPDF
- NumPy

## Project Structure

```text
IntelliDocs/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── data/
│   └── sample.pdf
│
└── src/
    ├── __init__.py
    ├── document_loader.py
    ├── vector_store.py
    └── rag_pipeline.py
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/IntelliDocs.git
cd IntelliDocs
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Do not upload `.env` to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## How RAG Works

1. The user uploads a PDF.
2. PyMuPDF extracts the text.
3. The text is divided into overlapping chunks.
4. Sentence Transformers converts chunks into vector embeddings.
5. FAISS stores the embeddings for similarity search.
6. When the user asks a question, the question is embedded.
7. FAISS retrieves the most relevant chunks.
8. Retrieved chunks are inserted into a structured prompt.
9. Gemini generates an answer using the retrieved context.

## Prompt Engineering

IntelliDocs uses a structured prompt that instructs the LLM to:

- answer using the supplied context;
- avoid unsupported information;
- explicitly state when the document does not contain the answer;
- produce concise and readable responses.

## Future Improvements

- Persistent vector database
- Multi-document knowledge bases
- Conversation memory
- Streaming responses
- Better source/page-level citations
- Authentication
- Deployment on Streamlit Cloud
- Support for DOCX and TXT files

## Author

Pragati Maurya
