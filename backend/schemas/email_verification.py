from pydantic import BaseModel, EmailStr

class EmailSchema(BaseModel):
    email: EmailStr

class TokenSchema(BaseModel):
    token: str
