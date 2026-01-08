from fastapi import APIRouter

router = APIRouter()

# Auth is now handled by BetterAuth on the frontend/Next.js side.
# Backend verifies sessions via database access.
