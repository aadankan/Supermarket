from pydantic import BaseModel, EmailStr
from typing import Optional

class SupplierBase(BaseModel):
    name: str
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(SupplierBase):
    pass

class SupplierOut(SupplierBase):
    id: int

    class Config:
        orm_mode = True
