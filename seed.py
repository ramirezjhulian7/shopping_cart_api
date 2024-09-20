# seed.py

import os
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal, engine
from app import models
from dotenv import load_dotenv

# Cargar variables de entorno desde .env.docker
load_dotenv(dotenv_path=".env.docker")

# Crear las tablas si no existen
models.Base.metadata.create_all(bind=engine)

def reset_sequence(db: Session, sequence_name: str, restart_with: int = 1):
    """
    Reinicia una secuencia específica en la base de datos.

    :param db: Sesión de SQLAlchemy.
    :param sequence_name: Nombre completo de la secuencia (incluyendo el esquema).
    :param restart_with: Valor con el que se reiniciará la secuencia.
    """
    try:
        reset_seq_sql = f"ALTER SEQUENCE {sequence_name} RESTART WITH {restart_with};"
        db.execute(text(reset_seq_sql))
        print(f"Secuencia {sequence_name} reiniciada con éxito a {restart_with}.")
    except Exception as e:
        db.rollback()
        print(f"Error al reiniciar la secuencia {sequence_name}: {e}")
        raise e

def seed_items(db: Session):
    try:
        # 1. Eliminar todos los CartItems existentes
        deleted_cart_items = db.query(models.CartItem).delete()
        print(f"Eliminados {deleted_cart_items} CartItems existentes.")

        # 2. Eliminar todos los Events existentes
        deleted_events = db.query(models.Event).delete()
        print(f"Eliminados {deleted_events} Events existentes.")

        # 3. Eliminar todos los Products existentes
        deleted_products = db.query(models.Product).delete()
        print(f"Eliminados {deleted_products} Products existentes.")

        # 4. Eliminar todos los Items existentes
        deleted_items = db.query(models.Item).delete()
        print(f"Eliminados {deleted_items} Items existentes.")

        # Confirmar las eliminaciones
        db.commit()

        # 5. Reiniciar la secuencia de items_id_seq a 1
        reset_sequence(db, "public.items_id_seq", restart_with=1)

        # Confirmar el reinicio de la secuencia
        db.commit()

        # 6. Crear nuevos ítems de prueba
        item1 = models.Product(
            name="Gafas de sol Carey",
            description="Gafas de sol de alta calidad con protección UV.",
            thumbnail="https://example.com/thumbnails/gafas_carey.jpg",
            price=39.99,
            stock=10,
            type=models.ItemType.PRODUCT,
            care_instructions="Limpiar con un paño suave y almacenar en un estuche."
        )
        item2 = models.Event(
            name="Red Hot Chili Peppers en Madrid",
            description="Concierto de Red Hot Chili Peppers en el estadio Santiago Bernabéu.",
            thumbnail="https://example.com/thumbnails/red_hot_chili_peppers.jpg",
            price=60.00,
            stock=20,
            type=models.ItemType.EVENT,
            event_date="2024-12-31"
        )

        # Agregar los nuevos ítems a la sesión
        db.add_all([item1, item2])
        db.commit()
        print("Ítems de prueba insertados correctamente.")

    except Exception as e:
        db.rollback()
        print(f"Error al ejecutar el seed: {e}")
        raise e

def main():
    db = SessionLocal()
    try:
        seed_items(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
