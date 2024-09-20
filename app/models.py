# app/models.py

from sqlalchemy import Column, Integer, ForeignKey, Float, String, Enum
from sqlalchemy.orm import relationship
from .database import Base
from enum import Enum as PyEnum

class ItemType(PyEnum):
    PRODUCT = "PRODUCT"
    EVENT = "EVENT"

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    thumbnail = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    type = Column(Enum(ItemType), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': type
    }

class Product(Item):
    __tablename__ = 'products'
    id = Column(Integer, ForeignKey('items.id', ondelete="CASCADE"), primary_key=True)
    care_instructions = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': ItemType.PRODUCT
    }

class Event(Item):
    __tablename__ = 'events'
    id = Column(Integer, ForeignKey('items.id', ondelete="CASCADE"), primary_key=True)
    event_date = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': ItemType.EVENT
    }

class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True, index=True)
    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('carts.id', ondelete="CASCADE"), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id', ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)

    cart = relationship("Cart", back_populates="items")
    item = relationship("Item")
