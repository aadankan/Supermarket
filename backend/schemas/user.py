from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr
    is_admin: bool = False

class UserCreate(UserBase):
    password: str  # plain password input

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_admin: bool | None = None

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True
