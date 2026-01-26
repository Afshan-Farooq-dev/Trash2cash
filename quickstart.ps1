# Quick Start Script for Smart Waste Management System
# Run this script to set up and start your Django application

Write-Host "🚀 Smart Waste Management System - Quick Start" -ForegroundColor Green
Write-Host "================================================`n" -ForegroundColor Green

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Python not found! Please install Python 3.8+ from python.org" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Cyan
if (Test-Path ".venv") {
    Write-Host "⚠️  Virtual environment already exists, skipping..." -ForegroundColor Yellow
}
elseif (Test-Path "venv") {
    Write-Host "⚠️  Old virtual environment found, skipping..." -ForegroundColor Yellow
}
else {
    python -m venv .venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Cyan
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    & ".\.venv\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment activated (.venv)" -ForegroundColor Green
}
elseif (Test-Path ".\venv\Scripts\Activate.ps1") {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment activated (venv)" -ForegroundColor Green
}
else {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Cyan
Write-Host "This may take a few minutes..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✅ Dependencies installed" -ForegroundColor Green

# Run migrations
Write-Host "`nSetting up database..." -ForegroundColor Cyan
python manage.py makemigrations
python manage.py migrate
Write-Host "✅ Database configured" -ForegroundColor Green

# Create superuser prompt
Write-Host "`n" -ForegroundColor White
Write-Host "================================================" -ForegroundColor Yellow
Write-Host "Would you like to create an admin superuser? (Y/N)" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Yellow
$createSuperuser = Read-Host "Enter Y or N"

if ($createSuperuser -eq "Y" -or $createSuperuser -eq "y") {
    Write-Host "`nCreating superuser..." -ForegroundColor Cyan
    python manage.py createsuperuser
    Write-Host "✅ Superuser created" -ForegroundColor Green
}
else {
    Write-Host "⚠️  Skipping superuser creation. You can create one later with: python manage.py createsuperuser" -ForegroundColor Yellow
}

# Start server
Write-Host "`n================================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host "`nStarting development server..." -ForegroundColor Cyan
Write-Host "`nYour application will be available at:" -ForegroundColor White
Write-Host "  🌐 Main App: http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host "  🔐 Admin Panel: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "================================================`n" -ForegroundColor Green

python manage.py runserver
