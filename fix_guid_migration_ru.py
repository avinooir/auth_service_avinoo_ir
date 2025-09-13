#!/usr/bin/env python
"""
اسکریپت حل مشکل مایگریشن GUID برای سرور روسی
Script to fix GUID migration issue for Russian server
"""

import os
import sys
import django
import uuid
import logging
from datetime import datetime

# تنظیم logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('guid_migration_fix.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_django():
    """تنظیم Django"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
        django.setup()
        logger.info("Django setup completed successfully")
        return True
    except Exception as e:
        logger.error(f"Django setup failed: {e}")
        return False

def check_database_connection():
    """بررسی اتصال به دیتابیس"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def check_users_table():
    """بررسی جدول کاربران"""
    try:
        from django.db import connection
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        user_count = User.objects.count()
        logger.info(f"Total users in database: {user_count}")
        
        # بررسی ساختار جدول
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()
            
            guid_exists = any(col[1] == 'guid' for col in columns)
            logger.info(f"GUID column exists: {guid_exists}")
            
            return user_count, guid_exists, columns
            
    except Exception as e:
        logger.error(f"Error checking users table: {e}")
        return 0, False, []

def backup_database():
    """پشتیبان‌گیری از دیتابیس"""
    try:
        import shutil
        from django.conf import settings
        
        db_path = settings.DATABASES['default']['NAME']
        backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        shutil.copy2(db_path, backup_path)
        logger.info(f"Database backed up to: {backup_path}")
        return backup_path
        
    except Exception as e:
        logger.error(f"Database backup failed: {e}")
        return None

def fix_guid_migration():
    """حل مشکل مایگریشن GUID"""
    try:
        from django.db import connection
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        logger.info("Starting GUID migration fix...")
        
        with connection.cursor() as cursor:
            # بررسی وجود ستون guid
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()
            guid_exists = any(col[1] == 'guid' for col in columns)
            
            if not guid_exists:
                logger.info("Adding GUID column...")
                cursor.execute("ALTER TABLE users ADD COLUMN guid VARCHAR(36)")
                logger.info("GUID column added successfully")
            
            # بررسی کاربران بدون GUID
            cursor.execute("SELECT COUNT(*) FROM users WHERE guid IS NULL OR guid = ''")
            null_guid_count = cursor.fetchone()[0]
            
            if null_guid_count > 0:
                logger.info(f"Generating GUIDs for {null_guid_count} users...")
                
                # دریافت کاربران بدون GUID
                cursor.execute("SELECT id FROM users WHERE guid IS NULL OR guid = ''")
                user_ids = [row[0] for row in cursor.fetchall()]
                
                # تولید GUID برای هر کاربر
                for user_id in user_ids:
                    new_guid = str(uuid.uuid4())
                    cursor.execute("UPDATE users SET guid = %s WHERE id = %s", [new_guid, user_id])
                
                logger.info(f"Generated GUIDs for {len(user_ids)} users")
            
            # اعمال unique constraint
            logger.info("Applying unique constraint...")
            try:
                cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS users_guid_unique ON users(guid)")
                logger.info("Unique constraint applied successfully")
            except Exception as e:
                logger.warning(f"Unique constraint might already exist: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"GUID migration fix failed: {e}")
        return False

def verify_fix():
    """تأیید حل مشکل"""
    try:
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        users = User.objects.all()
        
        logger.info(f"Verifying fix for {users.count()} users...")
        
        success_count = 0
        for user in users:
            if hasattr(user, 'guid') and user.guid:
                success_count += 1
                logger.info(f"User {user.username}: GUID = {user.guid}")
            else:
                logger.error(f"User {user.username}: No GUID found!")
        
        if success_count == users.count():
            logger.info("SUCCESS: All users have GUIDs!")
            return True
        else:
            logger.error(f"ERROR: Only {success_count}/{users.count()} users have GUIDs")
            return False
            
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return False

def test_jwt_token():
    """تست JWT Token"""
    try:
        from django.contrib.auth import get_user_model
        from apps.users.jwt_serializers import CustomRefreshToken
        import jwt
        
        User = get_user_model()
        user = User.objects.first()
        
        if not user:
            logger.warning("No users found for JWT test")
            return False
        
        # تولید JWT Token
        refresh = CustomRefreshToken.for_user(user)
        access_token = refresh.access_token
        
        # دیکود کردن توکن
        decoded = jwt.decode(str(access_token), options={"verify_signature": False})
        
        if decoded.get('guid'):
            logger.info(f"SUCCESS: JWT Token contains GUID: {decoded.get('guid')}")
            return True
        else:
            logger.error("ERROR: JWT Token does not contain GUID")
            return False
            
    except Exception as e:
        logger.error(f"JWT test failed: {e}")
        return False

def mark_migration_as_applied():
    """علامت‌گذاری مایگریشن به عنوان اجرا شده"""
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            # بررسی وجود جدول django_migrations
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='django_migrations'")
            if cursor.fetchone():
                # بررسی وجود مایگریشن
                cursor.execute("SELECT COUNT(*) FROM django_migrations WHERE app='users' AND name='0002_user_guid'")
                count = cursor.fetchone()[0]
                
                if count == 0:
                    # اضافه کردن مایگریشن به جدول
                    cursor.execute("""
                        INSERT INTO django_migrations (app, name, applied) 
                        VALUES ('users', '0002_user_guid', %s)
                    """, [datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                    logger.info("Migration marked as applied")
                else:
                    logger.info("Migration already marked as applied")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to mark migration as applied: {e}")
        return False

def main():
    """تابع اصلی"""
    logger.info("=" * 60)
    logger.info("Starting GUID Migration Fix for Russian Server")
    logger.info("=" * 60)
    
    try:
        # 1. تنظیم Django
        if not setup_django():
            return False
        
        # 2. بررسی اتصال دیتابیس
        if not check_database_connection():
            return False
        
        # 3. بررسی جدول کاربران
        user_count, guid_exists, columns = check_users_table()
        if user_count == 0:
            logger.warning("No users found in database")
            return True
        
        # 4. پشتیبان‌گیری
        backup_path = backup_database()
        if backup_path:
            logger.info(f"Backup created: {backup_path}")
        
        # 5. حل مشکل مایگریشن
        if not fix_guid_migration():
            return False
        
        # 6. تأیید حل مشکل
        if not verify_fix():
            return False
        
        # 7. تست JWT Token
        if not test_jwt_token():
            logger.warning("JWT test failed, but GUID migration is complete")
        
        # 8. علامت‌گذاری مایگریشن
        mark_migration_as_applied()
        
        logger.info("=" * 60)
        logger.info("SUCCESS: GUID Migration Fix Completed Successfully!")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"Main execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
