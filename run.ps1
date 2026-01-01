# Quick Run Script - Just start the Django server
# This script automatically activates venv and runs the server

Write-Host "🚀 Starting Smart Waste Management System..." -ForegroundColor Green
Write-Host "==========================================`n" -ForegroundColor Green

# Activate virtual environment
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment (.venv)..." -ForegroundColor Cyan
    & ".\.venv\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment activated`n" -ForegroundColor Green
} elseif (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment (venv)..." -ForegroundColor Cyan
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment activated`n" -ForegroundColor Green
} else {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run quickstart.ps1 first to create the virtual environment." -ForegroundColor Yellow
    exit 1
}

# Start Django server
Write-Host "Starting Django development server..." -ForegroundColor Cyan
Write-Host "Server will be available at: http://127.0.0.1:8000/" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server`n" -ForegroundColor Yellow
Write-Host "==========================================`n" -ForegroundColor Green

python manage.py runserver
