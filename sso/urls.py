"""
SSO URL Configuration
"""

from django.urls import path, include
from . import views

app_name = 'sso'

urlpatterns = [
    # API endpoints
    path('api/login/', views.SSOLoginView.as_view(), name='sso_login'),
    path('api/register/', views.SSORegisterView.as_view(), name='sso_register'),
    path('api/validate-token/', views.SSOTokenValidationView.as_view(), name='sso_validate_token'),
    path('api/callback/', views.SSOCallbackView.as_view(), name='sso_callback'),
    path('api/logout/', views.SSOLogoutView.as_view(), name='sso_logout'),
    path('api/user-info/', views.SSOUserInfoView.as_view(), name='sso_user_info'),
    
    # Web-based SSO pages
    path('login/', views.sso_login_page, name='sso_login_page'),
    path('register/', views.sso_register_page, name='sso_register_page'),
    path('callback/', views.sso_callback_page, name='sso_callback_page'),
    
    # Test page (protected)
    path('test/', views.test_protected_page, name='test_protected_page'),
    path('test/callback/', views.test_callback_page, name='test_callback_page'),
    path('test/login/', views.test_simple_login, name='test_simple_login'),
    
    # Admin endpoints
    path('api/admin/clients/', views.SSOClientListView.as_view(), name='sso_clients'),
    path('api/admin/sessions/', views.SSOSessionListView.as_view(), name='sso_sessions'),
    path('api/admin/logs/', views.SSOAuditLogListView.as_view(), name='sso_audit_logs'),
]
