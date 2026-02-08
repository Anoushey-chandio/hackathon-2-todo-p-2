from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
import uuid
from sqlmodel import Field, Relationship, Column, DateTime, Text
from sqlalchemy.sql import func
from src.models.base import SQLModel as BaseSQLModel

if TYPE_CHECKING:
    from src.models.user import User

class Conversation(BaseSQLModel, table=True):
    __tablename__ = "conversation"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    title: Optional[str] = Field(default=None)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
    )

    messages: List["Message"] = Relationship(back_populates="conversation")
    # We might want to link back to user, but let's check if User model needs update.
    # The spec said User (1) -> (Many) Conversation.
    # I should check if I need to update User model to add `conversations` relationship.
    # The data-model.md implied relationships.
    
class Message(BaseSQLModel, table=True):
    __tablename__ = "message"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", nullable=False)
    role: str = Field(nullable=False) # user, assistant, system
    content: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )

    conversation: Optional[Conversation] = Relationship(back_populates="messages")
