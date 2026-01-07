# Todo App Phase II

Full-stack Todo application with Authentication.

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy (Async), Alembic, Pydantic
- **Frontend**: Next.js 16 (App Router), Tailwind CSS
- **Database**: PostgreSQL (Neon)
- **Auth**: JWT (OAuth2 Password Bearer)

## Setup

1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt # (Generate this)
   alembic upgrade head
   uvicorn src.main:app --reload
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Env**:
   Ensure `.env` in root has `DATABASE_URL` and `SECRET_KEY`.

## Features
- Signup/Login
- Protected Tasks Dashboard
- Add/Edit/Delete/Complete Tasks
- Responsive Theme
