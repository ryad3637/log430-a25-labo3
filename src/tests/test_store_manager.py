"""
Tests for orders manager
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import json
import pytest
from store_manager import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    result = client.get('/health-check')
    assert result.status_code == 200
    assert result.get_json() == {'status':'ok'}

def test_stock_flow(client):
    # 1. Créez un article (POST /products)
    product_data = {'name': 'Test Product', 'sku': 'TEST-12345', 'price': 99.90}
    response = client.post('/products',
                          data=json.dumps(product_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    product_response = response.get_json()
    assert product_response['product_id'] > 0 
    product_id = product_response['product_id']
    print(f"Produit créé avec ID: {product_id}")

    # 2. Ajoutez 5 unités au stock de cet article (POST /stocks)
    stock_data = {'product_id': product_id, 'quantity': 5}
    response = client.post('/stocks',
                          data=json.dumps(stock_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    print("5 unités ajoutées au stock")

    # 3. Vérifiez le stock, votre article devra avoir 5 unités dans le stock (GET /stocks/:id)
    response = client.get(f'/stocks/{product_id}')
    assert response.status_code == 201
    stock_response = response.get_json()
    assert stock_response['quantity'] == 5
    print(f"Stock initial vérifié: {stock_response['quantity']} unités")

    # Créer un utilisateur pour la commande
    user_data = {'name': 'Test User', 'email': 'test@example.com'}
    response = client.post('/users',
                          data=json.dumps(user_data),
                          content_type='application/json')
    
    if response.status_code != 201:
        print(f"❌ Erreur lors de la création d'utilisateur: {response.status_code}")
        print(f"Response data: {response.get_data(as_text=True)}")
    assert response.status_code == 201
    user_response = response.get_json()
    user_id = user_response['user_id']
    print(f"Utilisateur créé avec ID: {user_id}")

    # 4. Faites une commande de 2 unités de l'article que vous avez créé (POST /orders)
    order_data = {
        'user_id': user_id,
        'items': [
            {
                'product_id': product_id,
                'quantity': 2,
                'unit_price': 99.90
            }
        ]
    }
    response = client.post('/orders',
                          data=json.dumps(order_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    order_response = response.get_json()
    order_id = order_response['order_id']
    print(f"Commande créée avec ID: {order_id} (2 unités commandées)")

    # 5. Vérifiez le stock encore une fois (GET /stocks/:id)
    response = client.get(f'/stocks/{product_id}')
    assert response.status_code == 201
    stock_after_order = response.get_json()
    print(f"Stock après commande: {stock_after_order['quantity']} unités")
    
    # Le stock devrait être de 3 (5 - 2)
    assert stock_after_order['quantity'] == 3

    # 6. Étape extra: supprimez la commande et vérifiez le stock de nouveau
    response = client.delete(f'/orders/{order_id}')
    assert response.status_code == 200
    print(f"Commande {order_id} supprimée")

    # Vérifier le stock après suppression de la commande
    response = client.get(f'/stocks/{product_id}')
    assert response.status_code == 201
    stock_after_deletion = response.get_json()
    print(f"Stock après suppression de la commande: {stock_after_deletion['quantity']} unités")
    
    # Le stock devrait être revenu à 5
    assert stock_after_deletion['quantity'] == 5

    # Vérifier aussi le stock de l'article avec id=2 (s'il existe)
    response = client.get('/stocks/2')
    if response.status_code == 201:
        stock_id2 = response.get_json()
        print(f"Stock de l'article ID=2: {stock_id2['quantity']} unités")
    else:
        print("Aucun article avec ID=2 trouvé")

    print("=== RÉPONSE À LA QUESTION 1 ===")
    print(f"Stock final pour l'article créé (ID {product_id}): {stock_after_deletion['quantity']} unités")
    if response.status_code == 201:
        print(f"Stock pour l'article ID=2: {stock_id2['quantity']} unités")
    else:
        print("Stock pour l'article ID=2: Article non trouvé")