$ErrorActionPreference = "Stop"
$backend_root = Join-Path $PWD "backend"
$python = Join-Path $backend_root ".venv\Scripts\python.exe"

Write-Host "Installing PyJWT..."
& $python -m pip install PyJWT

Write-Host "Restarting services..."
.\start_services.ps1
