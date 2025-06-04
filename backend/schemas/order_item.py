from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class OrderItemBase(BaseModel):
    order_id: Optional[int] = None
    product_id: int
    quantity: int
    price: Decimal

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
