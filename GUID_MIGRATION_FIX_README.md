# راهنمای حل مشکل مایگریشن GUID

## 📋 توضیحات

این مجموعه اسکریپت‌ها برای حل مشکل `UNIQUE constraint failed: new__users.guid` در سرور روسی شما طراحی شده است.

## 🚀 نحوه استفاده

### روش 1: استفاده از PowerShell (Windows)

```powershell
# اجرای اسکریپت PowerShell
.\run_guid_fix.ps1
```

### روش 2: استفاده از Bash (Linux/Mac)

```bash
# اجرای اسکریپت Bash
./run_guid_fix.sh
```

### روش 3: اجرای مستقیم Python

```bash
# اجرای مستقیم اسکریپت Python
python fix_guid_migration_ru.py
```

## 📁 فایل‌های موجود

- **`fix_guid_migration_ru.py`** - اسکریپت اصلی Python
- **`run_guid_fix.ps1`** - اسکریپت PowerShell برای Windows
- **`run_guid_fix.sh`** - اسکریپت Bash برای Linux/Mac
- **`GUID_MIGRATION_FIX_README.md`** - این فایل راهنما

## 🔧 ویژگی‌های اسکریپت

### ✅ قابلیت‌های اصلی

1. **بررسی خودکار:** بررسی وضعیت دیتابیس و کاربران
2. **پشتیبان‌گیری:** ایجاد backup از دیتابیس قبل از تغییرات
3. **حل مشکل:** اضافه کردن فیلد GUID و تولید GUID برای کاربران موجود
4. **تست جامع:** بررسی JWT Token و API Response
5. **لاگ‌گیری:** ثبت تمام عملیات در فایل لاگ
6. **علامت‌گذاری مایگریشن:** علامت‌گذاری مایگریشن به عنوان اجرا شده

### 📊 خروجی‌ها

- **فایل لاگ:** `guid_migration_fix.log`
- **Backup دیتابیس:** `db.sqlite3.backup_YYYYMMDD_HHMMSS`
- **گزارش کنسول:** نمایش وضعیت در زمان واقعی

## 🛠️ پیش‌نیازها

### نرم‌افزارهای مورد نیاز

- Python 3.7+
- Django 3.0+
- دسترسی به دیتابیس SQLite

### وابستگی‌های Python

```bash
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
```

## 📋 مراحل اجرا

### 1. آماده‌سازی

```bash
# کپی کردن فایل‌ها به سرور
scp fix_guid_migration_ru.py user@server:/path/to/project/
scp run_guid_fix.sh user@server:/path/to/project/
```

### 2. اجرا

```bash
# ورود به سرور
ssh user@server

# رفتن به پوشه پروژه
cd /path/to/project/

# اجرای اسکریپت
./run_guid_fix.sh
```

### 3. بررسی نتایج

```bash
# بررسی لاگ
cat guid_migration_fix.log

# بررسی backup
ls -la *.backup_*

# تست Django
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> for user in User.objects.all():
...     print(f"{user.username}: {user.guid}")
```

## 🔍 عیب‌یابی

### مشکلات رایج

#### 1. خطای Python not found
```bash
# نصب Python
sudo apt update
sudo apt install python3 python3-pip
```

#### 2. خطای Django setup
```bash
# نصب Django
pip3 install django
```

#### 3. خطای دسترسی به دیتابیس
```bash
# بررسی مجوزهای فایل
ls -la db.sqlite3
chmod 644 db.sqlite3
```

#### 4. خطای virtual environment
```bash
# ایجاد virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 📞 پشتیبانی

### در صورت بروز مشکل

1. **بررسی لاگ:** فایل `guid_migration_fix.log` را بررسی کنید
2. **بررسی backup:** از فایل backup استفاده کنید
3. **تست دستی:** مراحل را به صورت دستی انجام دهید

### دستورات مفید

```bash
# بررسی وضعیت مایگریشن
python manage.py showmigrations users

# اجرای مایگریشن دستی
python manage.py migrate users --fake

# بررسی کاربران
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print([(u.username, u.guid) for u in User.objects.all()])"
```

## 🎯 نتیجه نهایی

پس از اجرای موفق اسکریپت:

- ✅ تمام کاربران GUID یکتا دارند
- ✅ GUID در JWT Token موجود است
- ✅ GUID در API responses موجود است
- ✅ مایگریشن‌ها اجرا شده‌اند
- ✅ دیتابیس سالم است

## 📝 یادداشت‌ها

- این اسکریپت برای سرورهای روسی بهینه شده است
- تمام عملیات با logging کامل انجام می‌شود
- backup خودکار قبل از هر تغییر ایجاد می‌شود
- اسکریپت قابل اجرا در Windows، Linux و Mac است

---

**تاریخ ایجاد:** 13 ژانویه 2025  
**نسخه:** 1.0  
**وضعیت:** آماده برای استفاده ✅
