import fitz
import re

def extract_text_from_pdf(pdf_path):
    """Extrait le texte d'un fichier PDF page par page."""
    doc = fitz.open(pdf_path)  # Ouvrir le fichier PDF
    text = "\n".join([page.get_text("text") for page in doc])  # Extraire le texte de chaque page
    return text

def clean_extracted_text(text):
    """Nettoie le texte extrait d'un PDF."""
    text = re.sub(r'\n+', '\n', text)  # Supprime les lignes vides
    text = re.sub(r'\s{2,}', ' ', text)  # Supprime les espaces multiples
    return text.strip()

def extract_sections(text):
    """Détecte automatiquement les sections importantes dans un rapport 10-K."""
    sections = {}
    # Détection des titres en majuscules (ex: "MANAGEMENT’S DISCUSSION AND ANALYSIS")
    matches = re.finditer(r'\n([A-Z][A-Z\s\-]+)\n', text)

    section_titles = []
    positions = []

    for match in matches:
        section_titles.append(match.group(1).strip())
        positions.append(match.start())

    # Extraire le contenu de chaque section
    for i in range(len(section_titles) - 1):
        section_name = section_titles[i]
        section_content = text[positions[i]:positions[i + 1]].strip()
        sections[section_name] = section_content

    # Ajouter la dernière section jusqu'à la fin du document
    if section_titles:
        sections[section_titles[-1]] = text[positions[-1]:].strip()

    return sections
