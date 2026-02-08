# Quickstart: Todo Chatbot

**Branch**: `015-todo-chatbot`

## Prerequisites

1. **OpenRouter API Key**: Ensure `OPENROUTER_API_KEY` is set in `backend/.env`.
2. **Database**: Ensure Neon DB is running and accessible.

## Setup

1. **Install Dependencies**:
   ```bash
   cd backend
   # Ensure virtualenv is active
   pip install openai
   ```
   (Frontend dependencies like `ai` might need to be installed if using Vercel AI SDK, but we stick to standard fetch for this MVP unless Vercel SDK is mandated. *Correction*: Research decided on Vercel AI SDK).
   ```bash
   cd frontend
   npm install ai
   ```

2. **Database Migrations**:
   ```bash
   cd backend
   alembic revision --autogenerate -m "Add chat tables"
   alembic upgrade head
   ```

## Running the Feature

1. **Start Backend**:
   ```bash
   cd backend
   python main.py
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Verify**:
   - Navigate to `http://localhost:3000/tasks`.
   - Click the new "Chat" bubble icon in the bottom right.
   - Type "Add a task to call mom".
   - Verify "Call mom" appears in your task list.
