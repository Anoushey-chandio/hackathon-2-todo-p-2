from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from src.core.database import get_db, AsyncSession
from src.models.user import User
from src.core.security import decode_access_token
import logging

logger = logging.getLogger(__name__)

# Placeholder tokenUrl, as auth is handled by Next.js
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        logger.warning("get_current_user: Invalid JWT token")
        raise credentials_exception
    
    # Better Auth JWT usually puts user id in 'sub'
    user_id: str = payload.get("sub")
    if user_id is None:
        # Fallback to 'id' if sub is missing
        user_id = payload.get("id")
    
    if user_id is None:
        logger.warning(f"get_current_user: No user ID in token payload: {payload}")
        raise credentials_exception

    # Get User
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if user is None:
        logger.warning(f"get_current_user: User not found for ID: {user_id}")
        raise credentials_exception

    return user
