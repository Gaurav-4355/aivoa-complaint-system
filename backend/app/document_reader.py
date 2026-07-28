import io
from pypdf import PdfReader
from docx import Document


def extract_text_from_upload(filename: str, content: bytes) -> str:
    """
    Lightweight, non-production-grade extraction - the assignment
    explicitly says production-grade OCR/parsing is not required.
    """
    name = filename.lower()

    if name.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if name.endswith(".docx"):
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)

    # .txt, .eml, or anything else: treat as plain text
    return content.decode("utf-8", errors="ignore")
