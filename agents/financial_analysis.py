import yfinance as yf
from transformers import pipeline
from datetime import datetime
import pandas as pd 

# Initialize sentiment analysis model
sentiment_model = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

def get_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock price data using yfinance.
    """
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def analyze_stock_trend(stock_data):
    """
    Analyze the stock price trend.
    """
    if stock_data.empty:
        return "No data available"
    
    close_prices = stock_data["Close"]
    
    if len(close_prices) < 2:
        return "Insufficient data to calculate trend"
    
    start_price = close_prices.iloc[0]  # First closing price
    end_price = close_prices.iloc[-1]   # Last closing price

    # Use .iloc[0] to extract a scalar value safely
    start_price = start_price.item() if isinstance(start_price, pd.Series) else start_price
    end_price = end_price.item() if isinstance(end_price, pd.Series) else end_price

    percent_change = ((end_price - start_price) / start_price) * 100
    return f"Variation: {percent_change:.2f}%"


def analyze_news_sentiment(news_texts):
    """
    Analyze sentiment of financial news.
    """
    sentiments = sentiment_model(news_texts)
    return sentiments

def generate_recommendation(ticker):
    """
    Generate a recommendation based on stock data and news sentiment.
    """
    # Fetch stock data using yfinance
    stock_data = get_stock_data(ticker, "2024-01-01", "2024-12-31")
    price_trend = analyze_stock_trend(stock_data)

    # Example news for sentiment analysis
    news = [
        "Apple has announced record revenue growth in 2024.",
        "iPhone sales are booming in 2024."
    ]
    sentiments = analyze_news_sentiment(news)

    # Calculate average sentiment
    avg_sentiment = sum([1 if s["label"] == "POSITIVE" else -1 for s in sentiments]) / len(sentiments)

    # Generate recommendation
    if avg_sentiment > 0.2 and "positive" in price_trend:
        return "BUY"
    elif avg_sentiment < -0.2 and "negative" in price_trend:
        return "SELL"
    else:
        return "HOLD"

# Example usage
ticker = "MSFT"
recommendation = generate_recommendation(ticker)
print(f"Recommendation for {ticker}: {recommendation}")