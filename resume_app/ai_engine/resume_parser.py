from PyPDF2 import PdfReader
import docx

def parse_resume(file):
    # Determine file type
    if hasattr(file, 'name'):
        filename = file.name.lower()
    else:
        raise ValueError("Invalid file uploaded")

    text = ""

    if filename.endswith(".pdf"):
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    elif filename.endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        raise ValueError("Unsupported file format. Upload PDF or DOCX.")

    return text
