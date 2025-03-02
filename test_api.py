import requests

url = "http://127.0.0.1:8000"

#Tester l'endpoint /ask
query = "What does TSR Percentile mean ?"
response = requests.get(f"{url}/ask", params={"query": query})
print("Réponse de l'API:", response.json())

# Tester l'endpoint /recommend
# ticker = "AAPL"
# response = requests.get(f"{url}/recommend", params={"ticker": ticker})
# print("Recommandation de l'API:", response.json())
