#!/bin/bash

# =============================================================================
# اسکریپت شروع سریع سیستم SSO
# =============================================================================

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 شروع سریع سیستم SSO${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${BLUE}ایجاد Virtual Environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}فعال‌سازی Virtual Environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}نصب Dependencies...${NC}"
pip install -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo -e "${BLUE}ایجاد فایل .env...${NC}"
    cp env.example .env
fi

# Create logs directory
mkdir -p logs

# Run migrations
echo -e "${BLUE}اجرای Migration...${NC}"
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo -e "${BLUE}جمع‌آوری Static Files...${NC}"
python manage.py collectstatic --noinput

# Create superuser if not exists
if [ -z "$(python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('exists' if User.objects.filter(is_superuser=True).exists() else '')" 2>/dev/null)" ]; then
    echo -e "${BLUE}ایجاد Superuser...${NC}"
    echo "نام کاربری: admin"
    echo "ایمیل: admin@example.com"
    python manage.py createsuperuser --username admin --email admin@example.com
fi

# Create RSA keys
echo -e "${BLUE}ایجاد کلیدهای RSA...${NC}"
python manage.py shell -c "
from sso.utils import generate_rsa_keys
try:
    generate_rsa_keys()
    print('کلیدهای RSA ایجاد شدند')
except Exception as e:
    print(f'خطا در ایجاد کلیدهای RSA: {e}')
"

echo ""
echo -e "${GREEN}✅ سیستم SSO آماده است!${NC}"
echo ""
echo "🌐 آدرس‌های مفید:"
echo "   - صفحه تست: http://127.0.0.1:8000/test/"
echo "   - صفحه ورود: http://127.0.0.1:8000/login/"
echo "   - Admin Panel: http://127.0.0.1:8000/admin/"
echo ""
echo "🚀 برای شروع سرور:"
echo "   python manage.py runserver"
echo ""
echo "📚 مستندات:"
echo "   - README: README_SSO.md"
echo "   - راهنمای کامل: docs/SSO_USAGE.md"
echo "   - تنظیمات: docs/CONFIGURATION.md"
echo ""
