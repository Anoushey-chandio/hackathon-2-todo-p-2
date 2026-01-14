from typing import Optional
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Column, DateTime

class Jwks(SQLModel, table=True):
    __tablename__ = "jwks"

    id: str = Field(primary_key=True)
    publicKey: str = Field(nullable=False)
    privateKey: str = Field(nullable=False)
    createdAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False), default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False), default_factory=lambda: datetime.now(timezone.utc))
