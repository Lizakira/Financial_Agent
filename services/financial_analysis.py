import yfinance as yf
from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

def get_stock_data(ticker, start_date, end_date):
    """Récupère l'historique des prix d'une action."""
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    return data

def analyze_stock_trend(stock_data):
    """Analyse la variation des prix de l'action en 2024."""
    start_price = stock_data["Close"].iloc[0]
    end_price = stock_data["Close"].iloc[-1]
    percent_change = ((end_price - start_price) / start_price) * 100
    return f"Variation en 2024 : {percent_change:.2f}%"

def analyze_news_sentiment(news_texts):
    """Analyse les sentiments des actualités financières 2024."""
    sentiments = sentiment_model(news_texts)
    return sentiments

def generate_recommendation(ticker):
    """Génère une recommandation basée sur les données 2024."""
    news = ["Apple a annoncé une augmentation de ses revenus en 2024...", "Les ventes d'iPhone sont en hausse en 2024..."]
    sentiments = analyze_news_sentiment(news)

    avg_sentiment = sum([1 if s["label"] == "POSITIVE" else -1 for s in sentiments]) / len(sentiments)

    stock_data = get_stock_data(ticker, "2024-01-01", "2024-12-31")
    price_trend = analyze_stock_trend(stock_data)

    if avg_sentiment > 0.2 and "positive" in price_trend:
        return "BUY"
    elif avg_sentiment < -0.2 and "negative" in price_trend:
        return "SELL"
    else:
        return "HOLD"
