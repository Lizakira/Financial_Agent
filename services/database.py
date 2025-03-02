import os
import chromadb

from sentence_transformers import SentenceTransformer
from services.document_processing import extract_text_from_pdf

#  Vérifier si le dossier de la base existe
DB_PATH = "chroma_db"
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

# Initialisation de ChromaDB
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection("sec_reports_2024")

# Charger le modèle d'embedding
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def add_document_to_chroma(doc_id, text):
    """Ajoute un document indexé dans ChromaDB."""
    embedding = embedding_model.encode(text).tolist()
    collection.add(ids=[doc_id], embeddings=[embedding], documents=[text])

def query_documents(query):
    """Effectue une recherche dans la base ChromaDB."""
    if collection.count() == 0:  # Vérifier si la base est vide
        return "⚠ La base de données est vide. Exécutez initialize_database() d'abord !"
    
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=5)
    
    return results["documents"] if results["documents"] else "Aucun résultat trouvé"

def initialize_database():
    """Charge le PDF et l'indexe dans ChromaDB si la base est vide."""
    pdf_path = "/home/liza/Bureau/financial_agent/services/annual_report.pdf"

    if collection.count() > 0:
        print("Base de données déjà initialisée.")
        return

    try:
        print(" Extraction du texte du rapport annuel 2024...")
        text = extract_text_from_pdf(pdf_path)
        add_document_to_chroma("apple_2024", text)
        print("Rapport 2024 chargé et indexé dans ChromaDB.")
    except Exception as e:
        print(f"⚠ Erreur lors de l'extraction du PDF : {e}")

# Exécuter l'initialisation SEULEMENT si la base est vide
initialize_database()
