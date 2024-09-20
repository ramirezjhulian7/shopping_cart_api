# app/utils/exceptions.py

from fastapi import HTTPException, status

class ItemNotFoundException(HTTPException):
    def __init__(self, item_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found."
        )

class OutOfStockException(HTTPException):
    def __init__(self, item_id: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Item with id {item_id} is out of stock."
        )

class InvalidQuantityException(HTTPException):
    def __init__(self, quantity: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid quantity: {quantity}. Must be a positive integer."
        )
