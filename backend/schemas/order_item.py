from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class OrderItemBase(BaseModel):
    order_id: Optional[int] = None
    product_id: int
    quantity: int
    price: Decimal
    name: Optional[str] = None  # Optional name for the product
    image_url: Optional[str] = None  # Optional URL for the product image

    class Config:
        orm_mode = True

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    quantity: int
    price: Decimal

    class Config:
        orm_mode = True

class OrderItem(OrderItemBase):
    pass
