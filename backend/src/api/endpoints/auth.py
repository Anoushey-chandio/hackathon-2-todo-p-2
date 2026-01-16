"""
Authentication endpoints - Email/Password auth with JWT tokens
Compatible with better-auth frontend client
"""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from pydantic import EmailStr, BaseModel
from src.core.database import get_db
from src.models.user import User
from src.models.auth import Session
from src.lib.auth_better import create_session_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
import logging
import asyncio
import uuid

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["auth"])


class SignUpRequest(BaseModel):
    """Sign up request model"""
    email: EmailStr
    password: str
    name: str | None = None


class SignInRequest(BaseModel):
    """Sign in request model"""
    email: EmailStr
    password: str


class SessionResponse(BaseModel):
    """Session response model"""
    session: dict
    user: dict


def hash_password(password: str) -> str:
    """Hash a password (truncate to 72 bytes for bcrypt compatibility)"""
    # bcrypt can only handle passwords up to 72 bytes
    password_truncated = password[:72]
    return pwd_context.hash(password_truncated)


def verify_password_sync(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash (truncate to 72 bytes for bcrypt compatibility)"""
    # bcrypt can only handle passwords up to 72 bytes
    password_truncated = plain_password[:72]
    return pwd_context.verify(password_truncated, hashed_password)


async def hash_password_async(password: str) -> str:
    """Async wrapper for password hashing"""
    return await asyncio.to_thread(hash_password, password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Async wrapper for password verification"""
    return await asyncio.to_thread(verify_password_sync, plain_password, hashed_password)


async def create_db_session(db: AsyncSession, user_id: str, token: str, expires_in_seconds: int) -> None:
    """Create a session record in the database"""
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(seconds=expires_in_seconds)
    
    session = Session(
        id=str(uuid.uuid4()),
        userId=user_id,
        token=token,
        expiresAt=expires_at,
        createdAt=now,
        updatedAt=now
    )
    db.add(session)
    await db.commit()


@router.post("/sign-up", response_model=SessionResponse)
async def sign_up(
    request: SignUpRequest,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Create a new user account and return session"""
    
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == request.email))
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Hash password (async to avoid blocking)
    hashed_password = await hash_password_async(request.password)
    
    # Create user
    user = User(
        email=request.email,
        name=request.name or request.email.split("@")[0],
        password=hashed_password,
        emailVerified=False,
        image=None,
        createdAt=datetime.now(timezone.utc),
        updatedAt=datetime.now(timezone.utc),
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    logger.info(f"User created: {user.email} (id: {user.id})")
    
    # Create session tokens
    tokens = create_session_token(str(user.id), user.email)
    
    # Save session to DB
    await create_db_session(db, str(user.id), tokens["access_token"], tokens["expires_in"])
    
    return SessionResponse(
        session=tokens,
        user={
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "image": user.image,
            "emailVerified": user.emailVerified,
            "createdAt": user.createdAt.isoformat(),
            "updatedAt": user.updatedAt.isoformat(),
        }
    )


@router.post("/sign-in", response_model=SessionResponse)
async def sign_in(
    request: SignInRequest,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Authenticate user with email/password"""
    
    # Find user
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalars().first()
    
    if not user or not await verify_password(request.password, user.password or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"User signed in: {user.email}")
    
    # Create session tokens
    tokens = create_session_token(str(user.id), user.email)
    
    # Save session to DB
    await create_db_session(db, str(user.id), tokens["access_token"], tokens["expires_in"])
    
    # Update last login
    user.updatedAt = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(user)
    
    return SessionResponse(
        session=tokens,
        user={
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "image": user.image,
            "emailVerified": user.emailVerified,
            "createdAt": user.createdAt.isoformat(),
            "updatedAt": user.updatedAt.isoformat(),
        }
    )


@router.post("/sign-out")
async def sign_out(
    authorization: Annotated[str | None, Header()] = None,
    db: Annotated[AsyncSession, Depends(get_db)] = None,
):
    """Sign out user (delete session from DB)"""
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
        result = await db.execute(select(Session).where(Session.token == token))
        session = result.scalars().first()
        if session:
            await db.delete(session)
            await db.commit()
    
    return {"success": True}


@router.get("/session", response_model=SessionResponse)
async def get_session(
    authorization: Annotated[str | None, Header()] = None,
    db: Annotated[AsyncSession, Depends(get_db)] = None,
):
    """Get current session/user info from token"""
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization.replace("Bearer ", "")
    
    # Verify token format
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
        
    # Check session in DB
    result_session = await db.execute(select(Session).where(Session.token == token))
    session_db = result_session.scalars().first()
    
    if not session_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid",
        )
    
    # Get user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return SessionResponse(
        session={
            "access_token": token,
            "token_type": "Bearer",
        },
        user={
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "image": user.image,
            "emailVerified": user.emailVerified,
            "createdAt": user.createdAt.isoformat(),
            "updatedAt": user.updatedAt.isoformat(),
        }
    )