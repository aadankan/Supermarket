from backend.schemas.address import AddressOut

from pydantic import BaseModel, EmailStr
from typing import List, Optional



# Base schema shared across others
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_admin: bool = False

# Schema for user creation (includes password)
class UserCreate(UserBase):
    password: str  # plain password input

# Schema for user updates (partial update support)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

# Schema returned in list/GET operations
class UserOut(UserBase):
    id: int

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
    default_address: Optional[dict] = None  # Details of the default address
