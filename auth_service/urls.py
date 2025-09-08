"""
URL configuration for auth_service project.

Professional microservice authentication service with JWT support.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # SSO endpoints (main microservice endpoints)
    path('', include('sso.urls')),
    
    # Authentication endpoints (legacy)
    path('auth/', include('apps.users.urls')),
    
    # Role management endpoints
    path('roles/', include('apps.roles.urls')),
    
    # Permission management endpoints
    path('permissions/', include('apps.permissions.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
