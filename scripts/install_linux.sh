#!/bin/bash

# =============================================================================
# اسکریپت نصب سیستم SSO روی Linux
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get user input
get_input() {
    read -p "$1: " input
    echo "$input"
}

# Function to get yes/no input
get_yes_no() {
    while true; do
        read -p "$1 (y/n): " yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            * ) echo "لطفاً y یا n وارد کنید.";;
        esac
    done
}

# =============================================================================
# شروع اسکریپت
# =============================================================================

echo "=========================================="
echo "🚀 نصب سیستم SSO روی Linux"
echo "=========================================="
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "این اسکریپت نباید با root اجرا شود!"
   print_warning "لطفاً با کاربر عادی اجرا کنید."
   exit 1
fi

# Get project directory
PROJECT_DIR=$(pwd)
print_status "مسیر پروژه: $PROJECT_DIR"

# Default domain
DEFAULT_DOMAIN="auth.avinoo.ir"

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    print_error "فایل manage.py یافت نشد!"
    print_warning "لطفاً در مسیر اصلی پروژه SSO باشید."
    exit 1
fi

# =============================================================================
# بررسی و نصب Python
# =============================================================================

print_status "بررسی Python..."

if ! command_exists python3; then
    print_warning "Python3 نصب نیست. در حال نصب..."
    
    # Detect OS and install Python
    if command_exists apt-get; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv python3-dev
    elif command_exists yum; then
        # CentOS/RHEL
        sudo yum update -y
        sudo yum install -y python3 python3-pip python3-venv python3-devel
    elif command_exists dnf; then
        # Fedora
        sudo dnf update -y
        sudo dnf install -y python3 python3-pip python3-venv python3-devel
    elif command_exists pacman; then
        # Arch Linux
        sudo pacman -Syu --noconfirm python python-pip
    else
        print_error "سیستم عامل پشتیبانی نمی‌شود!"
        exit 1
    fi
else
    print_success "Python3 نصب است"
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
print_status "نسخه Python: $PYTHON_VERSION"

if [[ $(echo "$PYTHON_VERSION < 3.9" | bc -l) -eq 1 ]]; then
    print_error "Python 3.9 یا بالاتر مورد نیاز است!"
    exit 1
fi

# =============================================================================
# ایجاد Virtual Environment
# =============================================================================

print_status "ایجاد Virtual Environment..."

if [ -d "venv" ]; then
    print_warning "Virtual Environment موجود است."
    if get_yes_no "آیا می‌خواهید آن را حذف و دوباره ایجاد کنید؟"; then
        rm -rf venv
        print_status "Virtual Environment قدیمی حذف شد."
    else
        print_status "استفاده از Virtual Environment موجود..."
    fi
fi

if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual Environment ایجاد شد"
fi

# Activate virtual environment
source venv/bin/activate
print_success "Virtual Environment فعال شد"

# Upgrade pip
print_status "به‌روزرسانی pip..."
pip install --upgrade pip

# =============================================================================
# نصب Dependencies
# =============================================================================

print_status "نصب Dependencies..."

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Dependencies نصب شدند"
else
    print_error "فایل requirements.txt یافت نشد!"
    exit 1
fi

# =============================================================================
# تنظیمات Environment
# =============================================================================

print_status "تنظیمات Environment..."

if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        cp env.example .env
        print_success "فایل .env از env.example ایجاد شد"
    else
        print_warning "فایل env.example یافت نشد. ایجاد فایل .env..."
        # Ask for domain
        DOMAIN=$(get_input "دامنه (پیش‌فرض: $DEFAULT_DOMAIN)")
        DOMAIN=${DOMAIN:-$DEFAULT_DOMAIN}
        
        # Ask for environment
        ENV_TYPE=$(get_input "نوع محیط (development/production) (پیش‌فرض: production)")
        ENV_TYPE=${ENV_TYPE:-production}
        
        if [ "$ENV_TYPE" = "production" ]; then
            cat > .env << EOF
# Django Settings
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN

# Microservice Configuration
AUTH_SERVICE_DOMAIN=$DOMAIN
ALLOWED_CLIENT_DOMAINS=app1.avinoo.ir,app2.avinoo.ir

# SSO Configuration
SSO_REDIRECT_URL=https://{domain}/callback
SSO_LOGIN_URL=https://{domain}/login
SSO_LOGOUT_URL=https://{domain}/logout

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=7

# CORS Settings
CORS_ALLOWED_ORIGINS=https://app1.avinoo.ir,https://app2.avinoo.ir,https://$DOMAIN

# Security Settings
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Logging
LOG_LEVEL=WARNING
EOF
        else
            cat > .env << EOF
# Django Settings
SECRET_KEY=django-insecure-change-this-in-development
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,$DOMAIN

# Microservice Configuration
AUTH_SERVICE_DOMAIN=$DOMAIN
ALLOWED_CLIENT_DOMAINS=127.0.0.1:8000,localhost:3000

# SSO Configuration
SSO_REDIRECT_URL=http://{domain}/callback
SSO_LOGIN_URL=http://{domain}/login
SSO_LOGOUT_URL=http://{domain}/logout

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=7

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://$DOMAIN

# Logging
LOG_LEVEL=INFO
EOF
        fi
        print_success "فایل .env ایجاد شد"
    fi
else
    print_warning "فایل .env موجود است"
fi

# =============================================================================
# تنظیمات Database
# =============================================================================

print_status "تنظیمات Database..."

# Database configuration
print_status "تنظیمات دیتابیس..."

if get_yes_no "آیا می‌خواهید از PostgreSQL استفاده کنید؟ (پیش‌فرض: SQLite)"; then
    if command_exists psql; then
        print_status "PostgreSQL نصب است"
        
        DB_NAME=$(get_input "نام دیتابیس (پیش‌فرض: auth_service_db)")
        DB_NAME=${DB_NAME:-auth_service_db}
        
        DB_USER=$(get_input "نام کاربر دیتابیس (پیش‌فرض: auth_user)")
        DB_USER=${DB_USER:-auth_user}
        
        DB_PASSWORD=$(get_input "رمز عبور دیتابیس")
        
        # Update .env file
        sed -i "s/# DB_ENGINE=/DB_ENGINE=django.db.backends.postgresql/" .env
        sed -i "s/# DB_NAME=/DB_NAME=$DB_NAME/" .env
        sed -i "s/# DB_USER=/DB_USER=$DB_USER/" .env
        sed -i "s/# DB_PASSWORD=/DB_PASSWORD=$DB_PASSWORD/" .env
        sed -i "s/# DB_HOST=/DB_HOST=localhost/" .env
        sed -i "s/# DB_PORT=/DB_PORT=5432/" .env
        
        print_success "تنظیمات PostgreSQL به‌روزرسانی شد"
    else
        print_warning "PostgreSQL نصب نیست. استفاده از SQLite"
    fi
else
    print_status "استفاده از SQLite (پیش‌فرض)"
fi

# =============================================================================
# Migration و Setup
# =============================================================================

print_status "اجرای Migration..."

# Create logs directory
mkdir -p logs

# Run migrations
python manage.py makemigrations
python manage.py migrate

print_success "Migration ها اجرا شدند"

# =============================================================================
# ایجاد Superuser
# =============================================================================

print_status "ایجاد Superuser..."

if get_yes_no "آیا می‌خواهید Superuser ایجاد کنید؟"; then
    USERNAME=$(get_input "نام کاربری (پیش‌فرض: admin)")
    USERNAME=${USERNAME:-admin}
    
    EMAIL=$(get_input "ایمیل (پیش‌فرض: admin@example.com)")
    EMAIL=${EMAIL:-admin@example.com}
    
    echo "رمز عبور را وارد کنید:"
    python manage.py createsuperuser --username "$USERNAME" --email "$EMAIL"
    
    print_success "Superuser ایجاد شد"
else
    print_warning "Superuser ایجاد نشد. می‌توانید بعداً با دستور زیر ایجاد کنید:"
    print_warning "python manage.py createsuperuser"
fi

# =============================================================================
# ایجاد کلیدهای RSA
# =============================================================================

print_status "ایجاد کلیدهای RSA..."

# Create keys directory
mkdir -p keys

# Generate RSA keys
python manage.py shell << EOF
from sso.utils import generate_rsa_keys
try:
    generate_rsa_keys()
    print("کلیدهای RSA ایجاد شدند")
except Exception as e:
    print(f"خطا در ایجاد کلیدهای RSA: {e}")
EOF

# =============================================================================
# ایجاد Systemd Service
# =============================================================================

if get_yes_no "آیا می‌خواهید Systemd Service ایجاد کنید؟"; then
    print_status "ایجاد Systemd Service..."
    
    SERVICE_NAME="sso-service"
    SERVICE_USER=$(whoami)
    SERVICE_PATH="$PROJECT_DIR"
    
    sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null << EOF
[Unit]
Description=SSO Authentication Service
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$SERVICE_PATH
Environment=PATH=$SERVICE_PATH/venv/bin
ExecStart=$SERVICE_PATH/venv/bin/python manage.py runserver 0.0.0.0:8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

    # Reload systemd and enable service
    sudo systemctl daemon-reload
    sudo systemctl enable $SERVICE_NAME
    
    print_success "Systemd Service ایجاد شد"
    print_status "برای شروع سرویس: sudo systemctl start $SERVICE_NAME"
    print_status "برای توقف سرویس: sudo systemctl stop $SERVICE_NAME"
    print_status "برای وضعیت سرویس: sudo systemctl status $SERVICE_NAME"
fi

# =============================================================================
# ایجاد Nginx Configuration
# =============================================================================

if get_yes_no "آیا می‌خواهید تنظیمات Nginx ایجاد کنید؟"; then
    print_status "ایجاد تنظیمات Nginx..."
    
    DOMAIN=$(get_input "دامنه (پیش‌فرض: $DEFAULT_DOMAIN)")
    DOMAIN=${DOMAIN:-$DEFAULT_DOMAIN}
    
    # Check if Let's Encrypt is available
    if command_exists certbot; then
        print_status "Let's Encrypt موجود است. ایجاد تنظیمات HTTPS..."
        
        sudo tee /etc/nginx/sites-available/sso-service > /dev/null << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-Host \$host;
        proxy_set_header X-Forwarded-Port \$server_port;
    }
    
    location /static/ {
        alias $SERVICE_PATH/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias $SERVICE_PATH/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF
        
        # Enable site
        sudo ln -sf /etc/nginx/sites-available/sso-service /etc/nginx/sites-enabled/
        
        # Test nginx configuration
        sudo nginx -t
        
        if [ $? -eq 0 ]; then
            sudo systemctl reload nginx
            
            # Get SSL certificate
            print_status "دریافت گواهی SSL از Let's Encrypt..."
            sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
            
            print_success "تنظیمات Nginx با HTTPS ایجاد شد"
            print_status "دامنه: https://$DOMAIN"
        else
            print_error "خطا در تنظیمات Nginx!"
        fi
    else
        print_warning "Let's Encrypt نصب نیست. ایجاد تنظیمات HTTP..."
        
        sudo tee /etc/nginx/sites-available/sso-service > /dev/null << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /static/ {
        alias $SERVICE_PATH/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias $SERVICE_PATH/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF
        
        # Enable site
        sudo ln -sf /etc/nginx/sites-available/sso-service /etc/nginx/sites-enabled/
        
        # Test nginx configuration
        sudo nginx -t
        
        if [ $? -eq 0 ]; then
            sudo systemctl reload nginx
            print_success "تنظیمات Nginx ایجاد شد"
            print_status "دامنه: http://$DOMAIN"
            print_warning "برای HTTPS، Let's Encrypt نصب کنید: sudo apt install certbot python3-certbot-nginx"
        else
            print_error "خطا در تنظیمات Nginx!"
        fi
    fi

    # Enable site
    sudo ln -sf /etc/nginx/sites-available/sso-service /etc/nginx/sites-enabled/
    
    # Test nginx configuration
    sudo nginx -t
    
    if [ $? -eq 0 ]; then
        sudo systemctl reload nginx
        print_success "تنظیمات Nginx ایجاد شد"
        print_status "دامنه: http://$DOMAIN"
    else
        print_error "خطا در تنظیمات Nginx!"
    fi
fi

# =============================================================================
# جمع‌آوری Static Files
# =============================================================================

print_status "جمع‌آوری Static Files..."

python manage.py collectstatic --noinput

print_success "Static Files جمع‌آوری شدند"

# =============================================================================
# تست سیستم
# =============================================================================

print_status "تست سیستم..."

# Test database connection
python manage.py check

if [ $? -eq 0 ]; then
    print_success "تست سیستم موفق بود"
else
    print_error "خطا در تست سیستم!"
    exit 1
fi

# =============================================================================
# خلاصه نصب
# =============================================================================

echo ""
echo "=========================================="
echo "✅ نصب سیستم SSO تکمیل شد!"
echo "=========================================="
echo ""
echo "📁 مسیر پروژه: $PROJECT_DIR"
echo "🐍 Virtual Environment: $PROJECT_DIR/venv"
echo "⚙️  تنظیمات: $PROJECT_DIR/.env"
echo "📊 دیتابیس: SQLite (پیش‌فرض)"
echo ""
echo "🚀 برای شروع:"
echo "   cd $PROJECT_DIR"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "🌐 آدرس‌های مفید:"
if [ -f "/etc/nginx/sites-available/sso-service" ]; then
    DOMAIN=$(grep "server_name" /etc/nginx/sites-available/sso-service | head -1 | awk '{print $2}' | sed 's/;//')
    if grep -q "ssl_certificate" /etc/nginx/sites-available/sso-service; then
        echo "   - صفحه تست: https://$DOMAIN/test/"
        echo "   - صفحه ورود: https://$DOMAIN/login/"
        echo "   - Admin Panel: https://$DOMAIN/admin/"
    else
        echo "   - صفحه تست: http://$DOMAIN/test/"
        echo "   - صفحه ورود: http://$DOMAIN/login/"
        echo "   - Admin Panel: http://$DOMAIN/admin/"
    fi
else
    echo "   - صفحه تست: http://127.0.0.1:8000/test/"
    echo "   - صفحه ورود: http://127.0.0.1:8000/login/"
    echo "   - Admin Panel: http://127.0.0.1:8000/admin/"
fi
echo ""
echo "📚 مستندات:"
echo "   - README: $PROJECT_DIR/README_SSO.md"
echo "   - راهنمای کامل: $PROJECT_DIR/docs/SSO_USAGE.md"
echo "   - تنظیمات: $PROJECT_DIR/docs/CONFIGURATION.md"
echo ""
echo "🔧 مدیریت سرویس:"
if [ -f "/etc/systemd/system/sso-service.service" ]; then
    echo "   sudo systemctl start sso-service"
    echo "   sudo systemctl stop sso-service"
    echo "   sudo systemctl status sso-service"
fi
echo ""
echo "📝 لاگ‌ها:"
echo "   tail -f $PROJECT_DIR/logs/django.log"
echo ""
echo "=========================================="
print_success "نصب کامل شد! 🎉"
echo "=========================================="
