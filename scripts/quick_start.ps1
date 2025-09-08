# =============================================================================
# اسکریپت شروع سریع سیستم SSO روی Windows
# =============================================================================

Write-Host "🚀 شروع سریع سیستم SSO" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "ایجاد Virtual Environment..." -ForegroundColor Blue
    python -m venv venv
}

# Activate virtual environment
Write-Host "فعال‌سازی Virtual Environment..." -ForegroundColor Blue
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "نصب Dependencies..." -ForegroundColor Blue
pip install -r requirements.txt

# Create .env if not exists
if (-not (Test-Path ".env")) {
    Write-Host "ایجاد فایل .env..." -ForegroundColor Blue
    Copy-Item "env.example" ".env"
}

# Create logs directory
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs"
}

# Run migrations
Write-Host "اجرای Migration..." -ForegroundColor Blue
python manage.py makemigrations
python manage.py migrate

# Collect static files
Write-Host "جمع‌آوری Static Files..." -ForegroundColor Blue
python manage.py collectstatic --noinput

# Create superuser if not exists
$superuserExists = python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('exists' if User.objects.filter(is_superuser=True).exists() else '')" 2>$null

if (-not $superuserExists) {
    Write-Host "ایجاد Superuser..." -ForegroundColor Blue
    Write-Host "نام کاربری: admin"
    Write-Host "ایمیل: admin@example.com"
    python manage.py createsuperuser --username admin --email admin@example.com
}

# Create RSA keys
Write-Host "ایجاد کلیدهای RSA..." -ForegroundColor Blue
$pythonScript = @"
from sso.utils import generate_rsa_keys
try:
    generate_rsa_keys()
    print('کلیدهای RSA ایجاد شدند')
except Exception as e:
    print(f'خطا در ایجاد کلیدهای RSA: {e}')
"@

$pythonScript | python

Write-Host ""
Write-Host "✅ سیستم SSO آماده است!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 آدرس‌های مفید:" -ForegroundColor White
Write-Host "   - صفحه تست: http://127.0.0.1:8000/test/" -ForegroundColor White
Write-Host "   - صفحه ورود: http://127.0.0.1:8000/login/" -ForegroundColor White
Write-Host "   - Admin Panel: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host ""
Write-Host "🚀 برای شروع سرور:" -ForegroundColor White
Write-Host "   python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "📚 مستندات:" -ForegroundColor White
Write-Host "   - README: README_SSO.md" -ForegroundColor White
Write-Host "   - راهنمای کامل: docs\SSO_USAGE.md" -ForegroundColor White
Write-Host "   - تنظیمات: docs\CONFIGURATION.md" -ForegroundColor White
Write-Host ""
