"""
Serializers for User app.
"""

import logging
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, UserProfile

logger = logging.getLogger(__name__)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'phone_number', 'password', 'password_confirm',
            'first_name', 'last_name'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }
    
    def validate(self, attrs):
        """Validate registration data."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'رمز عبور و تأیید آن مطابقت ندارند.'
            })
        
        # Check if email already exists
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({
                'email': 'کاربری با این ایمیل قبلاً ثبت‌نام کرده است.'
            })
        
        # Check if username already exists
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({
                'username': 'کاربری با این نام کاربری قبلاً ثبت‌نام کرده است.'
            })
        
        # Check if phone number already exists
        if attrs.get('phone_number') and User.objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError({
                'phone_number': 'کاربری با این شماره تلفن قبلاً ثبت‌نام کرده است.'
            })
        
        return attrs
    
    def create(self, validated_data):
        """Create new user."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        logger.info(f"New user registered: {user.username}")
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    
    def validate(self, attrs):
        """Validate login credentials."""
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            # Try to authenticate with username or email
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                # Try with email if username failed
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(
                        request=self.context.get('request'),
                        username=user_obj.username,
                        password=password
                    )
                except User.DoesNotExist:
                    pass
            
            if user:
                if not user.is_active:
                    raise serializers.ValidationError({
                        'non_field_errors': 'حساب کاربری شما غیرفعال است.'
                    })
                
                if user.is_locked():
                    raise serializers.ValidationError({
                        'non_field_errors': 'حساب کاربری شما قفل شده است. لطفاً بعداً تلاش کنید.'
                    })
                
                # Reset failed login attempts on successful login
                user.reset_failed_login()
                
                attrs['user'] = user
                return attrs
            else:
                # Increment failed login attempts
                try:
                    user_obj = User.objects.get(username=username)
                    user_obj.increment_failed_login()
                except User.DoesNotExist:
                    try:
                        user_obj = User.objects.get(email=username)
                        user_obj.increment_failed_login()
                    except User.DoesNotExist:
                        pass
                
                raise serializers.ValidationError({
                    'non_field_errors': 'نام کاربری یا رمز عبور اشتباه است.'
                })
        else:
            raise serializers.ValidationError({
                'non_field_errors': 'نام کاربری و رمز عبور الزامی است.'
            })


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.
    """
    
    full_name_fa = serializers.ReadOnlyField()
    
    class Meta:
        model = UserProfile
        fields = [
            'first_name_fa', 'last_name_fa', 'full_name_fa',
            'avatar', 'bio', 'birth_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user information.
    """
    
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone_number', 'first_name', 'last_name',
            'full_name', 'is_phone_verified', 'is_email_verified', 'is_active',
            'date_joined', 'last_login', 'profile'
        ]
        read_only_fields = [
            'id', 'is_phone_verified', 'is_email_verified', 'is_active',
            'date_joined', 'last_login'
        ]
    
    def get_full_name(self, obj):
        """Get full name of user."""
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return obj.username


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password.
    """
    
    old_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    
    new_password = serializers.CharField(
        min_length=8,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    
    new_password_confirm = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    
    def validate_old_password(self, value):
        """Validate old password."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('رمز عبور فعلی اشتباه است.')
        return value
    
    def validate(self, attrs):
        """Validate password change data."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'رمز عبور جدید و تأیید آن مطابقت ندارند.'
            })
        return attrs
    
    def save(self):
        """Save new password."""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        logger.info(f"Password changed for user: {user.username}")
        return user
