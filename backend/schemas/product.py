from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    count: int = 0
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    class Config:
        orm_mode = True

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    count: Optional[int] = None

    class Config:
        orm_mode = True
