from fastapi import APIRouter
from src.api.endpoints import tasks, auth, chat

api_router = APIRouter(prefix="/api")

# Include routers with proper prefixes
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(tasks.router)

# Update chat router prefix to match current endpoint
# Backend chat router defines "/message" directly
api_router.include_router(chat.router, prefix="")  # no extra prefix
