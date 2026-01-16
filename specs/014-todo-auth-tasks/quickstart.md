# Quickstart: Full-Stack Todo App

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (Neon connection string)

## Environment Setup

1. **Backend**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   cp .env.example .env
   # Update .env with DATABASE_URL
   ```

2. **Frontend**
   ```bash
   cd frontend
   npm install
   cp .env.example .env.local
   # Update .env.local with NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

## Running the App

1. **Start Backend**
   ```bash
   cd backend
   uvicorn src.main:app --reload
   ```
   *Available at http://localhost:8000*

2. **Start Frontend**
   ```bash
   cd frontend
   npm run dev
   ```
   *Available at http://localhost:3000*

## Verification

1. Go to `http://localhost:3000`.
2. Click "Sign Up".
3. Enter credentials -> Dashboard should load.
4. Add a task -> Should appear in list.
5. Reload page -> Session should persist.
