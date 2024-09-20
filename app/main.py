# app/main.py

from fastapi import FastAPI
from .routers import cart
from .database import Base, engine

# Importar todos los modelos para asegurar que las tablas se creen
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Shopping Cart API",
    description="API para gestionar un carrito de la compra.",
    version="1.0.0"
)

app.include_router(cart.router)
