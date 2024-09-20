# app/crud.py

from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from . import models, schemas

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_cart(db: Session, cart_id: int):
    return db.query(models.Cart).filter(models.Cart.id == cart_id).first()

def create_cart(db: Session):
    db_cart = models.Cart()
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def add_item_to_cart(db: Session, cart_id: int, item_id: int, quantity: int):
    item = get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if item.stock < quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")
    
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart_id, 
        models.CartItem.item_id == item_id
    ).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = models.CartItem(
            cart_id=cart_id, 
            item_id=item_id, 
            quantity=quantity
        )
        db.add(cart_item)
    item.stock -= quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

def update_cart_item(db: Session, cart_id: int, item_id: int, quantity: int):
    if quantity < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity cannot be negative")
    
    # Buscar el ítem en el carrito
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart_id, 
        models.CartItem.item_id == item_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CartItem not found")
    
    # Buscar el ítem en la base de datos
    item = get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    if quantity == 0:
        # Si la cantidad es 0, devolver el stock y eliminar el ítem del carrito
        item.stock += cart_item.quantity
        db.delete(cart_item)
        db.commit()
        return None  # Devolver None si el ítem fue eliminado
    else:
        # Verificar si hay suficiente stock para la cantidad solicitada
        if item.stock + cart_item.quantity < quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")
        
        # Actualizar el stock y la cantidad del ítem en el carrito
        item.stock += cart_item.quantity - quantity
        cart_item.quantity = quantity
        db.commit()
        db.refresh(cart_item)
        return cart_item


def remove_cart_item(db: Session, cart_id: int, item_id: int):
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart_id, 
        models.CartItem.item_id == item_id
    ).first()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CartItem not found")
    
    item = get_item(db, item_id)
    if item:
        item.stock += cart_item.quantity
    db.delete(cart_item)
    db.commit()
    return {"detail": "Item removed from cart successfully."}

# Funciones CRUD para crear ítems
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        description=product.description,
        thumbnail=product.thumbnail,
        price=product.price,
        stock=product.stock,
        type=models.ItemType.PRODUCT,
        care_instructions=product.care_instructions
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(
        name=event.name,
        description=event.description,
        thumbnail=event.thumbnail,
        price=event.price,
        stock=event.stock,
        type=models.ItemType.EVENT,
        event_date=event.event_date
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_all_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_cart_invoice(db: Session, cart_id: int) -> schemas.CartInvoice:
    cart = db.query(models.Cart).options(
        joinedload(models.Cart.items).joinedload(models.CartItem.item)
    ).filter(models.Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found.")
    
    if not cart.items:
        return schemas.CartInvoice(items=[], total_quantity=0, total_price=0.0)
    
    invoice_items = []
    total_quantity = 0
    total_price = 0.0

    for cart_item in cart.items:
        item = cart_item.item
        subtotal = round(cart_item.quantity * item.price, 2)
        invoice_item = schemas.CartItem(
            id=cart_item.id,
            cart_id=cart_item.cart_id,
            item_id=item.id,
            quantity=cart_item.quantity,
            item=schemas.Item.from_orm(item),
            subtotal=subtotal
        )
        invoice_items.append(invoice_item)
        total_quantity += cart_item.quantity
        total_price += subtotal

    cart_invoice = schemas.CartInvoice(
        items=invoice_items,
        total_quantity=total_quantity,
        total_price=round(total_price, 2)
    )
    return cart_invoice
