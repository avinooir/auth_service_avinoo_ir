# 🔐 Auth Service Setup Script for Windows
# سکریپت نصب خودکار سرویس احراز هویت مرکزی برای Windows

Write-Host "🚀 شروع نصب سرویس احراز هویت مرکزی Avinoo.ir" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# بررسی Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion یافت شد" -ForegroundColor Green
} catch {
    Write-Host "❌ Python یافت نشد. لطفاً Python 3.9+ نصب کنید." -ForegroundColor Red
    exit 1
}

# ایجاد محیط مجازی
Write-Host "📦 ایجاد محیط مجازی..." -ForegroundColor Yellow
python -m venv venv

# فعال‌سازی محیط مجازی
Write-Host "🔧 فعال‌سازی محیط مجازی..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# نصب وابستگی‌ها
Write-Host "📚 نصب وابستگی‌ها..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

# کپی فایل محیط
Write-Host "⚙️ تنظیم فایل محیط..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item "env.example" ".env"
    Write-Host "✅ فایل .env ایجاد شد" -ForegroundColor Green
} else {
    Write-Host "⚠️ فایل .env از قبل موجود است" -ForegroundColor Yellow
}

# ایجاد دایرکتوری‌های لازم
Write-Host "📁 ایجاد دایرکتوری‌های لازم..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
New-Item -ItemType Directory -Force -Path "media\avatars" | Out-Null
New-Item -ItemType Directory -Force -Path "staticfiles" | Out-Null
New-Item -ItemType Directory -Force -Path "keys" | Out-Null

# تولید کلیدهای RSA
Write-Host "🔑 تولید کلیدهای RSA..." -ForegroundColor Yellow
python scripts/generate_rsa_keys.py

# اجرای مایگریشن‌ها
Write-Host "🗄️ اجرای مایگریشن‌ها..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

# ایجاد superuser
Write-Host "👤 ایجاد superuser..." -ForegroundColor Yellow
python scripts/create_superuser.py

# ایجاد کلاینت‌های SSO
Write-Host "🔗 ایجاد کلاینت‌های SSO..." -ForegroundColor Yellow
python scripts/create_sso_clients.py

# جمع‌آوری فایل‌های استاتیک
Write-Host "📦 جمع‌آوری فایل‌های استاتیک..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

Write-Host ""
Write-Host "🎉 نصب با موفقیت تکمیل شد!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "📝 اطلاعات مهم:" -ForegroundColor Cyan
Write-Host "• Admin Panel: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host "• Username: admin" -ForegroundColor White
Write-Host "• Password: admin123456" -ForegroundColor White
Write-Host ""
Write-Host "🌐 URL های تست:" -ForegroundColor Cyan
Write-Host "• Auth Service: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "• App1: http://127.0.0.1:8000/client_apps/app1/index.html" -ForegroundColor White
Write-Host "• App2: http://127.0.0.1:8000/client_apps/app2/index.html" -ForegroundColor White
Write-Host ""
Write-Host "🚀 برای اجرای سرور:" -ForegroundColor Cyan
Write-Host "python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "🧪 برای تست API:" -ForegroundColor Cyan
Write-Host "python scripts/test_sso_api.py" -ForegroundColor White
Write-Host ""
Write-Host "⚠️ نکات مهم:" -ForegroundColor Yellow
Write-Host "• رمز عبور admin را بعد از اولین ورود تغییر دهید" -ForegroundColor White
Write-Host "• فایل .env را با تنظیمات Production به‌روزرسانی کنید" -ForegroundColor White
Write-Host "• کلیدهای RSA را در جای امن نگهداری کنید" -ForegroundColor White
Write-Host ""
Write-Host "📚 مستندات کامل در فایل README.md موجود است" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ آماده استفاده!" -ForegroundColor Green
