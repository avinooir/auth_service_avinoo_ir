#!/usr/bin/env python3
"""
اسکریپت سریع برای اصلاح ALLOWED_HOSTS
"""

import os
import sys

def fix_allowed_hosts():
    """اصلاح ALLOWED_HOSTS در فایل .env"""
    
    print("🔧 اصلاح ALLOWED_HOSTS...")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("📝 به‌روزرسانی فایل .env...")
        
        # Backup original file
        os.system('cp .env .env.backup')
        
        # Read current .env file
        with open('.env', 'r') as f:
            content = f.read()
        
        # Update ALLOWED_HOSTS
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('ALLOWED_HOSTS='):
                lines[i] = 'ALLOWED_HOSTS=localhost,127.0.0.1,auth.avinoo.ir,87.248.150.86'
                break
        
        # Write updated content
        with open('.env', 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ فایل .env به‌روزرسانی شد")
    else:
        print("⚠️  فایل .env یافت نشد. ایجاد فایل جدید...")
        
        env_content = """# Django Settings
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,auth.avinoo.ir,87.248.150.86

# Microservice Configuration
AUTH_SERVICE_DOMAIN=auth.avinoo.ir
ALLOWED_CLIENT_DOMAINS=app1.avinoo.ir,app2.avinoo.ir

# SSO Configuration
SSO_REDIRECT_URL=http://{domain}/callback
SSO_LOGIN_URL=http://{domain}/login
SSO_LOGOUT_URL=http://{domain}/logout

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=7

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://87.248.150.86:4141

# Logging
LOG_LEVEL=INFO"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ فایل .env ایجاد شد")
    
    print("")
    print("🎉 مشکل ALLOWED_HOSTS حل شد!")
    print("")
    print("🌐 آدرس‌های قابل دسترسی:")
    print("   - http://87.248.150.86:4141/test/")
    print("   - http://87.248.150.86:4141/login/")
    print("   - http://87.248.150.86:4141/admin/")
    print("")
    print("📝 سرور را راه‌اندازی مجدد کنید:")
    print("   python manage.py runserver 0.0.0.0:4141")

if __name__ == "__main__":
    fix_allowed_hosts()
