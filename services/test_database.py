from services.database import query_documents

# Tester une recherche
query = "What does TSR Percentile mean ?"
response = query_documents(query)

print("Résultat de la recherche :", response)
