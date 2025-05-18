from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    product_id: int
    change: int
    transaction_type: str
    timestamp: datetime
    note: str | None = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    change: int
    transaction_type: str
    timestamp: datetime
    note: str | None = None

class TransactionOut(TransactionBase):
    id: int

    class Config:
        orm_mode = True
