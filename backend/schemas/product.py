# schemas/product.py
from pydantic import BaseModel
from decimal import Decimal

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: Decimal
    count: int | None = 0

class ProductCreate(ProductBase):
    name: str
    description: str | None = None
    price: Decimal
    count: int | None = 0
    class Config:
        orm_mode = True

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    count: int | None = None

    class Config:
        orm_mode = True
