from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from src.core.database import get_db, AsyncSession
from src.models.user import User
from src.models.auth import Account
from src.schemas.user import UserCreate, UserLogin, Token
from src.core.security import get_password_hash, verify_password, create_access_token
import uuid
from datetime import datetime, timezone

router = APIRouter()

@router.post("/signup", response_model=Token)
async def signup(
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

    # Create User
    user_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
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
        accountId=account_id, # Better Auth quirk? usually just id.
        providerId="credential",
        userId=user_id,
        password=hashed_password,
        createdAt=now,
        updatedAt=now
    )
    db.add(account)
    
    await db.commit()
    await db.refresh(user)

    # Generate Token
    access_token = create_access_token(data={"sub": user.id})
    return Token(access_token=access_token, token_type="bearer")

@router.post("/login", response_model=Token)
async def login(
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
    # In reality a user might have multiple accounts (google, etc), we need the one with password
    accounts = result.scalars().all()
    account = next((a for a in accounts if a.password), None)

    if not account or not verify_password(user_in.password, account.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.id})
    return Token(access_token=access_token, token_type="bearer")
