#!/bin/bash
# Start Todo App - Backend and Frontend
# This script starts both servers

echo ""
echo "================================================================================"
echo " TODO APP STARTUP"
echo "================================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.11+ and add it to your PATH"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js 18+ and add it to your PATH"
    exit 1
fi

echo "INFO: Python version:"
python3 --version
echo ""
echo "INFO: Node.js version:"
node --version
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
}

trap cleanup EXIT

# Start Backend
echo "Starting Backend (FastAPI)..."
cd "$SCRIPT_DIR/backend"

# Activate or create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install dependencies if needed
pip install -q -r requirements.txt 2>/dev/null || true

# Start backend
python3 -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start Frontend
echo ""
echo "Starting Frontend (Next.js)..."
cd "$SCRIPT_DIR/frontend"

# Install dependencies if needed
npm install -q 2>/dev/null || true

# Start frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "================================================================================"
echo " SERVERS STARTED"
echo "================================================================================"
echo ""
echo "Backend:  http://127.0.0.1:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop servers"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
