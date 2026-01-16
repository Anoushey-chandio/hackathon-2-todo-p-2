from fastapi import APIRouter
from .endpoints import tasks, auth

api_router = APIRouter(prefix="/api")
api_router.include_router(tasks.router, tags=["tasks"])
api_router.include_router(auth.router, tags=["auth"])
