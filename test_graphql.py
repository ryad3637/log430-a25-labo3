import requests
import json

# Test de l'endpoint GraphQL
url = "http://localhost:5000/stocks/graphql-query"

# Requête GraphQL suggérée
query1 = {
    "query": "{ product(id: \"1\") { id quantity } }"
}

# Requête GraphQL avec plus d'informations
query2 = {
    "query": "{ product(id: \"2\") { id name quantity } }"
}

# Requête GraphQL avec toutes les nouvelles colonnes
query3 = {
    "query": "{ product(id: \"1\") { id name sku price quantity } }"
}

print("=== Test GraphQL Endpoint Amélioré ===")
print(f"URL: {url}")

# Test 1: Requête suggérée originale
print("\n1. Requête suggérée: { product(id: \"1\") { id quantity } }")
try:
    response1 = requests.post(url, json=query1)
    print(f"Status Code: {response1.status_code}")
    print(f"Réponse: {json.dumps(response1.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Erreur: {e}")

# Test 2: Avec plus d'informations
print("\n2. Requête étendue: { product(id: \"2\") { id name quantity } }")
try:
    response2 = requests.post(url, json=query2)
    print(f"Status Code: {response2.status_code}")
    print(f"Réponse: {json.dumps(response2.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Erreur: {e}")

# Test 3: Requête complète avec toutes les améliorations
print("\n3. Requête complète: { product(id: \"1\") { id name sku price quantity } }")
try:
    response3 = requests.post(url, json=query3)
    print(f"Status Code: {response3.status_code}")
    print(f"Réponse: {json.dumps(response3.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Erreur: {e}")