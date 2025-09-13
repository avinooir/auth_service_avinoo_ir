# راهنمای استقرار در سرور روسی

## 📋 فایل‌های مورد نیاز

برای حل مشکل مایگریشن GUID در سرور روسی، این فایل‌ها را کپی کنید:

### فایل‌های اصلی
- `fix_guid_migration_ru.py` - اسکریپت اصلی Python
- `run_guid_fix.sh` - اسکریپت Bash برای Linux
- `GUID_MIGRATION_FIX_README.md` - راهنمای کامل

## 🚀 مراحل استقرار

### 1. کپی فایل‌ها به سرور

```bash
# کپی فایل‌ها به سرور روسی
scp fix_guid_migration_ru.py user@russian-server:/path/to/auth_service/
scp run_guid_fix.sh user@russian-server:/path/to/auth_service/
scp GUID_MIGRATION_FIX_README.md user@russian-server:/path/to/auth_service/
```

### 2. ورود به سرور

```bash
# ورود به سرور روسی
ssh user@russian-server

# رفتن به پوشه پروژه
cd /path/to/auth_service/
```

### 3. تنظیم مجوزها

```bash
# قابل اجرا کردن اسکریپت Bash
chmod +x run_guid_fix.sh

# بررسی مجوزهای فایل‌ها
ls -la fix_guid_migration_ru.py
ls -la run_guid_fix.sh
```

### 4. اجرای اسکریپت

```bash
# اجرای اسکریپت
./run_guid_fix.sh
```

## 🔍 بررسی نتایج

### بررسی لاگ
```bash
# نمایش لاگ
cat guid_migration_fix.log

# نمایش آخرین خطوط لاگ
tail -f guid_migration_fix.log
```

### بررسی backup
```bash
# لیست فایل‌های backup
ls -la *.backup_*

# بررسی اندازه backup
du -h *.backup_*
```

### تست Django
```bash
# بررسی وضعیت مایگریشن
python manage.py showmigrations users

# تست کاربران
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
for user in User.objects.all():
    print(f'{user.username}: {user.guid}')
"
```

## 🛠️ عیب‌یابی

### مشکلات رایج

#### 1. خطای Python
```bash
# بررسی نسخه Python
python3 --version

# نصب Python اگر نیاز باشد
sudo apt update
sudo apt install python3 python3-pip
```

#### 2. خطای Django
```bash
# نصب Django
pip3 install django

# یا استفاده از virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 3. خطای دسترسی
```bash
# بررسی مجوزهای فایل‌ها
ls -la db.sqlite3
chmod 644 db.sqlite3

# بررسی مجوزهای پوشه
ls -la
chmod 755 .
```

## 📊 خروجی‌های مورد انتظار

### لاگ موفق
```
INFO - Django setup completed successfully
INFO - Database connection successful
INFO - Total users in database: X
INFO - GUID column exists: True/False
INFO - Database backed up to: /path/to/backup
INFO - Starting GUID migration fix...
INFO - Generated GUIDs for X users
INFO - SUCCESS: All users have GUIDs!
INFO - SUCCESS: JWT Token contains GUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
INFO - SUCCESS: GUID Migration Fix Completed Successfully!
```

### فایل‌های ایجاد شده
- `guid_migration_fix.log` - فایل لاگ
- `db.sqlite3.backup_YYYYMMDD_HHMMSS` - backup دیتابیس

## ✅ تأیید موفقیت

پس از اجرای موفق اسکریپت:

1. **تمام کاربران GUID دارند**
2. **JWT Token شامل GUID است**
3. **فایل لاگ بدون خطا است**
4. **Backup دیتابیس ایجاد شده است**

## 📞 پشتیبانی

### در صورت بروز مشکل

1. **بررسی لاگ:** فایل `guid_migration_fix.log` را بررسی کنید
2. **بررسی backup:** از فایل backup استفاده کنید
3. **تست دستی:** مراحل را به صورت دستی انجام دهید

### دستورات مفید

```bash
# بررسی وضعیت سیستم
python3 --version
pip3 list | grep django

# بررسی دیتابیس
sqlite3 db.sqlite3 ".schema users"

# تست Django
python3 manage.py check
python3 manage.py showmigrations
```

---

**تاریخ:** 13 ژانویه 2025  
**وضعیت:** آماده برای استقرار ✅
