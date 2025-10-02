"""
Test minimal pour vérifier le schéma GraphQL
"""
import sys
sys.path.append('.')

from stocks.schemas.product import Product
from stocks.schemas.query import Query
from graphene import Schema

# Test d'import
try:
    print("=== Test du schéma GraphQL ===")
    
    # Créer le schéma
    schema = Schema(query=Query)
    
    # Test de requête simple
    result = schema.execute('{ product(id: "1") { id name quantity } }')
    print("Requête basique réussie")
    print(f"Données: {result.data}")
    print(f"Erreurs: {result.errors}")
    
    # Test de requête avec nouveaux champs
    result2 = schema.execute('{ product(id: "1") { id name sku price quantity } }')
    print("\nRequête avec nouveaux champs:")
    print(f"Données: {result2.data}")
    print(f"Erreurs: {result2.errors}")
    
except Exception as e:
    print(f"Erreur: {e}")
    import traceback
    traceback.print_exc()