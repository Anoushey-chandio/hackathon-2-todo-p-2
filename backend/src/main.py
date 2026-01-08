from fastapi import FastAPI
from src.api.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from src.core.database import init_db
from src.core.config import settings

print(f"DEBUG main.py: settings.DATABASE_URL={settings.DATABASE_URL}")

app = FastAPI(title="Todo App API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}