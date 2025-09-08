"""
URLs for Permissions app.
"""

from django.urls import path
from . import views

app_name = 'permissions'

urlpatterns = [
    # User permission management
    path('user-permissions/', views.UserPermissionListView.as_view(), name='user_permission_list'),
    path('user-permissions/<int:pk>/', views.UserPermissionDetailView.as_view(), name='user_permission_detail'),
    path('users/<int:user_id>/permissions/', views.user_permissions_view, name='user_permissions'),
    
    # Permission group management
    path('groups/', views.PermissionGroupListView.as_view(), name='permission_group_list'),
    path('groups/<int:pk>/', views.PermissionGroupDetailView.as_view(), name='permission_group_detail'),
    
    # Permission group permission management
    path('group-permissions/', views.PermissionGroupPermissionListView.as_view(), name='permission_group_permission_list'),
    
    # Audit logs
    path('audit-logs/', views.AuditLogListView.as_view(), name='audit_log_list'),
]
