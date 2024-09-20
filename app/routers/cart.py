# app/routers/cart.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Union
from .. import models, schemas, crud
from ..database import get_db
import logging

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
)

# Configurar logging
logger = logging.getLogger(__name__)

@router.post("/items/", response_model=schemas.CartItem)
def add_item(cart_item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    logger.info(f"Agregando ítem ID {cart_item.item_id} con cantidad {cart_item.quantity} al carrito.")
    cart = db.query(models.Cart).first()
    if not cart:
        cart = crud.create_cart(db)
    try:
        # Agregar el ítem al carrito
        db_cart_item = crud.add_item_to_cart(db, cart.id, cart_item.item_id, cart_item.quantity)
        
        # Asegurar que 'item' está cargado para acceder a 'price'
        db_cart_item = db.query(models.CartItem).options(joinedload(models.CartItem.item)).filter(models.CartItem.id == db_cart_item.id).first()
        
        if not db_cart_item.item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Calcular subtotal
        subtotal = db_cart_item.quantity * db_cart_item.item.price
        
        # Crear la respuesta incluyendo 'subtotal'
        response = schemas.CartItem(
            id=db_cart_item.id,
            cart_id=db_cart_item.cart_id,
            item_id=db_cart_item.item_id,
            quantity=db_cart_item.quantity,
            item=db_cart_item.item,
            subtotal=subtotal
        )
        
        return response
    except HTTPException as e:
        logger.error(f"Error al agregar ítem al carrito: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado al agregar ítem al carrito: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/items/{item_id}/", response_model=Union[schemas.CartItem, dict])
def update_item(item_id: int, cart_item: schemas.CartItemBase, db: Session = Depends(get_db)):
    logger.info(f"Actualizando ítem ID {item_id} con nueva cantidad {cart_item.quantity}.")
    cart = db.query(models.Cart).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found.")
    
    try:
        # Actualizar el ítem en el carrito
        db_cart_item = crud.update_cart_item(db, cart.id, item_id, cart_item.quantity)
        
        # Si el ítem fue eliminado (devuelve None), devolver un mensaje
        if db_cart_item is None:
            return {"message": "Item removed from cart"}
        
        # Calcular subtotal si el ítem fue actualizado
        subtotal = db_cart_item.quantity * db_cart_item.item.price
        
        # Crear la respuesta incluyendo 'subtotal'
        response = schemas.CartItem(
            id=db_cart_item.id,
            cart_id=db_cart_item.cart_id,
            item_id=db_cart_item.item_id,
            quantity=db_cart_item.quantity,
            item=db_cart_item.item,
            subtotal=subtotal
        )
        
        return response
    except HTTPException as e:
        logger.error(f"Error al actualizar ítem en el carrito: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado al actualizar ítem en el carrito: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/items/{item_id}/")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    logger.info(f"Eliminando ítem ID {item_id} del carrito.")
    cart = db.query(models.Cart).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found.")
    try:
        result = crud.remove_cart_item(db, cart.id, item_id)
        return result
    except HTTPException as e:
        logger.error(f"Error al eliminar ítem del carrito: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado al eliminar ítem del carrito: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/", response_model=schemas.Cart)
def get_cart(db: Session = Depends(get_db)):
    logger.info("Obteniendo el carrito.")
    cart = db.query(models.Cart).options(
        joinedload(models.Cart.items).joinedload(models.CartItem.item)
    ).first()
    if not cart or not cart.items:
        return schemas.Cart(items=[], total_quantity=0, total_price=0.0)
    
    items = []
    total_quantity = 0
    total_price = 0.0
    for cart_item in cart.items:
        if not cart_item.item:
            logger.warning(f"El CartItem ID {cart_item.id} no tiene un ítem asociado.")
            continue  # O maneja el error según tus necesidades
        subtotal = round(cart_item.quantity * cart_item.item.price, 2)
        item_schema = schemas.CartItem(
            id=cart_item.id,
            cart_id=cart_item.cart_id,
            item_id=cart_item.item_id,
            quantity=cart_item.quantity,
            item=schemas.Item.from_orm(cart_item.item),
            subtotal=subtotal
        )
        items.append(item_schema)
        total_quantity += cart_item.quantity
        total_price += subtotal
    
    return schemas.Cart(
        items=items,
        total_quantity=total_quantity,
        total_price=round(total_price, 2)
    )

@router.get("/invoice/", response_model=schemas.CartInvoice)
def get_cart_invoice(db: Session = Depends(get_db)):
    logger.info("Obteniendo la factura del carrito.")
    cart = db.query(models.Cart).options(joinedload(models.Cart.items).joinedload(models.CartItem.item)).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found.")
    try:
        invoice = crud.get_cart_invoice(db, cart.id)
        return invoice
    except HTTPException as e:
        logger.error(f"Error al obtener la factura del carrito: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado al obtener la factura del carrito: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
