"""
Views for User app.
"""

import logging
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django_ratelimit.decorators import ratelimit
from django_ratelimit.exceptions import Ratelimited
from django.core.exceptions import ValidationError

from .models import User, UserProfile
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    UserProfileSerializer, ChangePasswordSerializer
)

logger = logging.getLogger(__name__)
User = get_user_model()


class UserRegistrationView(APIView):
    """
    User registration endpoint.
    """
    
    permission_classes = [permissions.AllowAny]
    
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST'))
    @method_decorator(never_cache)
    def post(self, request):
        """Register new user."""
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                
                # Get user data
                user_serializer = UserSerializer(user)
                
                logger.info(f"User registered successfully: {user.username}")
                
                return Response({
                    'message': 'ثبت‌نام با موفقیت انجام شد.',
                    'user': user_serializer.data,
                    'tokens': {
                        'access': str(access_token),
                        'refresh': str(refresh)
                    }
                }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Ratelimited:
            return Response({
                'error': 'تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً کمی صبر کنید.'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return Response({
                'error': 'خطایی در ثبت‌نام رخ داد. لطفاً دوباره تلاش کنید.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(TokenObtainPairView):
    """
    User login endpoint with JWT tokens.
    """
    
    permission_classes = [permissions.AllowAny]
    
    @method_decorator(ratelimit(key='ip', rate='10/m', method='POST'))
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        """Login user and return JWT tokens."""
        try:
            serializer = UserLoginSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                user = serializer.validated_data['user']
                
                # Update last login IP
                client_ip = self.get_client_ip(request)
                user.update_last_login_ip(client_ip)
                
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                
                # Get user data
                user_serializer = UserSerializer(user)
                
                logger.info(f"User logged in successfully: {user.username}")
                
                return Response({
                    'message': 'ورود با موفقیت انجام شد.',
                    'user': user_serializer.data,
                    'tokens': {
                        'access': str(access_token),
                        'refresh': str(refresh)
                    }
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Ratelimited:
            return Response({
                'error': 'تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً کمی صبر کنید.'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return Response({
                'error': 'خطایی در ورود رخ داد. لطفاً دوباره تلاش کنید.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update user profile.
    """
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Get current user."""
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        """Get current user profile."""
        try:
            user = self.get_object()
            serializer = self.get_serializer(user)
            
            return Response({
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Get profile error: {str(e)}")
            return Response({
                'error': 'خطایی در دریافت پروفایل رخ داد.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, *args, **kwargs):
        """Update user profile."""
        try:
            user = self.get_object()
            serializer = self.get_serializer(user, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                logger.info(f"User profile updated: {user.username}")
                
                return Response({
                    'message': 'پروفایل با موفقیت بروزرسانی شد.',
                    'user': serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"Update profile error: {str(e)}")
            return Response({
                'error': 'خطایی در بروزرسانی پروفایل رخ داد.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Get and update user profile details.
    """
    
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Get current user profile."""
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class ChangePasswordView(APIView):
    """
    Change user password.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    @method_decorator(ratelimit(key='user', rate='5/m', method='POST'))
    def post(self, request):
        """Change user password."""
        try:
            serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
            
            if serializer.is_valid():
                serializer.save()
                
                return Response({
                    'message': 'رمز عبور با موفقیت تغییر کرد.'
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Ratelimited:
            return Response({
                'error': 'تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً کمی صبر کنید.'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        except Exception as e:
            logger.error(f"Change password error: {str(e)}")
            return Response({
                'error': 'خطایی در تغییر رمز عبور رخ داد.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Logout user by blacklisting refresh token.
    """
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            logger.info(f"User logged out: {request.user.username}")
            
            return Response({
                'message': 'خروج با موفقیت انجام شد.'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'توکن refresh الزامی است.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return Response({
            'error': 'خطایی در خروج رخ داد.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
