"""
Authentication endpoints - Session-based auth (no JWT)
Compatible with BetterAuth frontend client
"""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import EmailStr, BaseModel
from src.core.database import get_db
from src.models.user import User
from src.models.auth import Session as AuthSession
from argon2 import PasswordHasher  # ✅ Argon2 - NO 72 byte limit!
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timezone, timedelta
import uuid
import asyncio
import logging

logger = logging.getLogger(__name__)

# -----------------------
# Password hashing - ARGON2 (Modern & Secure)
# -----------------------
ph = PasswordHasher()

def hash_password_sync(password: str) -> str:
    """Hash password using Argon2 - handles any length!"""
    return ph.hash(password)

def verify_password_sync(plain_password: str, hashed_password: str) -> bool:
    """Verify password using Argon2"""
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False

async def hash_password(password: str) -> str:
    """Async wrapper for hash_password_sync"""
    return await asyncio.to_thread(hash_password_sync, password)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Async wrapper for verify_password_sync"""
    return await asyncio.to_thread(verify_password_sync, plain_password, hashed_password)

# -----------------------
# Router (NO PREFIX HERE)
# -----------------------
router = APIRouter(tags=["auth"])

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
# Session Helpers
# -----------------------
SESSION_EXPIRE_SECONDS = 60 * 60 * 24  # 1 day

async def create_db_session(db: AsyncSession, user_id: str, token: str, expires_in_seconds: int) -> None:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(seconds=expires_in_seconds)
    
    session = AuthSession(
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
        secure=False,
        samesite="lax",
        path="/"
    )

# -----------------------
# Endpoints
# -----------------------
@router.post("/signup", response_model=SessionResponse)
async def sign_up(
    request: SignUpRequest,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(User).where(User.email == request.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    hashed_password = await hash_password(request.password)
    
    now = datetime.now(timezone.utc)
    user = User(
        email=request.email,
        name=request.name or request.email.split("@")[0],
        password=hashed_password,
        emailVerified=False,
        image=None,
        createdAt=now,
        updatedAt=now,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    logger.info(f"User created: {user.email} (id: {user.id})")
    
    session_token = str(uuid.uuid4())
    await create_db_session(db, str(user.id), session_token, SESSION_EXPIRE_SECONDS)
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

@router.post("/signin", response_model=SessionResponse)
async def sign_in(
    request: SignInRequest,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalars().first()
    
    if not user or not await verify_password(request.password, user.password or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    logger.info(f"User signed in: {user.email}")
    
    session_token = str(uuid.uuid4())
    await create_db_session(db, str(user.id), session_token, SESSION_EXPIRE_SECONDS)
    
    user.updatedAt = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(user)
    
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

@router.post("/signout")
async def sign_out(
    request: Request,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    token = request.cookies.get("access_token")
    if token:
        result = await db.execute(select(AuthSession).where(AuthSession.token == token))
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
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    result_session = await db.execute(select(AuthSession).where(AuthSession.token == token))
    session_db = result_session.scalars().first()
    
    if not session_db or session_db.expiresAt < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid",
        )
    
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