import graphene
from graphene import ObjectType, String, Int
from stocks.schemas.product import Product
from db import get_redis_conn

class Query(ObjectType):       
    product = graphene.Field(Product, id=String(required=True))
    stock_level = Int(product_id=String(required=True))
    
    def resolve_product(self, info, id):
        """ Create an instance of Product based on stock info for that product that is in Redis """
        redis_client = get_redis_conn()
        product_data = redis_client.hgetall(f"stock:{id}")
        # Utilisation des colonnes name, sku, price stockées dans Redis
        if product_data:
            return Product(
                id=int(id),
                name=product_data.get('name', f"Product {id}"),
                sku=product_data.get('sku', ''),
                price=float(product_data.get('price', 0.0)),
                quantity=int(product_data.get('quantity', 0))
            )
        return None
    
    def resolve_stock_level(self, info, product_id):
        """ Retrieve stock quantity from Redis """
        redis_client = get_redis_conn()
        quantity = redis_client.hget(f"stock:{product_id}", "quantity")
        return int(quantity) if quantity else 0