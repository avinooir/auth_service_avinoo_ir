"""
Views for Role app.
"""

import logging
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django_ratelimit.decorators import ratelimit
from django_ratelimit.exceptions import Ratelimited
from django.db.models import Q

from .models import Role, UserRole, Permission, RolePermission
from .serializers import (
    RoleSerializer, RoleCreateSerializer, UserRoleSerializer,
    UserRoleCreateSerializer, RolePermissionSerializer,
    RolePermissionCreateSerializer, UserWithRolesSerializer,
    PermissionSerializer
)

logger = logging.getLogger(__name__)
User = get_user_model()


class RoleListView(generics.ListCreateAPIView):
    """
    List and create roles.
    """
    
    queryset = Role.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RoleCreateSerializer
        return RoleSerializer
    
    def get_queryset(self):
        """Filter roles based on search parameters."""
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(display_name__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """List roles with pagination."""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            
            return Response({
                'roles': serializer.data,
                'count': queryset.count()
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"List roles error: {str(e)}")
            return Response({
                'error': 'خطایی در دریافت لیست نقش‌ها رخ داد.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @method_decorator(ratelimit(key='user', rate='10/m', method='POST'))
    def create(self, request, *args, **kwargs):
        """Create new role."""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                role = serializer.save()
                role_serializer = RoleSerializer(role)
                
                logger.info(f"Role created: {role.name} by {request.user.username}")
                
                return Response({
                    'message': 'نقش با موفقیت ایجاد شد.',
                    'role': role_serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Ratelimited:
            return Response({
                'error': 'تعداد درخواست‌های شما بیش از حد مجاز است.'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        except Exception as e:
            logger.error(f"Create role error: {str(e)}")
            return Response({
                'error': 'خطایی در ایجاد نقش رخ داد.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and delete role.
    """
    
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RoleCreateSerializer
        return RoleSerializer
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete role."""
        try:
            role = self.get_object()
            
            if role.is_system_role:
                return Response({
                    'error': 'نقش‌های سیستمی قابل حذف نیستند.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if role has active users
            active_users = role.role_users.filter(is_active=True).count()
            if active_users > 0:
                return Response({
                    'error': f'نقش دارای {active_users} کاربر فعال است و قابل حذف نیست.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            role.is_active = False
            role.save()
            
            logger.info(f"Role deactivated: {role.name} by {request.user.username}")
            
            return Response({
                'message': 'نقش با موفقیت غیرفعال شد.'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Delete role error: {str(e)}")
            return Response({
                'error': 'خطایی در حذف نقش رخ داد.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRoleListView(generics.ListCreateAPIView):
    """
    List and create user roles.
    """
    
    queryset = UserRole.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserRoleCreateSerializer
        return UserRoleSerializer
    
    def get_queryset(self):
        """Filter user roles based on parameters."""
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id', None)
        role_id = self.request.query_params.get('role_id', None)
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        if role_id:
            queryset = queryset.filter(role_id=role_id)
        
        return queryset
    
    @method_decorator(ratelimit(key='user', rate='10/m', method='POST'))
    def create(self, request, *args, **kwargs):
        """Assign role to user."""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user_role = serializer.save(assigned_by=request.user)
                user_role_serializer = UserRoleSerializer(user_role)
                
                logger.info(f"Role assigned: {user_role.role.name} to {user_role.user.username} by {request.user.username}")
                
                return Response({
                    'message': 'نقش با موفقیت به کاربر اختصاص داده شد.',
                    'user_role': user_role_serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Ratelimited:
            return Response({
                'error': 'تعداد درخواست‌های شما بیش از حد مجاز است.'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        except Exception as e:
            logger.error(f"Assign role error: {str(e)}")
            return Response({
                'error': 'خطایی در اختصاص نقش رخ داد.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and delete user role.
    """
    
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        """Remove role from user."""
        try:
            user_role = self.get_object()
            user_role.is_active = False
            user_role.save()
            
            logger.info(f"Role removed: {user_role.role.name} from {user_role.user.username} by {request.user.username}")
            
            return Response({
                'message': 'نقش با موفقیت از کاربر حذف شد.'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Remove role error: {str(e)}")
            return Response({
                'error': 'خطایی در حذف نقش رخ داد.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PermissionListView(generics.ListAPIView):
    """
    List permissions.
    """
    
    queryset = Permission.objects.filter(is_active=True)
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter permissions based on search parameters."""
        queryset = super().get_queryset()
        app_label = self.request.query_params.get('app_label', None)
        search = self.request.query_params.get('search', None)
        
        if app_label:
            queryset = queryset.filter(app_label=app_label)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(display_name__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset


class RolePermissionListView(generics.ListCreateAPIView):
    """
    List and create role permissions.
    """
    
    queryset = RolePermission.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RolePermissionCreateSerializer
        return RolePermissionSerializer
    
    def get_queryset(self):
        """Filter role permissions based on parameters."""
        queryset = super().get_queryset()
        role_id = self.request.query_params.get('role_id', None)
        
        if role_id:
            queryset = queryset.filter(role_id=role_id)
        
        return queryset
    
    @method_decorator(ratelimit(key='user', rate='10/m', method='POST'))
    def create(self, request, *args, **kwargs):
        """Grant permission to role."""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                role_permission = serializer.save(granted_by=request.user)
                role_permission_serializer = RolePermissionSerializer(role_permission)
                
                logger.info(f"Permission granted: {role_permission.permission.name} to {role_permission.role.name} by {request.user.username}")
                
                return Response({
                    'message': 'مجوز با موفقیت به نقش اعطا شد.',
                    'role_permission': role_permission_serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Ratelimited:
            return Response({
                'error': 'تعداد درخواست‌های شما بیش از حد مجاز است.'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        except Exception as e:
            logger.error(f"Grant permission error: {str(e)}")
            return Response({
                'error': 'خطایی در اعطای مجوز رخ داد.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_roles_view(request, user_id):
    """
    Get user roles.
    """
    try:
        user = User.objects.get(id=user_id)
        user_roles = user.user_roles.filter(is_active=True)
        
        serializer = UserRoleSerializer(user_roles, many=True)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'roles': serializer.data
        }, status=status.HTTP_200_OK)
    
    except User.DoesNotExist:
        return Response({
            'error': 'کاربر یافت نشد.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        logger.error(f"Get user roles error: {str(e)}")
        return Response({
            'error': 'خطایی در دریافت نقش‌های کاربر رخ داد.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
