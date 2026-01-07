from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, Column, DateTime
from sqlalchemy.sql import func
from src.models.base import SQLModel as BaseSQLModel # Import SQLModel from base.py

class User(BaseSQLModel, table=True): # Inherit from SQLModel and use table=True
    __tablename__ = "users" # Still good practice for Alembic

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()), nullable=False)
    
    tasks: List["Task"] = Relationship(back_populates="owner") # Use forward reference