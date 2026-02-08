# backend/src/api/deps.py
from typing import Annotated
from fastapi import Depends, HTTPException, status, Request
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.core.database import get_db
from src.models.user import User
from src.models.auth import Session
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

async def get_token(request: Request) -> str:  # ✅ async
    """
    Get the session token from httpOnly cookie
    """
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        return cookie_token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated"
    )

async def get_current_user(  # ✅ async
    db: Annotated[AsyncSession, Depends(get_db)],  # ✅ AsyncSession
    token: Annotated[str, Depends(get_token)]
) -> User:
    """
    Get the currently authenticated user based on session cookie
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Check if session exists and is valid
    result_session = await db.execute(select(Session).where(Session.token == token))  # ✅ await db.execute
    session_db = result_session.scalars().first()  # ✅ scalars().first()

    if not session_db or session_db.expiresAt < datetime.now(timezone.utc):
        logger.warning(f"get_current_user: Invalid or expired session for token: {token[:10]}...")
        raise credentials_exception

    # Get User from DB
    result_user = await db.execute(select(User).where(User.id == session_db.userId))  # ✅ await
    user = result_user.scalars().first()  # ✅ scalars().first()

    if not user:
        logger.warning(f"get_current_user: User not found for ID: {session_db.userId}")
        raise credentials_exception

    return user