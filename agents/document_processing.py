import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    """Extrait et nettoie le texte d'un PDF."""
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return clean_extracted_text(text)

def clean_extracted_text(text):
    """Nettoie le texte extrait du PDF."""
    text = re.sub(r'\n+', '\n', text)  # Supprime les lignes vides
    text = re.sub(r'\s{2,}', ' ', text)  # Supprime les espaces multiples
    return text.strip()
