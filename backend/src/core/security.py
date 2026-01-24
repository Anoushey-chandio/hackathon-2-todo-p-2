# src/core/security.py
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from typing import Optional
import uuid

from .config import settings
from src.models.auth import Session  # SQLModel session model
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# Password hashing context
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash a plain password for storing in the database"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the stored hash"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def create_session_token(user_id: str) -> str:
    """Create a unique session token (UUID)"""
    return str(uuid.uuid4())


async def validate_session_token(token: str, db: AsyncSession) -> bool:
    """
    Validate that the session token exists in the DB and is not expired.
    `db` is an AsyncSession instance.
    """
    query = select(Session).where(Session.token == token)
    result = await db.execute(query)
    db_session = result.scalars().first()

    if db_session and db_session.expiresAt > datetime.now(timezone.utc):
        return True

    return False


async def create_db_session(db: AsyncSession, user_id: str, token: str, expires_in_seconds: int) -> Session:
    """
    Create a session record in the DB.
    Returns the session object.
    """
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(seconds=expires_in_seconds)

    session_obj = Session(
        id=str(uuid.uuid4()),
        userId=user_id,
        token=token,
        expiresAt=expires_at,
        createdAt=now,
        updatedAt=now,
    )
    db.add(session_obj)
    await db.commit()
    await db.refresh(session_obj)
    return session_obj
