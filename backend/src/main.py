from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from dotenv import load_dotenv

from src.api.api import api_router
from src.api.errors import APIError
from src.core.database import init_db, async_engine
from src.core.config import settings

load_dotenv(override=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized.")
    yield
    logger.info("Closing database connection...")
    await async_engine.dispose()
    logger.info("Database connection closed.")

app = FastAPI(title="Todo App API", lifespan=lifespan)

# CORS - Must be BEFORE routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message, "details": exc.details}},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500, 
        content={"detail": "Internal Server Error", "message": str(exc)}
    )

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Backend is running successfully 🚀"}