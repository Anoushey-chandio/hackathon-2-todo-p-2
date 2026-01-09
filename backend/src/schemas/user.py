from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import Optional
from datetime import datetime

class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True)

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserOut(UserBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(SQLModel):
    access_token: str
    token_type: str