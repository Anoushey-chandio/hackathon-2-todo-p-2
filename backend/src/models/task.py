from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, Column, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from src.models.base import SQLModel as BaseSQLModel

class Task(BaseSQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    is_completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False))

    user_id: str = Field(foreign_key="user.id", nullable=False)
    owner: "User" = Relationship(back_populates="tasks")
