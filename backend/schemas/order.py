from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from schemas.order_item import OrderItemCreate

# Pydantic model for creating an order
class OrderCreate(BaseModel):
    user_id: int
    order_date: datetime
    status: Optional[str] = 'pending'  # default status is 'pending'

    class Config:
        orm_mode = True

class OrderCreateWithItems(BaseModel):
    user_id: int
    shipping_address_id: int
    billing_address_id: int
    items: List[OrderItemCreate]
    order_date: Optional[datetime] = None
    status: Optional[str] = "pending"

# Pydantic model for updating an order
class OrderUpdate(BaseModel):
    user_id: Optional[int]
    order_date: Optional[datetime]
    status: Optional[str]

    class Config:
        orm_mode = True

# Pydantic model for getting an order (response model)
class Order(BaseModel):
    id: int
    user_id: int
    order_date: datetime
    status: str

    class Config:
        orm_mode = True
