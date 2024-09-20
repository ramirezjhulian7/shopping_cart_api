# app/schemas.py

from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class ItemType(str, Enum):
    PRODUCT = "PRODUCT"
    EVENT = "EVENT"

class ItemBase(BaseModel):
    name: str
    description: str
    thumbnail: str
    price: float
    stock: int
    type: ItemType

class ProductCreate(ItemBase):
    care_instructions: str

class EventCreate(ItemBase):
    event_date: str

class Item(ItemBase):
    id: int

    model_config = {
        "from_attributes": True  # Para Pydantic v2
    }

class CartItemBase(BaseModel):
    item_id: int
    quantity: int = Field(..., ge=0, description="Cantidad debe ser mayor que 0")

class CartItemCreate(CartItemBase):
    pass

class CartItem(BaseModel):
    id: int
    cart_id: int
    item_id: int
    quantity: int
    item: Item
    subtotal: float

    model_config = {
        "from_attributes": True  # Para Pydantic v2
    }

class Cart(BaseModel):
    items: List[CartItem]
    total_quantity: int
    total_price: float

    model_config = {
        "from_attributes": True  # Para Pydantic v2
    }

class CartInvoice(BaseModel):
    items: List[CartItem]
    total_quantity: int
    total_price: float

    model_config = {
        "from_attributes": True  # Para Pydantic v2
    }
