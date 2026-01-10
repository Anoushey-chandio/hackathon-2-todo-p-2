from fastapi import APIRouter
from .endpoints import tasks

api_router = APIRouter()
api_router.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
