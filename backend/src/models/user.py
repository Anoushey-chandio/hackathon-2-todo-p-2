from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
import uuid

from sqlmodel import Field, Relationship, Column, DateTime
from src.models.base import SQLModel as BaseSQLModel

if TYPE_CHECKING:
    from src.models.task import Task
    from src.models.auth import Session, Account


class User(BaseSQLModel, table=True):
    __tablename__ = "user"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    emailVerified: bool = Field(default=False)
    image: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)

    createdAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    updatedAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))

    # ✅ Relationships
    tasks: List["Task"] = Relationship(back_populates="owner")
    sessions: List["Session"] = Relationship(back_populates="user")
    accounts: List["Account"] = Relationship(back_populates="user")
