#!/bin/bash

# =============================================================================
# اسکریپت Deploy سیستم SSO برای Production
# مخصوص دامنه auth.avinoo.ir
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
DOMAIN="auth.avinoo.ir"
PROJECT_DIR="/opt/sso-service"
SERVICE_USER="sso"
SERVICE_NAME="sso-service"

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

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   print_error "این اسکریپت باید با root اجرا شود!"
   exit 1
fi

echo "=========================================="
echo "🚀 Deploy سیستم SSO برای Production"
echo "🌐 دامنه: $DOMAIN"
echo "=========================================="
echo ""

# =============================================================================
# نصب Dependencies سیستم
# =============================================================================

print_status "نصب Dependencies سیستم..."

# Update system
apt-get update

# Install required packages
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    nginx \
    certbot \
    python3-certbot-nginx \
    redis-server \
    git \
    curl \
    wget \
    unzip \
    build-essential

print_success "Dependencies سیستم نصب شدند"

# =============================================================================
# ایجاد کاربر سرویس
# =============================================================================

print_status "ایجاد کاربر سرویس..."

if ! id "$SERVICE_USER" &>/dev/null; then
    useradd -r -s /bin/bash -d "$PROJECT_DIR" -m "$SERVICE_USER"
    print_success "کاربر $SERVICE_USER ایجاد شد"
else
    print_warning "کاربر $SERVICE_USER موجود است"
fi

# =============================================================================
# تنظیمات SQLite (برای تست)
# =============================================================================

print_status "تنظیمات SQLite..."

# SQLite doesn't need additional setup
print_success "SQLite آماده است (فایل db.sqlite3 خودکار ایجاد می‌شود)"

# =============================================================================
# تنظیمات Redis (اختیاری)
# =============================================================================

print_status "تنظیمات Redis..."

# Configure Redis
sed -i 's/^# maxmemory <bytes>/maxmemory 256mb/' /etc/redis/redis.conf
sed -i 's/^# maxmemory-policy noeviction/maxmemory-policy allkeys-lru/' /etc/redis/redis.conf

systemctl restart redis-server
systemctl enable redis-server

print_success "Redis تنظیم شد (اختیاری - برای cache)"

# =============================================================================
# کپی کردن پروژه
# =============================================================================

print_status "کپی کردن پروژه..."

# Create project directory
mkdir -p "$PROJECT_DIR"
chown "$SERVICE_USER:$SERVICE_USER" "$PROJECT_DIR"

# Copy project files (assuming current directory is the project)
cp -r . "$PROJECT_DIR/"
chown -R "$SERVICE_USER:$SERVICE_USER" "$PROJECT_DIR"

print_success "پروژه کپی شد"

# =============================================================================
# تنظیمات Virtual Environment
# =============================================================================

print_status "تنظیمات Virtual Environment..."

# Switch to service user
sudo -u "$SERVICE_USER" bash << EOF
cd "$PROJECT_DIR"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install additional production packages
pip install gunicorn psycopg2-binary redis
EOF

print_success "Virtual Environment تنظیم شد"

# =============================================================================
# تنظیمات Environment
# =============================================================================

print_status "تنظیمات Environment..."

# Create production .env file
sudo -u "$SERVICE_USER" tee "$PROJECT_DIR/.env" > /dev/null << EOF
# Django Settings
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN,87.248.150.86

# Microservice Configuration
AUTH_SERVICE_DOMAIN=$DOMAIN
ALLOWED_CLIENT_DOMAINS=app1.avinoo.ir,app2.avinoo.ir

# SSO Configuration
SSO_REDIRECT_URL=https://{domain}/callback
SSO_LOGIN_URL=https://{domain}/login
SSO_LOGOUT_URL=https://{domain}/logout

# Database Configuration (SQLite for testing)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=sso_service_db
# DB_USER=sso_user
# DB_PASSWORD=sso_secure_password_123
# DB_HOST=localhost
# DB_PORT=5432

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
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS=DENY

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=WARNING

# Email Configuration (configure as needed)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EOF

print_success "فایل .env ایجاد شد"

# =============================================================================
# Migration و Setup
# =============================================================================

print_status "اجرای Migration..."

sudo -u "$SERVICE_USER" bash << EOF
cd "$PROJECT_DIR"
source venv/bin/activate

# Create logs directory
mkdir -p logs

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@$DOMAIN', 'admin123456')" | python manage.py shell

# Generate RSA keys
python manage.py shell << 'PYTHON_EOF'
from sso.utils import generate_rsa_keys
try:
    generate_rsa_keys()
    print('کلیدهای RSA ایجاد شدند')
except Exception as e:
    print(f'خطا در ایجاد کلیدهای RSA: {e}')
PYTHON_EOF
EOF

print_success "Migration ها اجرا شدند"

# =============================================================================
# تنظیمات Gunicorn
# =============================================================================

print_status "تنظیمات Gunicorn..."

# Create Gunicorn configuration
sudo -u "$SERVICE_USER" tee "$PROJECT_DIR/gunicorn.conf.py" > /dev/null << EOF
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
user = "$SERVICE_USER"
group = "$SERVICE_USER"
tmp_upload_dir = None
forwarded_allow_ips = "*"
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
}
EOF

print_success "تنظیمات Gunicorn ایجاد شد"

# =============================================================================
# تنظیمات Systemd Service
# =============================================================================

print_status "تنظیمات Systemd Service..."

tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null << EOF
[Unit]
Description=SSO Authentication Service
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --config gunicorn.conf.py auth_service.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal
SyslogIdentifier=$SERVICE_NAME

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
systemctl daemon-reload
systemctl enable $SERVICE_NAME

print_success "Systemd Service ایجاد شد"

# =============================================================================
# تنظیمات Nginx
# =============================================================================

print_status "تنظیمات Nginx..."

# Create Nginx configuration
tee /etc/nginx/sites-available/$SERVICE_NAME > /dev/null << EOF
# Rate limiting
limit_req_zone \$binary_remote_addr zone=login:10m rate=5r/m;
limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;

# Upstream
upstream sso_backend {
    server 127.0.0.1:8000;
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    return 301 https://\$server_name\$request_uri;
}

# HTTPS server
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
    ssl_stapling on;
    ssl_stapling_verify on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';" always;
    
    # Static files
    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    location /media/ {
        alias $PROJECT_DIR/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # API endpoints with rate limiting
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://sso_backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-Host \$host;
        proxy_set_header X-Forwarded-Port \$server_port;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # Login page with rate limiting
    location /login/ {
        limit_req zone=login burst=5 nodelay;
        proxy_pass http://sso_backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-Host \$host;
        proxy_set_header X-Forwarded-Port \$server_port;
    }
    
    # Other locations
    location / {
        proxy_pass http://sso_backend;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-Host \$host;
        proxy_set_header X-Forwarded-Port \$server_port;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/

# Test nginx configuration
nginx -t

if [ $? -eq 0 ]; then
    systemctl reload nginx
    print_success "تنظیمات Nginx ایجاد شد"
else
    print_error "خطا در تنظیمات Nginx!"
    exit 1
fi

# =============================================================================
# دریافت گواهی SSL
# =============================================================================

print_status "دریافت گواهی SSL از Let's Encrypt..."

# Get SSL certificate
certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

print_success "گواهی SSL دریافت شد"

# =============================================================================
# شروع سرویس‌ها
# =============================================================================

print_status "شروع سرویس‌ها..."

# Start services
systemctl start $SERVICE_NAME
systemctl start nginx
systemctl start redis-server

# Enable services
systemctl enable $SERVICE_NAME
systemctl enable nginx
systemctl enable redis-server

print_success "سرویس‌ها شروع شدند"

# =============================================================================
# تنظیمات Firewall
# =============================================================================

print_status "تنظیمات Firewall..."

# Configure UFW
ufw --force enable
ufw allow ssh
ufw allow 'Nginx Full'
ufw allow 5432/tcp  # PostgreSQL (if needed for external access)

print_success "Firewall تنظیم شد"

# =============================================================================
# تنظیمات Logrotate
# =============================================================================

print_status "تنظیمات Logrotate..."

# Create logrotate configuration
tee /etc/logrotate.d/$SERVICE_NAME > /dev/null << EOF
$PROJECT_DIR/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $SERVICE_USER $SERVICE_USER
    postrotate
        systemctl reload $SERVICE_NAME
    endscript
}
EOF

print_success "Logrotate تنظیم شد"

# =============================================================================
# خلاصه Deploy
# =============================================================================

echo ""
echo "=========================================="
echo "✅ Deploy سیستم SSO تکمیل شد!"
echo "=========================================="
echo ""
echo "🌐 دامنه: https://$DOMAIN"
echo "📁 مسیر پروژه: $PROJECT_DIR"
echo "👤 کاربر سرویس: $SERVICE_USER"
echo "🗄️  دیتابیس: SQLite (برای تست)"
echo "📊 Cache: Redis"
echo "🔒 SSL: Let's Encrypt"
echo ""
echo "🌐 آدرس‌های مفید:"
echo "   - صفحه تست: https://$DOMAIN/test/"
echo "   - صفحه ورود: https://$DOMAIN/login/"
echo "   - Admin Panel: https://$DOMAIN/admin/"
echo ""
echo "🔧 مدیریت سرویس:"
echo "   systemctl start $SERVICE_NAME"
echo "   systemctl stop $SERVICE_NAME"
echo "   systemctl restart $SERVICE_NAME"
echo "   systemctl status $SERVICE_NAME"
echo ""
echo "📝 لاگ‌ها:"
echo "   journalctl -u $SERVICE_NAME -f"
echo "   tail -f $PROJECT_DIR/logs/django.log"
echo ""
echo "🔐 اطلاعات ورود:"
echo "   نام کاربری: admin"
echo "   رمز عبور: admin123456"
echo "   ایمیل: admin@$DOMAIN"
echo ""
echo "⚠️  نکات امنیتی:"
echo "   - رمز عبور admin را تغییر دهید"
echo "   - تنظیمات ایمیل را پیکربندی کنید"
echo "   - فایروال را بررسی کنید"
echo "   - بک‌آپ منظم تنظیم کنید"
echo ""
echo "=========================================="
print_success "Deploy کامل شد! 🎉"
echo "=========================================="
