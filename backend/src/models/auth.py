from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, Column, DateTime

class Session(SQLModel, table=True):
    __tablename__ = "session"

    id: str = Field(primary_key=True)
    expiresAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    ipAddress: Optional[str] = Field(default=None)
    userAgent: Optional[str] = Field(default=None)
    userId: str = Field(foreign_key="user.id", nullable=False)
    token: str = Field(unique=True, index=True, nullable=False)
    createdAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    updatedAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))

    user: "User" = Relationship(back_populates="sessions")

class Account(SQLModel, table=True):
    __tablename__ = "account"

    id: str = Field(primary_key=True)
    accountId: str = Field(nullable=False)
    providerId: str = Field(nullable=False)
    userId: str = Field(foreign_key="user.id", nullable=False)
    accessToken: Optional[str] = Field(default=None)
    refreshToken: Optional[str] = Field(default=None)
    idToken: Optional[str] = Field(default=None)
    expiresAt: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    password: Optional[str] = Field(default=None)
    createdAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    updatedAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))

    user: "User" = Relationship(back_populates="accounts")

class Verification(SQLModel, table=True):
    __tablename__ = "verification"

    id: str = Field(primary_key=True)
    identifier: str = Field(nullable=False)
    value: str = Field(nullable=False)
    expiresAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    createdAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    updatedAt: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
