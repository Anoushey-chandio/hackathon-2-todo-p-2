from fastapi import FastAPI
from src.api.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from src.core.database import init_db # Import init_db

app = FastAPI(title="Todo App API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Should be specific in production, e.g. ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.on_event("startup")
async def on_startup():
    await init_db() # Initialize the database on startup

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}