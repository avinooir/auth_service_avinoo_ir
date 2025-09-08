#!/usr/bin/env python
"""
Script to create initial data for the auth service.
This includes default roles, permissions, and sample data.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.roles.models import Role, Permission, RolePermission
from apps.permissions.models import PermissionGroup, PermissionGroupPermission
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


def create_default_permissions():
    """Create default permissions for the system."""
    print("Creating default permissions...")
    
    permissions_data = [
        # User management permissions
        {
            'name': 'users.view_user',
            'display_name': 'مشاهده کاربران',
            'description': 'اجازه مشاهده لیست کاربران',
            'app_label': 'users',
            'codename': 'view_user'
        },
        {
            'name': 'users.add_user',
            'display_name': 'افزودن کاربر',
            'description': 'اجازه ایجاد کاربر جدید',
            'app_label': 'users',
            'codename': 'add_user'
        },
        {
            'name': 'users.change_user',
            'display_name': 'ویرایش کاربر',
            'description': 'اجازه ویرایش اطلاعات کاربران',
            'app_label': 'users',
            'codename': 'change_user'
        },
        {
            'name': 'users.delete_user',
            'display_name': 'حذف کاربر',
            'description': 'اجازه حذف کاربران',
            'app_label': 'users',
            'codename': 'delete_user'
        },
        
        # Role management permissions
        {
            'name': 'roles.view_role',
            'display_name': 'مشاهده نقش‌ها',
            'description': 'اجازه مشاهده لیست نقش‌ها',
            'app_label': 'roles',
            'codename': 'view_role'
        },
        {
            'name': 'roles.add_role',
            'display_name': 'افزودن نقش',
            'description': 'اجازه ایجاد نقش جدید',
            'app_label': 'roles',
            'codename': 'add_role'
        },
        {
            'name': 'roles.change_role',
            'display_name': 'ویرایش نقش',
            'description': 'اجازه ویرایش نقش‌ها',
            'app_label': 'roles',
            'codename': 'change_role'
        },
        {
            'name': 'roles.delete_role',
            'display_name': 'حذف نقش',
            'description': 'اجازه حذف نقش‌ها',
            'app_label': 'roles',
            'codename': 'delete_role'
        },
        {
            'name': 'roles.assign_role',
            'display_name': 'اختصاص نقش',
            'description': 'اجازه اختصاص نقش به کاربران',
            'app_label': 'roles',
            'codename': 'assign_role'
        },
        
        # Permission management permissions
        {
            'name': 'permissions.view_permission',
            'display_name': 'مشاهده مجوزها',
            'description': 'اجازه مشاهده لیست مجوزها',
            'app_label': 'permissions',
            'codename': 'view_permission'
        },
        {
            'name': 'permissions.grant_permission',
            'display_name': 'اعطای مجوز',
            'description': 'اجازه اعطای مجوز به کاربران',
            'app_label': 'permissions',
            'codename': 'grant_permission'
        },
        {
            'name': 'permissions.revoke_permission',
            'display_name': 'لغو مجوز',
            'description': 'اجازه لغو مجوز از کاربران',
            'app_label': 'permissions',
            'codename': 'revoke_permission'
        },
        
        # System permissions
        {
            'name': 'system.view_audit_log',
            'display_name': 'مشاهده لاگ حسابرسی',
            'description': 'اجازه مشاهده لاگ‌های حسابرسی',
            'app_label': 'system',
            'codename': 'view_audit_log'
        },
        {
            'name': 'system.manage_system',
            'display_name': 'مدیریت سیستم',
            'description': 'اجازه مدیریت تنظیمات سیستم',
            'app_label': 'system',
            'codename': 'manage_system'
        }
    ]
    
    created_permissions = []
    for perm_data in permissions_data:
        permission, created = Permission.objects.get_or_create(
            name=perm_data['name'],
            defaults=perm_data
        )
        if created:
            created_permissions.append(permission)
            print(f"  ✓ Created permission: {permission.display_name}")
        else:
            print(f"  - Permission already exists: {permission.display_name}")
    
    print(f"Created {len(created_permissions)} new permissions")
    return created_permissions


def create_default_roles():
    """Create default roles for the system."""
    print("Creating default roles...")
    
    roles_data = [
        {
            'name': 'super_admin',
            'display_name': 'مدیر کل',
            'description': 'دسترسی کامل به تمام بخش‌های سیستم',
            'is_system_role': True
        },
        {
            'name': 'admin',
            'display_name': 'مدیر',
            'description': 'مدیریت کاربران، نقش‌ها و مجوزها',
            'is_system_role': True
        },
        {
            'name': 'moderator',
            'display_name': 'ناظر',
            'description': 'نظارت بر کاربران و محتوا',
            'is_system_role': True
        },
        {
            'name': 'user',
            'display_name': 'کاربر عادی',
            'description': 'کاربر عادی سیستم',
            'is_system_role': True
        }
    ]
    
    created_roles = []
    for role_data in roles_data:
        role, created = Role.objects.get_or_create(
            name=role_data['name'],
            defaults=role_data
        )
        if created:
            created_roles.append(role)
            print(f"  ✓ Created role: {role.display_name}")
        else:
            print(f"  - Role already exists: {role.display_name}")
    
    print(f"Created {len(created_roles)} new roles")
    return created_roles


def assign_permissions_to_roles():
    """Assign permissions to default roles."""
    print("Assigning permissions to roles...")
    
    try:
        # Get roles
        super_admin = Role.objects.get(name='super_admin')
        admin = Role.objects.get(name='admin')
        moderator = Role.objects.get(name='moderator')
        user = Role.objects.get(name='user')
        
        # Get permissions
        all_permissions = Permission.objects.all()
        user_permissions = Permission.objects.filter(app_label='users')
        role_permissions = Permission.objects.filter(app_label='roles')
        permission_permissions = Permission.objects.filter(app_label='permissions')
        system_permissions = Permission.objects.filter(app_label='system')
        
        # Super Admin - All permissions
        for permission in all_permissions:
            RolePermission.objects.get_or_create(
                role=super_admin,
                permission=permission
            )
        print(f"  ✓ Assigned all permissions to Super Admin")
        
        # Admin - User, Role, Permission management
        admin_permissions = user_permissions | role_permissions | permission_permissions
        for permission in admin_permissions:
            RolePermission.objects.get_or_create(
                role=admin,
                permission=permission
            )
        print(f"  ✓ Assigned admin permissions to Admin")
        
        # Moderator - User view and basic management
        moderator_permissions = Permission.objects.filter(
            name__in=[
                'users.view_user',
                'users.change_user',
                'roles.view_role',
                'permissions.view_permission'
            ]
        )
        for permission in moderator_permissions:
            RolePermission.objects.get_or_create(
                role=moderator,
                permission=permission
            )
        print(f"  ✓ Assigned moderator permissions to Moderator")
        
        # User - Basic permissions (if any)
        user_permissions = Permission.objects.filter(
            name__in=[
                'users.view_user'  # Users can view their own profile
            ]
        )
        for permission in user_permissions:
            RolePermission.objects.get_or_create(
                role=user,
                permission=permission
            )
        print(f"  ✓ Assigned user permissions to User")
        
    except Role.DoesNotExist as e:
        print(f"  ✗ Error: Role not found - {e}")
    except Exception as e:
        print(f"  ✗ Error assigning permissions: {e}")


def create_permission_groups():
    """Create permission groups for better organization."""
    print("Creating permission groups...")
    
    groups_data = [
        {
            'name': 'user_management',
            'display_name': 'مدیریت کاربران',
            'description': 'مجوزهای مربوط به مدیریت کاربران',
            'app_label': 'users'
        },
        {
            'name': 'role_management',
            'display_name': 'مدیریت نقش‌ها',
            'description': 'مجوزهای مربوط به مدیریت نقش‌ها',
            'app_label': 'roles'
        },
        {
            'name': 'permission_management',
            'display_name': 'مدیریت مجوزها',
            'description': 'مجوزهای مربوط به مدیریت مجوزها',
            'app_label': 'permissions'
        },
        {
            'name': 'system_management',
            'display_name': 'مدیریت سیستم',
            'description': 'مجوزهای مربوط به مدیریت سیستم',
            'app_label': 'system'
        }
    ]
    
    created_groups = []
    for group_data in groups_data:
        group, created = PermissionGroup.objects.get_or_create(
            name=group_data['name'],
            defaults=group_data
        )
        if created:
            created_groups.append(group)
            print(f"  ✓ Created permission group: {group.display_name}")
        else:
            print(f"  - Permission group already exists: {group.display_name}")
    
    # Assign permissions to groups
    for group in created_groups:
        app_label = group.app_label
        permissions = Permission.objects.filter(app_label=app_label)
        
        for permission in permissions:
            PermissionGroupPermission.objects.get_or_create(
                group=group,
                permission=permission
            )
        
        print(f"  ✓ Assigned {permissions.count()} permissions to {group.display_name}")
    
    print(f"Created {len(created_groups)} new permission groups")
    return created_groups


def assign_default_role_to_superuser():
    """Assign super_admin role to existing superusers."""
    print("Assigning super_admin role to superusers...")
    
    try:
        super_admin_role = Role.objects.get(name='super_admin')
        superusers = User.objects.filter(is_superuser=True)
        
        from apps.roles.models import UserRole
        
        for superuser in superusers:
            user_role, created = UserRole.objects.get_or_create(
                user=superuser,
                role=super_admin_role
            )
            if created:
                print(f"  ✓ Assigned super_admin role to {superuser.username}")
            else:
                print(f"  - {superuser.username} already has super_admin role")
        
    except Role.DoesNotExist:
        print("  ✗ super_admin role not found")
    except Exception as e:
        print(f"  ✗ Error assigning role to superuser: {e}")


def main():
    """Main function to create all initial data."""
    print("=" * 50)
    print("🚀 Creating Initial Data for Auth Service")
    print("=" * 50)
    print()
    
    try:
        # Create permissions
        create_default_permissions()
        print()
        
        # Create roles
        create_default_roles()
        print()
        
        # Assign permissions to roles
        assign_permissions_to_roles()
        print()
        
        # Create permission groups
        create_permission_groups()
        print()
        
        # Assign default role to superuser
        assign_default_role_to_superuser()
        print()
        
        print("=" * 50)
        print("✅ Initial data creation completed successfully!")
        print("=" * 50)
        print()
        print("Created:")
        print(f"  - {Permission.objects.count()} permissions")
        print(f"  - {Role.objects.count()} roles")
        print(f"  - {PermissionGroup.objects.count()} permission groups")
        print(f"  - {RolePermission.objects.count()} role-permission assignments")
        print()
        print("You can now use the admin panel to manage users, roles, and permissions.")
        
    except Exception as e:
        print(f"❌ Error creating initial data: {e}")
        logger.error(f"Error creating initial data: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
