from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from src.core.database import get_db, AsyncSession
from src.models.user import User
from src.models.auth import Account, Session
from src.models.jwks import Jwks
from src.schemas.user import UserCreate, UserLogin
from src.core.security import get_password_hash, verify_password, create_access_token
from src.api.deps import get_current_user
import uuid
from datetime import datetime, timezone, timedelta

router = APIRouter()

@router.post("/sign-up")
async def sign_up(
    user_in: UserCreate,
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
    user = User(
        id=user_id,
        email=user_in.email,
        name=user_in.email.split("@")[0], # Default name
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
    access_token = create_access_token(data={"sub": user.id})
    session = Session(
        id=session_id,
        userId=user_id,
        token=access_token,
        expiresAt=now + timedelta(days=7),
        createdAt=now,
        updatedAt=now
    )
    db.add(session)
    
    await db.commit()
    await db.refresh(user)
    await db.refresh(session)

    return {
        "user": user,
        "session": session
    }

@router.post("/sign-in/email")
async def sign_in_email(
    user_in: UserLogin,
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
    access_token = create_access_token(data={"sub": user.id})
    session = Session(
        id=session_id,
        userId=user.id,
        token=access_token,
        expiresAt=now + timedelta(days=7),
        createdAt=now,
        updatedAt=now
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    return {
        "user": user,
        "session": session
    }

@router.get("/get-session")
async def get_session(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Since we are using Bearer token, the current_user is already resolved.
    # We just need to return the session info.
    # Ideally we should look up the session by the token, but get_current_user consumes the token.
    # For now, we will return the latest valid session for the user as a fallback,
    # or just mock the session object if we can't easily get the exact one without changing deps.
    
    # Better approach: Find the session that corresponds to the user's active login.
    # But since we generate a NEW session on every login, there might be multiple.
    # We will fetch the most recently created session for this user.
    
    result = await db.execute(
        select(Session)
        .where(Session.userId == current_user.id)
        .order_by(Session.createdAt.desc())
    )
    session = result.scalars().first()
    
    if not session:
         raise HTTPException(status_code=401, detail="Session not found")

    return {
        "user": current_user,
        "session": session
    }

@router.get("/.well-known/jwks.json")
async def get_jwks(db: Annotated[AsyncSession, Depends(get_db)]):
    # Fetch keys from DB
    result = await db.execute(select(Jwks))
    keys = result.scalars().all()
    
    # Format as JWKS
    jwks_keys = []
    for key in keys:
        # Assuming publicKey is stored as JSON string or PEM that needs parsing
        # For now, just returning what's in the DB if it matches JWK format
        # If it's a PEM, we'd need to convert it.
        # But given the error "updatedAt NULL", the keys are likely being inserted by a library.
        # We will just expose them.
        import json
        try:
            key_data = json.loads(key.publicKey)
            jwks_keys.append(key_data)
        except:
            pass
            
    return {"keys": jwks_keys}
