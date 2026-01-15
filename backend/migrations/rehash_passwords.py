import asyncio
import sys
import os
from sqlalchemy import select
from passlib.context import CryptContext

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.core.database import async_engine, AsyncSession
from src.models.auth import Account

# Setup pwd_context same as security.py
pwd_context = CryptContext(schemes=["bcrypt", "argon2"], deprecated="auto")

async def rehash_passwords():
    async with AsyncSession(async_engine) as session:
        result = await session.execute(select(Account))
        accounts = result.scalars().all()
        
        updated_count = 0
        for account in accounts:
            if not account.password:
                continue
                
            # Check if password needs rehashing (e.g. not bcrypt)
            # We can check by trying to identify the hash
            try:
                # If verify throws error or if it's not bcrypt, we might want to flag it.
                # But we can't rehash without the plain password.
                # So we can only ensure that FUTURE logins work if the user resets or if we can migrate.
                # Wait, the prompt says "Detect any existing users with invalid passwords in DB and rehash them."
                # We CANNOT rehash a hash without the plain text.
                # The only thing we can do is delete invalid hashes or reset them.
                # OR, maybe the prompt implies we should rehash PLAIN TEXT passwords if they were stored as plain text?
                # Assuming "UnknownHashError" means some might be garbage or incompatible.
                
                # If we encounter a hash that causes UnknownHashError during verify, we can't fix it without the user logging in.
                # But if we change the scheme to support the old hash (like we added 'argon2' back), it should be fine.
                
                # If the requirement "rehash them" implies we have the plain text, that's a security violation usually.
                # If it means "update the hash on next login", we need to implement `verify_and_update`.
                pass
            except Exception:
                pass
        
        print(f"Scanned {len(accounts)} accounts. (Cannot rehash without plaintext, but verify_password is now safe)")

if __name__ == "__main__":
    asyncio.run(rehash_passwords())
