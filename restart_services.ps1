$ErrorActionPreference = "SilentlyContinue"
Write-Host "Stopping services..."
taskkill /F /IM uvicorn.exe
taskkill /F /IM node.exe
taskkill /F /IM python.exe # Be careful with this one, but verifying script runs in fresh python process
Start-Sleep -Seconds 2
$ErrorActionPreference = "Stop"

.\start_services.ps1
