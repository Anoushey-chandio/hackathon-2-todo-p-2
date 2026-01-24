from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, Relationship, Column, DateTime
from sqlalchemy.sql import func
from src.models.base import SQLModel as BaseSQLModel

if TYPE_CHECKING:
    from src.models.user import User


class Task(BaseSQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    is_completed: bool = Field(default=False)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    )

    user_id: str = Field(foreign_key="user.id", nullable=False)

    owner: "User" = Relationship(back_populates="tasks")
