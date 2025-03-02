from fastapi import APIRouter
from agents.document_processing import extract_text_from_pdf, clean_extracted_text
from agents.financial_analysis import analyze_stock_trend, generate_recommendation
from agents.database import query_documents


router = APIRouter()

# Endpoint pour poser une question sur le rapport 2024
@router.get("/ask")
def ask(query: str):
    response = query_documents(query)
    return {"response": response}

# Endpoint pour obtenir une recommandation financière
@router.get("/recommend")
def recommend(ticker: str):
    recommendation = generate_recommendation(ticker)
    return {"recommendation": recommendation}
