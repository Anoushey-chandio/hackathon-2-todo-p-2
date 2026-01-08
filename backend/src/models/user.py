from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, Column, DateTime
from sqlalchemy.sql import func
from src.models.base import SQLModel as BaseSQLModel

class User(BaseSQLModel, table=True):
    __tablename__ = "user" # BetterAuth default

    id: str = Field(primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    emailVerified: bool = Field(default=False)
    image: Optional[str] = Field(default=None)
    createdAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    updatedAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    
    tasks: List["Task"] = Relationship(back_populates="owner")
    sessions: List["Session"] = Relationship(back_populates="user")
    accounts: List["Account"] = Relationship(back_populates="user")