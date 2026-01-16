$ErrorActionPreference = "Stop"

# Paths
$root = $PWD
$backend_root = Join-Path $root "backend"
$frontend_root = Join-Path $root "frontend"

# Kill existing processes on ports 8000 and 3000 (simple approach)
# On windows, netstat -ano | findstr :8000 -> taskkill
# Skipping cleanup for now, assuming clean env or user will restart sandbox

# Backend Start
Write-Host "Starting Backend..."
Set-Location $backend_root
$env:PYTHONPATH = $backend_root
$uvicorn = Join-Path $backend_root ".venv\Scripts\uvicorn.exe"

# Start-Process allows independent execution
Start-Process -FilePath $uvicorn -ArgumentList "src.main:app", "--reload", "--host", "127.0.0.1", "--port", "8000" -RedirectStandardOutput "$root\backend.log" -RedirectStandardError "$root\backend_err.log" -PassThru -NoNewWindow

# Frontend Start
Write-Host "Starting Frontend..."
Set-Location $frontend_root

# Check if node_modules exists, if not install
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing frontend dependencies..."
    npm install
}

# Start Next.js
# Use cmd /c to run npm properly
Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "npm run dev" -RedirectStandardOutput "$root\frontend.log" -RedirectStandardError "$root\frontend_err.log" -PassThru -NoNewWindow

Write-Host "Services started. Waiting 10s for initialization..."
Start-Sleep -Seconds 10

Write-Host "Running Auth Test..."
Set-Location $root
# Run python test
& "$backend_root\.venv\Scripts\python.exe" test_auth_flow.py
