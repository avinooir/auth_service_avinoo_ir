#!/bin/bash

# 🔐 Auth Service Setup Script
# سکریپت نصب خودکار سرویس احراز هویت مرکزی

echo "🚀 شروع نصب سرویس احراز هویت مرکزی Avinoo.ir"
echo "================================================"

# بررسی Python
if ! command -v python &> /dev/null; then
    echo "❌ Python یافت نشد. لطفاً Python 3.9+ نصب کنید."
    exit 1
fi

PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION یافت شد"

# ایجاد محیط مجازی
echo "📦 ایجاد محیط مجازی..."
python -m venv venv

# فعال‌سازی محیط مجازی
echo "🔧 فعال‌سازی محیط مجازی..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# نصب وابستگی‌ها
echo "📚 نصب وابستگی‌ها..."
pip install --upgrade pip
pip install -r requirements.txt

# کپی فایل محیط
echo "⚙️ تنظیم فایل محیط..."
if [ ! -f .env ]; then
    cp env.example .env
    echo "✅ فایل .env ایجاد شد"
else
    echo "⚠️ فایل .env از قبل موجود است"
fi

# ایجاد دایرکتوری‌های لازم
echo "📁 ایجاد دایرکتوری‌های لازم..."
mkdir -p logs media/avatars staticfiles keys

# تولید کلیدهای RSA
echo "🔑 تولید کلیدهای RSA..."
python scripts/generate_rsa_keys.py

# اجرای مایگریشن‌ها
echo "🗄️ اجرای مایگریشن‌ها..."
python manage.py makemigrations
python manage.py migrate

# ایجاد superuser
echo "👤 ایجاد superuser..."
python scripts/create_superuser.py

# ایجاد کلاینت‌های SSO
echo "🔗 ایجاد کلاینت‌های SSO..."
python scripts/create_sso_clients.py

# جمع‌آوری فایل‌های استاتیک
echo "📦 جمع‌آوری فایل‌های استاتیک..."
python manage.py collectstatic --noinput

echo ""
echo "🎉 نصب با موفقیت تکمیل شد!"
echo "================================"
echo ""
echo "📝 اطلاعات مهم:"
echo "• Admin Panel: http://127.0.0.1:8000/admin/"
echo "• Username: admin"
echo "• Password: admin123456"
echo ""
echo "🌐 URL های تست:"
echo "• Auth Service: http://127.0.0.1:8000"
echo "• App1: http://127.0.0.1:8000/client_apps/app1/index.html"
echo "• App2: http://127.0.0.1:8000/client_apps/app2/index.html"
echo ""
echo "🚀 برای اجرای سرور:"
echo "python manage.py runserver"
echo ""
echo "🧪 برای تست API:"
echo "python scripts/test_sso_api.py"
echo ""
echo "⚠️ نکات مهم:"
echo "• رمز عبور admin را بعد از اولین ورود تغییر دهید"
echo "• فایل .env را با تنظیمات Production به‌روزرسانی کنید"
echo "• کلیدهای RSA را در جای امن نگهداری کنید"
echo ""
echo "📚 مستندات کامل در فایل README.md موجود است"
echo ""
echo "✅ آماده استفاده!"