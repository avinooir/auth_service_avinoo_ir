#!/bin/bash

# =============================================================================
# اسکریپت اصلاح ALLOWED_HOSTS برای سرور فعلی
# =============================================================================

echo "🔧 اصلاح ALLOWED_HOSTS..."

# Check if .env file exists
if [ -f ".env" ]; then
    echo "📝 به‌روزرسانی فایل .env..."
    
    # Backup original file
    cp .env .env.backup
    
    # Update ALLOWED_HOSTS
    sed -i 's/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=localhost,127.0.0.1,auth.avinoo.ir,87.248.150.86/' .env
    
    echo "✅ فایل .env به‌روزرسانی شد"
else
    echo "⚠️  فایل .env یافت نشد. ایجاد فایل جدید..."
    
    cat > .env << EOF
# Django Settings
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,auth.avinoo.ir,87.248.150.86

# Microservice Configuration
AUTH_SERVICE_DOMAIN=auth.avinoo.ir
ALLOWED_CLIENT_DOMAINS=app1.avinoo.ir,app2.avinoo.ir

# SSO Configuration
SSO_REDIRECT_URL=http://{domain}/callback
SSO_LOGIN_URL=http://{domain}/login
SSO_LOGOUT_URL=http://{domain}/logout

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=7

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://87.248.150.86:4141

# Logging
LOG_LEVEL=INFO
EOF
    
    echo "✅ فایل .env ایجاد شد"
fi

# Restart service if systemd service exists
if systemctl is-active --quiet sso-service; then
    echo "🔄 راه‌اندازی مجدد سرویس..."
    sudo systemctl restart sso-service
    echo "✅ سرویس راه‌اندازی مجدد شد"
fi

echo ""
echo "🎉 مشکل ALLOWED_HOSTS حل شد!"
echo ""
echo "🌐 آدرس‌های قابل دسترسی:"
echo "   - http://87.248.150.86:4141/test/"
echo "   - http://87.248.150.86:4141/login/"
echo "   - http://87.248.150.86:4141/admin/"
echo ""
echo "📝 اگر سرویس systemd ندارید، سرور را دستی راه‌اندازی مجدد کنید:"
echo "   python manage.py runserver 0.0.0.0:4141"
