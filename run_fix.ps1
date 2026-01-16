$ErrorActionPreference = "Stop"
$backend_root = Join-Path $PWD "backend"
$env:PYTHONPATH = $backend_root
$python = Join-Path $backend_root ".venv\Scripts\python.exe"
$alembic = Join-Path $backend_root ".venv\Scripts\alembic.exe"

Write-Host "Installing dependencies..."
& $python -m pip install httpx asyncpg psycopg2-binary python-multipart sqlalchemy[asyncio] greenlet

Write-Host "Running migrations..."
Set-Location $backend_root
# check if alembic exists, if not try python -m alembic
if (-not (Test-Path $alembic)) {
    Write-Host "Alembic exe not found, using python module..."
    & $python -m alembic revision --autogenerate -m "add_user_password"
    & $python -m alembic upgrade head
} else {
    & $alembic revision --autogenerate -m "add_user_password"
    & $alembic upgrade head
}

Write-Host "Verifying DB..."
& $python verify_db_setup.py
