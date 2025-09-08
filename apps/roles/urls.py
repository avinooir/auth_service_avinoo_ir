"""
URLs for Role app.
"""

from django.urls import path
from . import views

app_name = 'roles'

urlpatterns = [
    # Role management
    path('', views.RoleListView.as_view(), name='role_list'),
    path('<int:pk>/', views.RoleDetailView.as_view(), name='role_detail'),
    
    # User role management
    path('user-roles/', views.UserRoleListView.as_view(), name='user_role_list'),
    path('user-roles/<int:pk>/', views.UserRoleDetailView.as_view(), name='user_role_detail'),
    path('users/<int:user_id>/roles/', views.user_roles_view, name='user_roles'),
    
    # Permission management
    path('permissions/', views.PermissionListView.as_view(), name='permission_list'),
    
    # Role permission management
    path('role-permissions/', views.RolePermissionListView.as_view(), name='role_permission_list'),
]
