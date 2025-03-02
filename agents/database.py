import os
import chromadb
from together import Together
from sentence_transformers import SentenceTransformer
from agents.document_processing import extract_text_from_pdf

# Load API Key Securely
#TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_KEY = "500f6c574bcb5086b15c8d230b65d563c0688360f9ff270f1dc548916ef69919"

# Initialize Together AI Client
client = Together(api_key=TOGETHER_API_KEY)

# Initialize ChromaDB
DB_PATH = "chroma_db"
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection("sec_reports_2024")

# Load embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def query_documents(query):
    """Fetches relevant text and generates a natural response using LLaMA 3.3 70B."""
    if collection.count() == 0:
        return "⚠ La base de données est vide. Exécutez initialize_database() d'abord !"
    
    # Encode query
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=5)
    
    # Extract retrieved sections
    retrieved_texts = results["documents"]

    if not retrieved_texts:
        return "Aucun résultat trouvé."

    # Flatten list of lists and ensure string format
    retrieved_texts = [doc for sublist in retrieved_texts for doc in sublist]
    #context = "\n".join(map(str, retrieved_texts))

    # Limit the context size to fit within the token limit
    MAX_CONTEXT_TOKENS = 6000  # Adjust this based on Together AI's 8193 limit

    # Convert retrieved texts to a single string
    full_context = "\n".join(map(str, retrieved_texts))

    # Ensure context does not exceed token limit
    context_words = full_context.split()[:MAX_CONTEXT_TOKENS]  # Keep only first 6000 words
    context = " ".join(context_words)  # Convert back to string


    # Call Together AI API (LLaMA 3.3 70B)
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[
            {"role": "system", "content": "You are an expert financial assistant. Answer the user's question based on the provided financial report data."},
            {"role": "user", "content": f"Question: {query}\n\nRelevant context:\n{context}\n\nProvide a detailed and concise answer:"}
        ],
        max_tokens=500,  # Reduce max_tokens to fit within the limit
        temperature=0.7
    )

    return response.choices[0].message.content  # Extract LLM response
