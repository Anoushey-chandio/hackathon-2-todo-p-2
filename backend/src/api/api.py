from fastapi import APIRouter
from .endpoints import tasks, auth

api_router = APIRouter()
api_router.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
api_router.include_router(auth.router, prefix="/api/auth", tags=["auth"])
