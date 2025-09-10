# PowerShell script to generate RSA keys
Write-Host "🔑 تولید کلیدهای RSA..." -ForegroundColor Green

# Create keys directory
if (!(Test-Path "keys")) {
    New-Item -ItemType Directory -Path "keys"
    Write-Host "📁 دایرکتوری keys ایجاد شد" -ForegroundColor Yellow
}

# Generate RSA keys using Python
Write-Host "🐍 اجرای Python script..." -ForegroundColor Cyan

try {
    python create_keys.py
    Write-Host "✅ کلیدهای RSA تولید شدند!" -ForegroundColor Green
} catch {
    Write-Host "❌ خطا در تولید کلیدها: $_" -ForegroundColor Red
    Write-Host "💡 لطفاً مطمئن شوید که Python و cryptography نصب شده است" -ForegroundColor Yellow
}

# Check if keys were created
if (Test-Path "keys/private_key.pem" -and Test-Path "keys/public_key.pem") {
    Write-Host "✅ کلیدها با موفقیت ایجاد شدند:" -ForegroundColor Green
    Write-Host "   - keys/private_key.pem" -ForegroundColor White
    Write-Host "   - keys/public_key.pem" -ForegroundColor White
} else {
    Write-Host "❌ کلیدها ایجاد نشدند" -ForegroundColor Red
}

Write-Host "`n🔧 برای تست JWT token:" -ForegroundColor Cyan
Write-Host "   python test_jwt_fix.py" -ForegroundColor White
