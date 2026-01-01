# Quick Commands Reference
# Copy and paste these commands as needed

Write-Host "📋 Smart Waste Management - Quick Commands" -ForegroundColor Green
Write-Host "==========================================`n" -ForegroundColor Green

Write-Host "1️⃣  QUICK START (First time setup):" -ForegroundColor Cyan
Write-Host "   .\quickstart.ps1`n" -ForegroundColor White

Write-Host "2️⃣  RUN SERVER (Daily use - AUTO activates venv):" -ForegroundColor Cyan
Write-Host "   .\run.ps1`n" -ForegroundColor White

Write-Host "3️⃣  MANUAL ACTIVATION (if needed):" -ForegroundColor Cyan
Write-Host "   .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   python manage.py runserver`n" -ForegroundColor White

Write-Host "4️⃣  RUN WITHOUT ACTIVATION (use full path):" -ForegroundColor Cyan
Write-Host "   .\.venv\Scripts\python.exe manage.py runserver`n" -ForegroundColor White

Write-Host "5️⃣  CREATE ADMIN USER:" -ForegroundColor Cyan
Write-Host "   python make_admin.py`n" -ForegroundColor White

Write-Host "6️⃣  CHECK DATABASE:" -ForegroundColor Cyan
Write-Host "   python check_records.py`n" -ForegroundColor White

Write-Host "7️⃣  RUN MIGRATIONS:" -ForegroundColor Cyan
Write-Host "   python manage.py makemigrations" -ForegroundColor White
Write-Host "   python manage.py migrate`n" -ForegroundColor White

Write-Host "==========================================`n" -ForegroundColor Green
Write-Host "💡 TIP: With VS Code settings updated, new terminals" -ForegroundColor Yellow
Write-Host "   will automatically activate venv!" -ForegroundColor Yellow
Write-Host "`n   Just type: python manage.py runserver`n" -ForegroundColor White

Write-Host "🎯 RECOMMENDED: Use .\run.ps1 for simplest startup`n" -ForegroundColor Green
