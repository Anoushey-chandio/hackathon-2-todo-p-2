# Quickstart: Phase II Todo App

## Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (Neon) - URL in `.env`

## Backend Setup (FastAPI)

1. Navigate to backend directory:
   ```bash
   cd backend
   ```
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy asyncpg alembic python-jose[cryptography] passlib[bcrypt] python-multipart
   ```
4. Run migrations:
   ```bash
   alembic upgrade head
   ```
5. Start server:
   ```bash
   uvicorn main:app --reload
   ```
   API available at `http://localhost:8000`

## Frontend Setup (Next.js)

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start development server:
   ```bash
   npm run dev
   ```
   App available at `http://localhost:3000`

## Environment Variables (.env)

Ensure root `.env` contains:
```
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
SECRET_KEY=your_secret_key_for_jwt
```
