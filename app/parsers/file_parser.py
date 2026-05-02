import pdfplumber
from docx import Document
import tempfile
import os


def parse_pdf(file_path):
    text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)


def parse_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])


def parse_file(file_storage):
    filename = file_storage.filename.lower()

    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file_storage.save(tmp.name)
        temp_path = tmp.name

    try:
        if filename.endswith(".pdf"):
            return parse_pdf(temp_path)

        elif filename.endswith(".docx"):
            return parse_docx(temp_path)

        else:
            raise ValueError("Unsupported file type. Use PDF or DOCX.")

    finally:
        os.remove(temp_path)