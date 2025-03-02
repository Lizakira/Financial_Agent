import streamlit as st
import requests

# FastAPI Server URL
FASTAPI_URL = "http://127.0.0.1:8000"  # Update if running on a different server

# 🎨 Streamlit UI
st.set_page_config(page_title="Financial Assistant", layout="wide")

st.title("💰 Financial Assistant")
st.sidebar.title("📊 Select a Tool")

# 🎯 Navigation Between Two Features
app_mode = st.sidebar.radio("Choose a Function:", ["📜 Chat with Financial Reports", "📈 Stock Recommendation"])

# ================== 🗨️ CHATBOT FOR FINANCIAL REPORTS ==================
if app_mode == "📜 Chat with Financial Reports":
    st.header("📜 Chat with Financial Reports")

    # User Input
    query = st.text_input("Ask a question about the financial reports:")
    
    if st.button("Ask"):
        if query:
            # Call FastAPI
            response = requests.get(f"{FASTAPI_URL}/ask", params={"query": query})
            if response.status_code == 200:
                st.subheader("🤖 Copilot Response:")
                st.write(response.json().get("response", "No response received."))
            else:
                st.error(f"Error {response.status_code}: {response.text}")

# ================== 📈 STOCK RECOMMENDATION TOOL ==================
elif app_mode == "📈 Stock Recommendation":
    st.header("📈 Stock Recommendation Tool")

    # User Input
    ticker = st.text_input("Enter a stock ticker symbol (e.g., MSFT, AAPL):")

    if st.button("Get Recommendation"):
        if ticker:
            # Call FastAPI
            response = requests.get(f"{FASTAPI_URL}/recommend", params={"ticker": ticker})
            if response.status_code == 200:
                st.subheader("📊 Recommendation:")
                st.write(response.json().get("recommendation", "No recommendation received."))
            else:
                st.error(f"Error {response.status_code}: {response.text}")
