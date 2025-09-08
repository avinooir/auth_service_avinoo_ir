"""
Views for Permissions app.
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

from .models import UserPermission, PermissionGroup, PermissionGroupPermission, AuditLog
from .serializers import (
    UserPermissionSerializer, UserPermissionCreateSerializer,
    PermissionGroupSerializer, PermissionGroupCreateSerializer,
    PermissionGroupPermissionSerializer, PermissionGroupPermissionCreateSerializer,
    AuditLogSerializer, UserWithPermissionsSerializer
)

logger = logging.getLogger(__name__)
User = get_user_model()


class UserPermissionListView(generics.ListCreateAPIView):
    """
    List and create user permissions.
    """
    
    queryset = UserPermission.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserPermissionCreateSerializer
        return UserPermissionSerializer
    
    def get_queryset(self):
        """Filter user permissions based on parameters."""
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id', None)
        permission_id = self.request.query_params.get('permission_id', None)
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        if permission_id:
            queryset = queryset.filter(permission_id=permission_id)
        
        return queryset
    
    @method_decorator(ratelimit(key='user', rate='10/m', method='POST'))
    def create(self, request, *args, **kwargs):
        """Grant permission to user."""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user_permission = serializer.save(granted_by=request.user)
                user_permission_serializer = UserPermissionSerializer(user_permission)
                
                # Create audit log
                AuditLog.objects.create(
                    user=request.user,
                    action='grant',
                    target_user=user_permission.user,
                    permission=user_permission.permission,
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    details={
                        'permission_name': user_permission.permission.name,
                        'user_username': user_permission.user.username
                    }
                )
                
                logger.info(f"Permission granted: {user_permission.permission.name} to {user_permission.user.username} by {request.user.username}")
                
                return Response({
                    'message': 'مجوز با موفقیت به کاربر اعطا شد.',
                    'user_permission': user_permission_serializer.data
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
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserPermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and delete user permission.
    """
    
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        """Revoke permission from user."""
        try:
            user_permission = self.get_object()
            user_permission.is_active = False
            user_permission.save()
            
            # Create audit log
            AuditLog.objects.create(
                user=request.user,
                action='revoke',
                target_user=user_permission.user,
                permission=user_permission.permission,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                details={
                    'permission_name': user_permission.permission.name,
                    'user_username': user_permission.user.username
                }
            )
            
            logger.info(f"Permission revoked: {user_permission.permission.name} from {user_permission.user.username} by {request.user.username}")
            
            return Response({
                'message': 'مجوز با موفقیت از کاربر لغو شد.'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Revoke permission error: {str(e)}")
            return Response({
                'error': 'خطایی در لغو مجوز رخ داد.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class PermissionGroupListView(generics.ListCreateAPIView):
    """
    List and create permission groups.
    """
    
    queryset = PermissionGroup.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PermissionGroupCreateSerializer
        return PermissionGroupSerializer
    
    def get_queryset(self):
        """Filter permission groups based on search parameters."""
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
    
    @method_decorator(ratelimit(key='user', rate='10/m', method='POST'))
    def create(self, request, *args, **kwargs):
        """Create new permission group."""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                group = serializer.save()
                group_serializer = PermissionGroupSerializer(group)
                
                logger.info(f"Permission group created: {group.name} by {request.user.username}")
                
                return Response({
                    'message': 'گروه مجوز با موفقیت ایجاد شد.',
                    'group': group_serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Ratelimited:
            return Response({
                'error': 'تعداد درخواست‌های شما بیش از حد مجاز است.'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        except Exception as e:
            logger.error(f"Create permission group error: {str(e)}")
            return Response({
                'error': 'خطایی در ایجاد گروه مجوز رخ داد.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PermissionGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and delete permission group.
    """
    
    queryset = PermissionGroup.objects.all()
    serializer_class = PermissionGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PermissionGroupCreateSerializer
        return PermissionGroupSerializer
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete permission group."""
        try:
            group = self.get_object()
            
            # Check if group has permissions
            permission_count = group.group_permissions.count()
            if permission_count > 0:
                return Response({
                    'error': f'گروه دارای {permission_count} مجوز است و قابل حذف نیست.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            group.is_active = False
            group.save()
            
            logger.info(f"Permission group deactivated: {group.name} by {request.user.username}")
            
            return Response({
                'message': 'گروه مجوز با موفقیت غیرفعال شد.'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Delete permission group error: {str(e)}")
            return Response({
                'error': 'خطایی در حذف گروه مجوز رخ داد.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PermissionGroupPermissionListView(generics.ListCreateAPIView):
    """
    List and create permission group permissions.
    """
    
    queryset = PermissionGroupPermission.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PermissionGroupPermissionCreateSerializer
        return PermissionGroupPermissionSerializer
    
    def get_queryset(self):
        """Filter group permissions based on parameters."""
        queryset = super().get_queryset()
        group_id = self.request.query_params.get('group_id', None)
        
        if group_id:
            queryset = queryset.filter(group_id=group_id)
        
        return queryset
    
    @method_decorator(ratelimit(key='user', rate='10/m', method='POST'))
    def create(self, request, *args, **kwargs):
        """Add permission to group."""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                group_permission = serializer.save(added_by=request.user)
                group_permission_serializer = PermissionGroupPermissionSerializer(group_permission)
                
                logger.info(f"Permission added to group: {group_permission.permission.name} to {group_permission.group.name} by {request.user.username}")
                
                return Response({
                    'message': 'مجوز با موفقیت به گروه اضافه شد.',
                    'group_permission': group_permission_serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Ratelimited:
            return Response({
                'error': 'تعداد درخواست‌های شما بیش از حد مجاز است.'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        except Exception as e:
            logger.error(f"Add permission to group error: {str(e)}")
            return Response({
                'error': 'خطایی در اضافه کردن مجوز به گروه رخ داد.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuditLogListView(generics.ListAPIView):
    """
    List audit logs.
    """
    
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter audit logs based on parameters."""
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id', None)
        action = self.request.query_params.get('action', None)
        target_user_id = self.request.query_params.get('target_user_id', None)
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        if action:
            queryset = queryset.filter(action=action)
        
        if target_user_id:
            queryset = queryset.filter(target_user_id=target_user_id)
        
        return queryset


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_permissions_view(request, user_id):
    """
    Get user permissions.
    """
    try:
        user = User.objects.get(id=user_id)
        user_permissions = user.direct_permissions.filter(is_active=True)
        
        serializer = UserPermissionSerializer(user_permissions, many=True)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'permissions': serializer.data
        }, status=status.HTTP_200_OK)
    
    except User.DoesNotExist:
        return Response({
            'error': 'کاربر یافت نشد.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        logger.error(f"Get user permissions error: {str(e)}")
        return Response({
            'error': 'خطایی در دریافت مجوزهای کاربر رخ داد.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
