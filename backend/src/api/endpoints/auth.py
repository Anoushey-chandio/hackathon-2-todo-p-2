from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import select
from src.core.database import get_db, AsyncSession
from src.models.user import User
from src.models.auth import Account, Session
from src.models.jwks import Jwks
from src.schemas.user import UserCreate, UserLogin
from src.core.security import get_password_hash, verify_password, create_access_token
from src.api.deps import get_current_user, get_token
import uuid
from datetime import datetime, timezone, timedelta

router = APIRouter()

COOKIE_NAME = "better-auth.session_token"
SESSION_DAYS = 7

@router.post("/sign-up/email")
async def sign_up(
    user_in: UserCreate,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Check if user exists
    result = await db.execute(select(User).where(User.email == user_in.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    now = datetime.now(timezone.utc)
    
    # Create User
    user_id = str(uuid.uuid4())
    user_name = user_in.name if user_in.name else user_in.email.split("@")[0]
    user = User(
        id=user_id,
        email=user_in.email,
        name=user_name,
        image=user_in.image,
        emailVerified=False,
        createdAt=now,
        updatedAt=now
    )
    db.add(user)

    # Create Account (Credential)
    account_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user_in.password)
    account = Account(
        id=account_id,
        accountId=account_id,
        providerId="credential",
        userId=user_id,
        password=hashed_password,
        createdAt=now,
        updatedAt=now
    )
    db.add(account)
    
    # Create Session
    session_id = str(uuid.uuid4())
    access_token = create_access_token(data={"sub": user.id}, expires_delta=timedelta(days=SESSION_DAYS))
    session = Session(
        id=session_id,
        userId=user_id,
        token=access_token,
        expiresAt=now + timedelta(days=SESSION_DAYS),
        createdAt=now,
        updatedAt=now
    )
    db.add(session)
    
    await db.commit()
    await db.refresh(user)
    await db.refresh(session)

    # Set Cookie
    response.set_cookie(
        key=COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=False, # Set to True in production with HTTPS
        samesite="lax",
        max_age=60 * 60 * 24 * SESSION_DAYS
    )

    return {
        "user": user,
        "session": session
    }

@router.post("/sign-in/email")
async def sign_in_email(
    user_in: UserLogin,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Find User
    result = await db.execute(select(User).where(User.email == user_in.email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Find Account
    result = await db.execute(select(Account).where(Account.userId == user.id))
    accounts = result.scalars().all()
    account = next((a for a in accounts if a.password), None)

    if not account or not verify_password(user_in.password, account.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Create Session
    now = datetime.now(timezone.utc)
    session_id = str(uuid.uuid4())
    access_token = create_access_token(data={"sub": user.id}, expires_delta=timedelta(days=SESSION_DAYS))
    session = Session(
        id=session_id,
        userId=user.id,
        token=access_token,
        expiresAt=now + timedelta(days=SESSION_DAYS),
        createdAt=now,
        updatedAt=now
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    # Set Cookie
    response.set_cookie(
        key=COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * SESSION_DAYS
    )

    return {
        "user": user,
        "session": session
    }

@router.get("/get-session")
async def get_session(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    token: str = Depends(get_token)
):
    # Find the session matching the current token
    # Note: get_current_user already validated the token is valid JWT and user exists.
    # But we want to return the Session object associated with it.
    result = await db.execute(
        select(Session)
        .where(Session.token == token)
    )
    session = result.scalars().first()
    
    if not session:
         raise HTTPException(status_code=401, detail="Session not found")

    return {
        "user": current_user,
        "session": session
    }

@router.post("/sign-out")
async def sign_out(
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
    token: str = Depends(get_token)
):
    # Find session and delete it
    result = await db.execute(select(Session).where(Session.token == token))
    session = result.scalars().first()
    
    if session:
        await db.delete(session)
        await db.commit()
    
    # Clear cookie
    response.delete_cookie(COOKIE_NAME)
    
    return {"success": True}

@router.get("/.well-known/jwks.json")
async def get_jwks(db: Annotated[AsyncSession, Depends(get_db)]):
    # Fetch keys from DB
    result = await db.execute(select(Jwks))
    keys = result.scalars().all()
    
    # Format as JWKS
    jwks_keys = []
    for key in keys:
        import json
        try:
            key_data = json.loads(key.publicKey)
            jwks_keys.append(key_data)
        except:
            pass
            
    return {"keys": jwks_keys}
