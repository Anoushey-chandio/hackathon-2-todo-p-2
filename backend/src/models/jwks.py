from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Column, DateTime

class Jwks(SQLModel, table=True):
    __tablename__ = "jwks"

    id: str = Field(primary_key=True)
    publicKey: str = Field(nullable=False)
    privateKey: str = Field(nullable=False)
    createdAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    updatedAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
