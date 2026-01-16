from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import Optional
from datetime import datetime

class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True)

class UserCreate(UserBase):
    password: str
    name: Optional[str] = None
    image: Optional[str] = None

class UserLogin(UserBase):
    password: str

class UserOut(UserBase):
    id: str
    name: str
    emailVerified: bool
    image: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True

class Token(SQLModel):
    access_token: str
    token_type: str