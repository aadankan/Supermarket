from pydantic import BaseModel
from decimal import Decimal

class OrderItemBase(BaseModel):
    order_id: int
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
