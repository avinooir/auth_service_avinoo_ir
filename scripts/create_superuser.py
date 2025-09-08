#!/usr/bin/env python
"""
Script to create superuser for the auth service
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError

User = get_user_model()


def create_superuser():
    """Create superuser for the auth service"""
    
    # Default superuser credentials
    username = 'admin'
    email = 'admin@avinoo.ir'
    password = 'admin123456'
    
    try:
        # Check if superuser already exists
        if User.objects.filter(username=username).exists():
            print(f"⚠️  Superuser '{username}' already exists.")
            return
        
        # Create superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='مدیر',
            last_name='سیستم'
        )
        
        print("✅ Superuser created successfully!")
        print(f"   - Username: {username}")
        print(f"   - Email: {email}")
        print(f"   - Password: {password}")
        print()
        print("🔐 Login credentials:")
        print(f"   - Admin Panel: http://127.0.0.1:8000/admin/")
        print(f"   - Username: {username}")
        print(f"   - Password: {password}")
        print()
        print("⚠️  Important: Change the password after first login!")
        
    except IntegrityError:
        print(f"❌ Error: Superuser '{username}' already exists.")
    except Exception as e:
        print(f"❌ Error creating superuser: {str(e)}")


if __name__ == '__main__':
    create_superuser()
