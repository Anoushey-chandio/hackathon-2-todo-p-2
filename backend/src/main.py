from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.api.api import api_router
from src.api.errors import APIError
from fastapi.middleware.cors import CORSMiddleware
from src.core.database import init_db, async_engine
from src.core.config import settings
from contextlib import asynccontextmanager
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load env vars from backend/.env relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=BASE_DIR / "backend" / ".env", override=True)

logger.info(f"DEBUG main.py: settings.DATABASE_URL={settings.DATABASE_URL}")

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

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "message": str(exc)},
    )

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}
