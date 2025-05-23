from schemas.address import AddressOut

from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Base schema shared across others
class UserBase(BaseModel):
    username: Optional[str] = None
    email: EmailStr
    is_admin: bool = False

class UserCreate(BaseModel):
    email: EmailStr

# Schema for user updates (partial update support)
class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    phoneNumber: Optional[str]
    country: Optional[str]
    postalCode: Optional[str]
    city: Optional[str]
    street: Optional[str]
    is_admin: Optional[bool]

# Schema returned in list/GET operations
class UserOut(UserBase):
    id: int
    email_confirmed: bool = False

    class Config:
        orm_mode = True

# Full user schema (if needed internally)
class User(UserOut):
    addresses: Optional[List[AddressOut]] = None
    default_address: Optional[AddressOut] = None
    created_at: str  # ISO format date string
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class EmailRequest(BaseModel):
    email: str
