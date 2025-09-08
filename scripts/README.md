# 🚀 اسکریپت‌های نصب و Deploy سیستم SSO

## 📋 فهرست مطالب
- [اسکریپت‌های موجود](#اسکریپت‌های-موجود)
- [نصب روی Linux](#نصب-روی-linux)
- [نصب روی Windows](#نصب-روی-windows)
- [Deploy Production](#deploy-production)
- [شروع سریع](#شروع-سریع)
- [نکات مهم](#نکات-مهم)

## 📁 اسکریپت‌های موجود

| فایل | توضیح | سیستم عامل | دیتابیس |
|------|-------|------------|---------|
| `install_linux.sh` | نصب کامل روی Linux | Linux | SQLite/PostgreSQL |
| `install_windows.ps1` | نصب کامل روی Windows | Windows | SQLite |
| `deploy_production.sh` | Deploy Production برای auth.avinoo.ir | Linux | SQLite |
| `deploy_test.sh` | Deploy تست برای auth.avinoo.ir | Linux | SQLite |
| `quick_start.sh` | شروع سریع | Linux | SQLite |
| `quick_start.ps1` | شروع سریع | Windows | SQLite |

## 🐧 نصب روی Linux

### نصب کامل
```bash
# دانلود پروژه
git clone <repository-url>
cd auth_service

# اجرای اسکریپت نصب
chmod +x scripts/install_linux.sh
./scripts/install_linux.sh
```

### ویژگی‌های اسکریپت نصب:
- ✅ نصب Python 3.9+
- ✅ ایجاد Virtual Environment
- ✅ نصب Dependencies
- ✅ تنظیمات Environment
- ✅ Migration Database
- ✅ ایجاد Superuser
- ✅ تولید کلیدهای RSA
- ✅ تنظیمات Systemd Service
- ✅ تنظیمات Nginx
- ✅ دریافت گواهی SSL (Let's Encrypt)
- ✅ تنظیمات امنیتی

### شروع سریع
```bash
chmod +x scripts/quick_start.sh
./scripts/quick_start.sh
```

## 🪟 نصب روی Windows

### نصب کامل
```powershell
# دانلود پروژه
git clone <repository-url>
cd auth_service

# اجرای اسکریپت نصب
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\scripts\install_windows.ps1
```

### ویژگی‌های اسکریپت نصب:
- ✅ بررسی Python
- ✅ ایجاد Virtual Environment
- ✅ نصب Dependencies
- ✅ تنظیمات Environment
- ✅ Migration Database
- ✅ ایجاد Superuser
- ✅ تولید کلیدهای RSA
- ✅ تنظیمات Windows Service (NSSM)
- ✅ تنظیمات امنیتی

### شروع سریع
```powershell
.\scripts\quick_start.ps1
```

## 🚀 Deploy Production

### Deploy برای auth.avinoo.ir (تست با SQLite)
```bash
# اجرای اسکریپت Deploy تست (نیاز به root)
sudo chmod +x scripts/deploy_test.sh
sudo ./scripts/deploy_test.sh
```

### Deploy برای auth.avinoo.ir (Production با PostgreSQL)
```bash
# اجرای اسکریپت Deploy Production (نیاز به root)
sudo chmod +x scripts/deploy_production.sh
sudo ./scripts/deploy_production.sh
```

### ویژگی‌های Deploy تست (SQLite):
- ✅ نصب Dependencies سیستم
- ✅ ایجاد کاربر سرویس
- ✅ کپی پروژه
- ✅ تنظیمات Virtual Environment
- ✅ تنظیمات Environment Production
- ✅ Migration Database (SQLite)
- ✅ تنظیمات Gunicorn
- ✅ تنظیمات Systemd Service
- ✅ تنظیمات Nginx با SSL
- ✅ دریافت گواهی Let's Encrypt
- ✅ تنظیمات Firewall
- ✅ تنظیمات Logrotate
- ✅ Rate Limiting
- ✅ Security Headers

### ویژگی‌های Deploy Production (PostgreSQL):
- ✅ نصب Dependencies سیستم
- ✅ تنظیمات PostgreSQL
- ✅ تنظیمات Redis
- ✅ ایجاد کاربر سرویس
- ✅ کپی پروژه
- ✅ تنظیمات Virtual Environment
- ✅ تنظیمات Environment Production
- ✅ Migration Database (PostgreSQL)
- ✅ تنظیمات Gunicorn
- ✅ تنظیمات Systemd Service
- ✅ تنظیمات Nginx با SSL
- ✅ دریافت گواهی Let's Encrypt
- ✅ تنظیمات Firewall
- ✅ تنظیمات Logrotate
- ✅ Rate Limiting
- ✅ Security Headers

## ⚡ شروع سریع

### Linux
```bash
# شروع سریع
chmod +x scripts/quick_start.sh
./scripts/quick_start.sh

# شروع سرور
source venv/bin/activate
python manage.py runserver
```

### Windows
```powershell
# شروع سریع
.\scripts\quick_start.ps1

# شروع سرور
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

## 🔧 مدیریت سرویس

### Linux (Systemd)
```bash
# شروع سرویس
sudo systemctl start sso-service

# توقف سرویس
sudo systemctl stop sso-service

# راه‌اندازی مجدد
sudo systemctl restart sso-service

# وضعیت سرویس
sudo systemctl status sso-service

# فعال‌سازی خودکار
sudo systemctl enable sso-service

# غیرفعال‌سازی
sudo systemctl disable sso-service
```

### Windows (NSSM)
```powershell
# شروع سرویس
Start-Service SSO-Service

# توقف سرویس
Stop-Service SSO-Service

# راه‌اندازی مجدد
Restart-Service SSO-Service

# وضعیت سرویس
Get-Service SSO-Service
```

## 📝 لاگ‌ها

### Linux
```bash
# لاگ‌های سرویس
journalctl -u sso-service -f

# لاگ‌های Django
tail -f logs/django.log

# لاگ‌های Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Windows
```powershell
# لاگ‌های Django
Get-Content logs\django.log -Tail 20 -Wait

# لاگ‌های Event Viewer
Get-EventLog -LogName Application -Source "SSO-Service" -Newest 10
```

## 🔐 تنظیمات امنیتی

### Production Checklist
- [ ] تغییر رمز عبور admin
- [ ] تنظیمات ایمیل
- [ ] بررسی فایروال
- [ ] تنظیمات بک‌آپ
- [ ] مانیتورینگ
- [ ] SSL Certificate
- [ ] Security Headers
- [ ] Rate Limiting

### تنظیمات فایروال
```bash
# UFW (Ubuntu)
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'

# iptables
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

## 🌐 تنظیمات DNS

### رکوردهای DNS مورد نیاز
```
A     auth.avinoo.ir     -> IP_SERVER
A     www.auth.avinoo.ir -> IP_SERVER
CNAME app1.avinoo.ir     -> auth.avinoo.ir
CNAME app2.avinoo.ir     -> auth.avinoo.ir
```

## 📊 مانیتورینگ

### Health Check
```bash
# بررسی وضعیت سرویس
curl -f https://auth.avinoo.ir/api/health/ || echo "Service is down"

# بررسی SSL
openssl s_client -connect auth.avinoo.ir:443 -servername auth.avinoo.ir
```

### Performance Monitoring
```bash
# بررسی استفاده از CPU
top -p $(pgrep -f "gunicorn")

# بررسی استفاده از حافظه
free -h

# بررسی فضای دیسک
df -h

# بررسی اتصالات شبکه
netstat -tulpn | grep :8000
```

## 🔄 بک‌آپ

### بک‌آپ دیتابیس
```bash
# PostgreSQL
pg_dump -h localhost -U sso_user sso_service_db > backup_$(date +%Y%m%d_%H%M%S).sql

# SQLite
cp db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3
```

### بک‌آپ فایل‌ها
```bash
# بک‌آپ کامل
tar -czf sso_backup_$(date +%Y%m%d_%H%M%S).tar.gz /opt/sso-service

# بک‌آپ تنظیمات
cp /opt/sso-service/.env backup_env_$(date +%Y%m%d_%H%M%S)
```

## 🚨 عیب‌یابی

### مشکلات رایج

#### سرویس شروع نمی‌شود
```bash
# بررسی لاگ‌ها
journalctl -u sso-service -f

# بررسی تنظیمات
systemctl status sso-service

# تست دستی
cd /opt/sso-service
source venv/bin/activate
python manage.py runserver
```

#### مشکل SSL
```bash
# بررسی گواهی
certbot certificates

# تمدید گواهی
certbot renew

# تست SSL
openssl s_client -connect auth.avinoo.ir:443
```

#### مشکل دیتابیس
```bash
# بررسی اتصال
sudo -u postgres psql -c "SELECT 1;"

# بررسی کاربر
sudo -u postgres psql -c "SELECT * FROM pg_user WHERE usename='sso_user';"

# بررسی دیتابیس
sudo -u postgres psql -c "SELECT datname FROM pg_database WHERE datname='sso_service_db';"
```

## 📞 پشتیبانی

برای مشکلات و سوالات:
1. بررسی لاگ‌ها
2. بررسی مستندات
3. تست دستی
4. تماس با تیم توسعه

---

**نسخه**: 1.0  
**تاریخ**: 2025-09-08  
**نویسنده**: تیم توسعه SSO
