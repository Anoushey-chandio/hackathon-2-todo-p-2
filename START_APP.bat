@echo off
REM Start Todo App - Backend and Frontend
REM This script starts both servers in separate windows

echo.
echo ================================================================================
echo  TODO APP STARTUP
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ and add it to your PATH
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ and add it to your PATH
    exit /b 1
)

echo INFO: Python version:
python --version
echo.
echo INFO: Node.js version:
node --version
echo.

REM Start Backend
echo Starting Backend (FastAPI)...
start "Todo Backend" cmd /k "cd /d %~dp0backend && python -m venv venv 2>nul || echo venv already exists... && venv\Scripts\activate && python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000"

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 3 /nobreak

REM Start Frontend
echo.
echo Starting Frontend (Next.js)...
start "Todo Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ================================================================================
echo  SERVERS STARTED
echo ================================================================================
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo.
echo Close either window to stop that server.
echo.
pause
