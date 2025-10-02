"""
Product class (value object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from sqlalchemy import Column, Integer, DECIMAL, String
from orders.models.base import Base

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    sku = Column(String(64), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)