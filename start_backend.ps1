# AI Werewolf Backend Startup Script
# Resolve Windows GBK encoding issues

Write-Host "Starting AI Werewolf Backend Service..." -ForegroundColor Cyan

# Set UTF-8 encoding
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

# Check for .env file
if (-not (Test-Path ".env")) {
    Write-Host "WARNING: .env file not found" -ForegroundColor Yellow
    Write-Host "Please copy env.example.txt to .env and fill in your API keys" -ForegroundColor Yellow
    exit 1
}

Write-Host "Environment configured" -ForegroundColor Green
Write-Host "TTS service will use DashScope API" -ForegroundColor Green
Write-Host ""

# Start backend service
python main.py --mode web




