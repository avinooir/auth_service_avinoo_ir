"""
URLs for User app.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile endpoints
    path('me/', views.UserProfileView.as_view(), name='user_profile'),
    path('profile/', views.UserProfileDetailView.as_view(), name='profile_detail'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]
