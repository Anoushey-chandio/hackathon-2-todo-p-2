from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status, Cookie
from sqlmodel import select
from src.core.database import get_db, AsyncSession
from src.models.user import User
from src.models.auth import Session
from datetime import datetime

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
    # if session.expiresAt < datetime.now(timezone.utc): # Naive/Aware handling needed
    # BetterAuth dates are usually naive UTC or aware. SQLModel DateTime(timezone=True) is aware.
    # Let's assume aware for now.
    if session.expiresAt.replace(tzinfo=None) < datetime.utcnow(): 
        # Compare naive UTC if stored as such or adjust.
        # Postgres stores UTC. SQLite stores text.
        # Let's just check against datetime.now()
        raise credentials_exception

    # Get User
    result = await db.execute(select(User).where(User.id == session.userId))
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
        
    return user