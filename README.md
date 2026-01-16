# Full-Stack Todo App

A modern, secure Todo application built with Next.js, FastAPI, and PostgreSQL (Neon).

## Features

- **Authentication**: Secure Signup & Login with JWT (HttpOnly cookies).
- **Tasks**: Create, Read, Update, Delete tasks.
- **Privacy**: Strict data isolation per user.
- **Responsive UI**: Built with Tailwind CSS.

## Tech Stack

- **Frontend**: Next.js 16 (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python 3.11+), SQLModel (SQLAlchemy)
- **Database**: PostgreSQL (Neon)

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL Database URL

### Setup

1. **Clone the repository**
2. **Environment Variables**:
   - Create `backend/.env` with `DATABASE_URL` and `BETTER_AUTH_SECRET`.
   - Create `frontend/.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8000`.

3. **Install Dependencies**:
   ```bash
   # Backend
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt

   # Frontend
   cd frontend
   npm install
   ```

4. **Run Application**:
   - **Windows**: Run `START_APP.bat` or `start_services.ps1`.
   - **Manual**:
     - Backend: `uvicorn src.main:app --reload`
     - Frontend: `npm run dev`

5. **Access**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

## Implementation Details

- **Auth**: JWT tokens are issued on login and stored in the database `session` table for revocation support.
- **API**: RESTful endpoints protected by `get_current_user` dependency.
- **Frontend**: Uses `fetch` proxy to backend to handle CORS and cookies securely.