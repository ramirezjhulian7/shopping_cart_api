# tests/test_cart.py

import pytest
from app import models, schemas
from sqlalchemy.orm import Session

@pytest.fixture(scope="module")
def test_items(db: Session):
    # Crear ítems de prueba
    item1 = models.Product(
        name="Gafas de sol Carey",
        description="Descripción de Gafas de sol Carey",
        thumbnail="url_thumbnail_product",
        price=39.99,
        stock=10,
        type=schemas.ItemType.PRODUCT,
        care_instructions="Instrucciones de cuidado"
    )
    item2 = models.Event(
        name="Red Hot Chili Peppers en Madrid",
        description="Descripción del evento",
        thumbnail="url_thumbnail_event",
        price=60.00,
        stock=20,
        type=schemas.ItemType.EVENT,
        event_date="2024-12-31"
    )
    db.add(item1)
    db.add(item2)
    db.commit()
    db.refresh(item1)
    db.refresh(item2)
    return [item1, item2]

def test_add_item_to_cart(client, test_items):
    response = client.post("/cart/items/", json={"item_id": test_items[0].id, "quantity": 3})
    assert response.status_code == 200
    data = response.json()
    assert data["item_id"] == test_items[0].id
    assert data["quantity"] == 3

def test_add_existing_item_to_cart(client, test_items):
    response = client.post("/cart/items/", json={"item_id": test_items[0].id, "quantity": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 5  # 3 + 2

def test_add_item_out_of_stock(client, test_items):
    response = client.post("/cart/items/", json={"item_id": test_items[0].id, "quantity": 100})
    assert response.status_code == 400
    assert response.json()["detail"] == f"Item with id {test_items[0].id} is out of stock."

def test_update_item_quantity(client, test_items):
    response = client.put(f"/cart/items/{test_items[0].id}/", json={"quantity": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 2

def test_remove_item_from_cart(client, test_items):
    response = client.delete(f"/cart/items/{test_items[0].id}/")
    assert response.status_code == 200
    assert response.json()["detail"] == "Item removed from cart successfully."

def test_get_empty_cart(client):
    response = client.get("/cart/")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total_quantity"] == 0
    assert data["total_price"] == 0.0
