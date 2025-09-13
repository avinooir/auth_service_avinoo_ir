# 🔧 حل مشکل مایگریشن GUID

## ❌ مشکل
```
django.db.utils.IntegrityError: UNIQUE constraint failed: new__users.guid
```

## 🔍 علت مشکل
وقتی فیلد `unique=True` به کاربران موجود اضافه می‌شود، Django نمی‌تواند مایگریشن را اجرا کند چون کاربران موجود GUID ندارند.

## ✅ راه حل

### روش 1: اجرای اسکریپت (توصیه شده)
```bash
python run_migration.py
```

### روش 2: اجرای دستی
```bash
# 1. اجرای مایگریشن
python manage.py migrate users

# 2. بررسی کاربران
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> for user in User.objects.all():
...     print(f"{user.username}: {user.guid}")
```

### روش 3: اگر مشکل ادامه داشت
```bash
# 1. حذف مایگریشن مشکل‌دار
rm apps/users/migrations/0002_user_guid.py

# 2. ایجاد مایگریشن جدید
python manage.py makemigrations users

# 3. اجرای مایگریشن
python manage.py migrate users
```

## 🧪 تست پس از مایگریشن

### بررسی GUID در دیتابیس
```python
from django.contrib.auth import get_user_model
User = get_user_model()

users = User.objects.all()
for user in users:
    print(f"User: {user.username}, GUID: {user.guid}")
```

### تست JWT Token
```python
from apps.users.jwt_serializers import CustomRefreshToken

user = User.objects.first()
refresh = CustomRefreshToken.for_user(user)
access_token = refresh.access_token

# دیکود کردن توکن
import jwt
decoded = jwt.decode(str(access_token), options={"verify_signature": False})
print(f"GUID in token: {decoded.get('guid')}")
```

## 📋 مراحل مایگریشن

مایگریشن در 3 مرحله انجام می‌شود:

1. **اضافه کردن فیلد** (بدون unique constraint)
2. **تولید GUID** برای کاربران موجود
3. **اعمال unique constraint**

## 🎯 نتیجه نهایی

پس از اجرای موفق مایگریشن:
- ✅ تمام کاربران GUID دارند
- ✅ GUID در JWT Token موجود است
- ✅ GUID در API responses موجود است
- ✅ GUID در پنل ادمین نمایش داده می‌شود
