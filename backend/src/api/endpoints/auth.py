"""
Authentication endpoints - Session-based auth (no JWT)
Compatible with BetterAuth frontend client
"""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import EmailStr, BaseModel
from src.core.database import get_db
from src.models.user import User
from src.models.auth import Session
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
import uuid
import asyncio
import logging

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["auth"])

# -----------------------
# Request / Response Models
# -----------------------
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class SessionResponse(BaseModel):
    user: dict

# -----------------------
# Password Helpers
# -----------------------
def hash_password_sync(password: str) -> str:
    """Hash a password (truncate to 72 bytes for bcrypt compatibility)"""
    password_truncated = password[:72]
    return pwd_context.hash(password_truncated)

def verify_password_sync(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    password_truncated = plain_password[:72]
    return pwd_context.verify(password_truncated, hashed_password)

async def hash_password(password: str) -> str:
    return await asyncio.to_thread(hash_password_sync, password)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return await asyncio.to_thread(verify_password_sync, plain_password, hashed_password)

# -----------------------
# Session Helpers
# -----------------------
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

def set_auth_cookie(response: Response, token: str, expires_in: int):
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=expires_in,
        expires=expires_in,
        secure=False,  # True in production
        samesite="lax",
        path="/"
    )

SESSION_EXPIRE_SECONDS = 60 * 60 * 24  # 1 day

# -----------------------
# Endpoints
# -----------------------

@router.post("/sign-up", response_model=SessionResponse)
async def sign_up(
    request: SignUpRequest,
    response: Response,
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
    
    # Hash password
    hashed_password = await hash_password(request.password)
    
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
    
    # Create session token (random UUID)
    session_token = str(uuid.uuid4())
    
    # Save session to DB
    await create_db_session(db, str(user.id), session_token, SESSION_EXPIRE_SECONDS)
    
    # Set cookie
    set_auth_cookie(response, session_token, SESSION_EXPIRE_SECONDS)

    return SessionResponse(
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
    response: Response,
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
        )
    
    logger.info(f"User signed in: {user.email}")
    
    # Create session token (random UUID)
    session_token = str(uuid.uuid4())
    
    # Save session to DB
    await create_db_session(db, str(user.id), session_token, SESSION_EXPIRE_SECONDS)
    
    # Update last login
    user.updatedAt = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(user)
    
    # Set cookie
    set_auth_cookie(response, session_token, SESSION_EXPIRE_SECONDS)

    return SessionResponse(
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
    request: Request,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Sign out user (delete session from DB and clear cookie)"""
    token = request.cookies.get("access_token")
    if token:
        result = await db.execute(select(Session).where(Session.token == token))
        session = result.scalars().first()
        if session:
            await db.delete(session)
            await db.commit()
    
    response.delete_cookie(key="access_token", path="/", samesite="lax")
    return {"success": True}

@router.get("/session", response_model=SessionResponse)
async def get_session(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get current session user info (SESSION-BASED ONLY)"""
    
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    # Check session in DB
    result_session = await db.execute(select(Session).where(Session.token == token))
    session_db = result_session.scalars().first()
    
    if not session_db or session_db.expiresAt < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid",
        )
    
    # Get user from DB
    result = await db.execute(select(User).where(User.id == session_db.userId))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return SessionResponse(
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
