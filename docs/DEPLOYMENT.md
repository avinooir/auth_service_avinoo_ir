# 🚀 Deployment Guide - Auth Service

## Overview

This guide provides comprehensive instructions for deploying the Auth Service in different environments, from development to production.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.9 or higher
- **Database**: PostgreSQL 12+ or MySQL 8.0+
- **Memory**: Minimum 512MB RAM
- **Storage**: Minimum 1GB free space
- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows Server

### Software Dependencies
- Python 3.9+
- pip
- PostgreSQL or MySQL
- Nginx (for production)
- Gunicorn (for production)

## 🏗️ Environment Setup

### 1. Development Environment

#### Local Development
```bash
# Clone the repository
git clone <repository-url>
cd auth_service

# Run setup script
./setup.sh

# Start development server
python manage.py runserver
```

#### Docker Development
```dockerfile
# Dockerfile.dev
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: auth_service_db
      POSTGRES_USER: auth_user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=True
      - DB_HOST=db
      - DB_NAME=auth_service_db
      - DB_USER=auth_user
      - DB_PASSWORD=password
    depends_on:
      - db

volumes:
  postgres_data:
```

### 2. Staging Environment

#### Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.9 python3.9-venv python3-pip postgresql postgresql-contrib nginx -y

# Create application user
sudo useradd -m -s /bin/bash authservice
sudo usermod -aG sudo authservice
```

#### Application Deployment
```bash
# Switch to application user
sudo su - authservice

# Clone repository
git clone <repository-url> /home/authservice/auth_service
cd /home/authservice/auth_service

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with staging configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Create initial data
python scripts/create_initial_data.py
```

#### Gunicorn Configuration
```python
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

#### Systemd Service
```ini
# /etc/systemd/system/auth-service.service
[Unit]
Description=Auth Service
After=network.target

[Service]
Type=notify
User=authservice
Group=authservice
WorkingDirectory=/home/authservice/auth_service
Environment=PATH=/home/authservice/auth_service/venv/bin
ExecStart=/home/authservice/auth_service/venv/bin/gunicorn --config gunicorn.conf.py auth_service.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Nginx Configuration
```nginx
# /etc/nginx/sites-available/auth-service
server {
    listen 80;
    server_name staging-auth.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/authservice/auth_service/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/authservice/auth_service/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
}
```

### 3. Production Environment

#### High Availability Setup

##### Load Balancer Configuration (HAProxy)
```haproxy
# /etc/haproxy/haproxy.cfg
global
    daemon
    maxconn 4096

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend auth_service_frontend
    bind *:80
    bind *:443 ssl crt /etc/ssl/certs/auth-service.pem
    redirect scheme https if !{ ssl_fc }
    
    default_backend auth_service_backend

backend auth_service_backend
    balance roundrobin
    option httpchk GET /health/
    
    server auth1 10.0.1.10:8000 check
    server auth2 10.0.1.11:8000 check
    server auth3 10.0.1.12:8000 check
```

##### Database Configuration (PostgreSQL)
```postgresql
# /etc/postgresql/13/main/postgresql.conf
listen_addresses = '*'
port = 5432
max_connections = 200
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB
```

##### Redis Configuration (for caching)
```redis
# /etc/redis/redis.conf
bind 127.0.0.1
port 6379
timeout 0
tcp-keepalive 300
maxmemory 256mb
maxmemory-policy allkeys-lru
```

#### Production Environment Variables
```env
# Production .env
SECRET_KEY=your-super-secret-production-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=auth_service_prod
DB_USER=auth_service_user
DB_PASSWORD=your-super-secure-db-password
DB_HOST=your-db-host
DB_PORT=5432

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME=15
JWT_REFRESH_TOKEN_LIFETIME=7

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Logging
LOG_LEVEL=WARNING

# Security
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS=DENY
```

## 🔧 Configuration Management

### Environment-Specific Settings

#### Development Settings
```python
# settings/dev.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Use SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Disable caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
```

#### Production Settings
```python
# settings/prod.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Database connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 600

# Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Logging
LOGGING['handlers']['file']['filename'] = '/var/log/auth-service/django.log'
LOGGING['handlers']['file']['level'] = 'WARNING'
```

## 📊 Monitoring and Logging

### Application Monitoring

#### Health Check Endpoint
```python
# apps/core/views.py
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache

def health_check(request):
    """Health check endpoint for load balancer."""
    try:
        # Check database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Check cache
        cache.set('health_check', 'ok', 10)
        cache.get('health_check')
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'ok',
            'cache': 'ok'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)
```

#### Logging Configuration
```python
# settings/logging.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'json': {
            'format': '{"level": "%(levelname)s", "time": "%(asctime)s", "module": "%(module)s", "message": "%(message)s"}',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/auth-service/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/auth-service/error.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'json',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps': {
            'handlers': ['file', 'error_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### System Monitoring

#### Prometheus Metrics
```python
# apps/core/middleware.py
import time
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache

class PrometheusMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Increment request counter
            cache.set(f'requests_total_{response.status_code}', 
                     cache.get(f'requests_total_{response.status_code}', 0) + 1, 
                     timeout=None)
            
            # Update response time histogram
            cache.set(f'response_time_{response.status_code}', 
                     cache.get(f'response_time_{response.status_code}', 0) + duration, 
                     timeout=None)
        
        return response
```

## 🔒 Security Considerations

### SSL/TLS Configuration
```nginx
# SSL configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

### Firewall Configuration
```bash
# UFW firewall rules
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw deny 8000/tcp   # Block direct access to Gunicorn
sudo ufw enable
```

### Database Security
```sql
-- Create dedicated database user
CREATE USER auth_service_user WITH PASSWORD 'secure_password';
CREATE DATABASE auth_service_prod OWNER auth_service_user;
GRANT ALL PRIVILEGES ON DATABASE auth_service_prod TO auth_service_user;

-- Revoke unnecessary privileges
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
```

## 🚀 Deployment Scripts

### Automated Deployment Script
```bash
#!/bin/bash
# deploy.sh

set -e

echo "🚀 Starting deployment..."

# Pull latest code
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart auth-service
sudo systemctl reload nginx

# Run tests
python scripts/test_api.py

echo "✅ Deployment completed successfully!"
```

### Backup Script
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/auth-service"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
pg_dump -h localhost -U auth_service_user auth_service_prod > $BACKUP_DIR/db_$DATE.sql

# Media files backup
tar -czf $BACKUP_DIR/media_$DATE.tar.gz media/

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "✅ Backup completed: $DATE"
```

## 📈 Performance Optimization

### Database Optimization
```python
# Database connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'auth_service_prod',
        'USER': 'auth_service_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'MAX_CONNS': 20,
            'MIN_CONNS': 5,
        }
    }
}
```

### Caching Strategy
```python
# Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            }
        }
    }
}

# Session caching
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          python manage.py test
          python scripts/test_api.py

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /home/authservice/auth_service
            ./deploy.sh
```

## 📞 Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check database status
sudo systemctl status postgresql

# Check database logs
sudo tail -f /var/log/postgresql/postgresql-13-main.log

# Test database connection
psql -h localhost -U auth_service_user -d auth_service_prod -c "SELECT 1;"
```

#### Application Issues
```bash
# Check application logs
sudo journalctl -u auth-service -f

# Check application status
sudo systemctl status auth-service

# Restart application
sudo systemctl restart auth-service
```

#### Nginx Issues
```bash
# Check Nginx configuration
sudo nginx -t

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log

# Reload Nginx
sudo systemctl reload nginx
```

### Performance Monitoring
```bash
# Monitor system resources
htop
iostat -x 1
netstat -tulpn

# Monitor application performance
curl -s http://localhost:8000/health/ | jq
```

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [PostgreSQL Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [Redis Configuration](https://redis.io/topics/config)

---

**Note**: This deployment guide provides a comprehensive overview. Always test deployments in a staging environment before applying to production.
