from pydantic import BaseModel
from typing import Optional

# Model for creating an inventory entry
class InventoryCreate(BaseModel):
    product_id: int
    quantity: int
    location: str

    class Config:
        orm_mode = True

# Model for updating an inventory entry
class InventoryUpdate(BaseModel):
    quantity: int
    location: Optional[str] = None

    class Config:
        orm_mode = True

# Model for reading inventory (output model)
class InventoryOut(BaseModel):
    product_id: int
    quantity: int
    location: str

    class Config:
        orm_mode = True
