import re
import fitz


def extract_text_from_pdf(uploaded_file):
    document = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
    pages = []

    for page in document:
        text = page.get_text("text")
        if text.strip():
            pages.append(text)

    document.close()
    return "\n".join(pages)


def split_text(text, chunk_size=900, overlap=150):
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks
