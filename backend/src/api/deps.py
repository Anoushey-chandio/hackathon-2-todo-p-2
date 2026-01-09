from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status, Cookie
from sqlmodel import select
from src.core.database import get_db, AsyncSession
from src.models.user import User
from src.models.auth import Session
from datetime import datetime, timezone

async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    session_token: Annotated[Optional[str], Cookie(alias="better-auth.session_token")] = None,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    
    if not session_token:
        raise credentials_exception

    # Validate session
    result = await db.execute(select(Session).where(Session.token == session_token))
    session = result.scalars().first()

    if not session:
        raise credentials_exception
    
    # Check expiry
    # BetterAuth dates are usually stored as aware UTC.
    now = datetime.now(timezone.utc)
    
    # Ensure session.expiresAt is aware for comparison
    expires_at = session.expiresAt
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < now:
        raise credentials_exception

    # Get User
    result = await db.execute(select(User).where(User.id == session.userId))
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
        
    return user