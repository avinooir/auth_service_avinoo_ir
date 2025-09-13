# 🔧 راهنمای تنظیمات سیستم SSO

## 📋 فهرست مطالب
- [تنظیمات Environment](#تنظیمات-environment)
- [تنظیمات Database](#تنظیمات-database)
- [تنظیمات JWT](#تنظیمات-jwt)
- [تنظیمات CORS](#تنظیمات-cors)
- [تنظیمات Security](#تنظیمات-security)
- [تنظیمات Production](#تنظیمات-production)

## 🌍 تنظیمات Environment

### فایل .env
```bash
# کپی کردن فایل نمونه
cp env.example .env
```

### تنظیمات اصلی
```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True  # False برای production
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Microservice Configuration
AUTH_SERVICE_DOMAIN=127.0.0.1:8000  # برای development
AUTH_SERVICE_DOMAIN=auth.avinoo.ir  # برای production
ALLOWED_CLIENT_DOMAINS=app1.avinoo.ir,app2.avinoo.ir
```

### تنظیمات SSO
```bash
# SSO Configuration
SSO_REDIRECT_URL=http://{domain}/callback  # برای development
SSO_REDIRECT_URL=https://{domain}/callback  # برای production
SSO_LOGIN_URL=http://{domain}/login
SSO_LOGOUT_URL=http://{domain}/logout
```

## 🗄️ تنظیمات Database

### SQLite (Development)
```bash
# در .env
# Database Configuration (SQLite for development)
# تنظیمات پیش‌فرض - نیازی به تغییر نیست
```

### PostgreSQL (Production)
```bash
# در .env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=auth_service_db
DB_USER=auth_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

### MySQL (Production)
```bash
# در .env
DB_ENGINE=django.db.backends.mysql
DB_NAME=auth_service_db
DB_USER=auth_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=3306
```

## 🔐 تنظیمات JWT

### تنظیمات پیش‌فرض
```bash
# در .env
JWT_ACCESS_TOKEN_LIFETIME=60  # دقیقه
JWT_REFRESH_TOKEN_LIFETIME=7  # روز
JWT_PRIVATE_KEY_PATH=keys/private_key.pem
JWT_PUBLIC_KEY_PATH=keys/public_key.pem
```

### تولید کلیدهای RSA
```bash
# تولید کلیدهای RSA
python manage.py shell -c "
from sso.utils import generate_rsa_keys
generate_rsa_keys()
"
```

### تنظیمات JWT در settings.py
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ALGORITHM': 'HS256',  # یا 'RS256' برای RSA
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': SECRET_KEY,
    'AUDIENCE': AUTH_SERVICE_DOMAIN,
    'ISSUER': AUTH_SERVICE_DOMAIN,
}
```

## 🌐 تنظیمات CORS

### تنظیمات Development
```bash
# در .env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://127.0.0.1:8000
```

### تنظیمات Production
```bash
# در .env
CORS_ALLOWED_ORIGINS=https://app1.avinoo.ir,https://app2.avinoo.ir,https://yourdomain.com
```

## 🔒 تنظیمات Security

### تنظیمات Development
```bash
# در .env
DEBUG=True
SECURE_SSL_REDIRECT=False
```

### تنظیمات Production
```bash
# در .env
DEBUG=False
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS=DENY
```

## 🚀 تنظیمات Production

### تنظیمات کامل Production
```bash
# در .env
# Django Settings
SECRET_KEY=your-very-secure-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Microservice Configuration
AUTH_SERVICE_DOMAIN=auth.yourdomain.com
ALLOWED_CLIENT_DOMAINS=app1.yourdomain.com,app2.yourdomain.com

# SSO Configuration
SSO_REDIRECT_URL=https://{domain}/callback
SSO_LOGIN_URL=https://{domain}/login
SSO_LOGOUT_URL=https://{domain}/logout

# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=auth_service_db
DB_USER=auth_user
DB_PASSWORD=your-secure-db-password
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=7
JWT_PRIVATE_KEY_PATH=keys/private_key.pem
JWT_PUBLIC_KEY_PATH=keys/public_key.pem

# CORS Settings
CORS_ALLOWED_ORIGINS=https://app1.yourdomain.com,https://app2.yourdomain.com

# Security Settings
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS=DENY

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=WARNING
```

## 📧 تنظیمات Email

### Gmail SMTP
```bash
# در .env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### SendGrid
```bash
# در .env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

## 📊 تنظیمات Logging

### تنظیمات Development
```bash
# در .env
LOG_LEVEL=INFO
```

### تنظیمات Production
```bash
# در .env
LOG_LEVEL=WARNING
```

### تنظیمات Logging در settings.py
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
    },
    'loggers': {
        'sso': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🔍 تنظیمات Debugging

### فعال‌سازی Debug Mode
```bash
# در .env
DEBUG=True
LOG_LEVEL=DEBUG
```

### بررسی لاگ‌ها
```bash
# Windows
Get-Content logs/django.log -Tail 20

# Linux/Mac
tail -f logs/django.log
```

## 🐳 تنظیمات Docker

### Dockerfile
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### docker-compose.yml
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - AUTH_SERVICE_DOMAIN=auth.yourdomain.com
    volumes:
      - .:/app
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=auth_service_db
      - POSTGRES_USER=auth_user
      - POSTGRES_PASSWORD=your-db-password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

## 📝 نکات مهم

### 1. امنیت
- همیشه `SECRET_KEY` را تغییر دهید
- در production `DEBUG=False` تنظیم کنید
- از HTTPS استفاده کنید
- کلیدهای RSA را امن نگه دارید

### 2. Performance
- از Redis برای caching استفاده کنید
- Database connection pooling فعال کنید
- Static files را با CDN سرو کنید

### 3. Monitoring
- لاگ‌ها را مانیتور کنید
- از Sentry برای error tracking استفاده کنید
- Health check endpoints اضافه کنید

---

**نسخه**: 1.0  
**تاریخ**: 2025-09-08  
**نویسنده**: تیم توسعه SSO
