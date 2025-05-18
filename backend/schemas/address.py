from pydantic import BaseModel
from typing import Optional

class AddressBase(BaseModel):
    user_id: int
    street: str
    city: str
    postal_code: str
    country: str
    is_default: Optional[int] = 0

class AddressCreate(AddressBase):
    created_at: str  # albo datetime, jeśli chcesz

class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    is_default: Optional[int] = None

class AddressOut(AddressBase):
    id: int
    created_at: str  # albo datetime

    class Config:
        orm_mode = True
