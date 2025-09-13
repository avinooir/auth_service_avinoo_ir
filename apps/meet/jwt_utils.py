"""
JWT utilities for meet.avinoo.ir integration
"""

import logging
import jwt
import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


class MeetJWTGenerator:
    """
    JWT token generator for meet.avinoo.ir
    """
    
    def __init__(self):
        self.app_id = "meet_avinoo"
        self.domain = "meet.avinoo.ir"
        self.app_secret = getattr(settings, 'MEET_JWT_SECRET', 'super_secret_key_98765')
        self.external_api_url = getattr(settings, 'MEET_EXTERNAL_API_URL', 'http://avinoo.ir/api/meets/access/')
    
    def check_user_access(self, room_name, user):
        """
        Check user access to meet room via external API
        Returns tuple: (access_data, error_message)
        """
        try:
            # استفاده از GUID کاربر از فیلد guid در مدل User
            user_guid = user.guid
            logger.info(f"Checking access for user {user.username} (GUID: {user_guid}) to room {room_name}")
            
            response = requests.get(self.external_api_url, params={
                'room_name': room_name,
                'user_guid': str(user_guid)
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    access_data = data['data']
                    
                    # بررسی دسترسی کاربر
                    if not access_data.get('has_access', False):
                        return None, "شما دسترسی به این جلسه ندارید"
                    
                    # بررسی وضعیت جلسه
                    status = access_data.get('status', '')
                    if status == 'past':
                        return None, "این جلسه به پایان رسیده است"
                    elif status == 'upcoming':
                        start_time = access_data.get('start_time', '')
                        return None, f"جلسه هنوز شروع نشده است. زمان شروع: {start_time}"
                    elif status == 'ongoing':
                        return access_data, None
                    else:
                        return access_data, None
                else:
                    # اگر API کاربر را نشناسد، خطا نمایش بده
                    error_msg = data.get('error', 'کاربر یافت نشد')
                    logger.warning(f"API user not found for GUID: {user_guid}, error: {error_msg}")
                    return None, f"کاربر در سیستم جلسات یافت نشد: {error_msg}"
            else:
                # اگر API در دسترس نباشد، خطا نمایش بده
                if response.status_code == 404:
                    try:
                        error_data = response.json()
                        error_msg = error_data.get('error', 'کاربر یافت نشد')
                        logger.warning(f"API user not found (404): {error_msg.encode('utf-8', 'ignore').decode('utf-8')}")
                        return None, f"کاربر در سیستم جلسات یافت نشد: {error_msg}"
                    except:
                        logger.warning(f"API user not found (404)")
                        return None, "کاربر در سیستم جلسات یافت نشد"
                else:
                    logger.warning(f"API unavailable (status: {response.status_code})")
                    return None, f"خطا در ارتباط با سرور جلسات (کد: {response.status_code})"
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout checking user access for room: {room_name}, user: {user_guid}")
            return None, "خطا در ارتباط با سرور - زمان انتظار به پایان رسید"
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error checking user access for room: {room_name}, user: {user_guid}")
            return None, "خطا در ارتباط با سرور"
        except Exception as e:
            logger.error(f"Error checking user access: {str(e)}")
            return None, "خطای غیرمنتظره در بررسی دسترسی"
    
    def _get_default_access_data(self, room_name):
        """
        اطلاعات پیش‌فرض دسترسی برای زمانی که API در دسترس نیست
        """
        from datetime import datetime, timedelta
        
        # زمان فعلی
        now = datetime.now()
        
        # اطلاعات پیش‌فرض - جلسه در حال برگزاری
        start_time = now - timedelta(minutes=30)  # جلسه 30 دقیقه پیش شروع شده
        end_time = now + timedelta(hours=1)       # جلسه 1 ساعت دیگر تمام می‌شود
        
        return {
            'meet_id': 1,
            'meet_title': f'جلسه {room_name}',
            'room_name': room_name,
            'meeting_type': 'online',
            'meeting_link': f'http://meet.avinoo.ir/{room_name}',
            'start_time': start_time.isoformat() + '+00:00',
            'end_time': end_time.isoformat() + '+00:00',
            'status': 'ongoing',
            'has_access': True,
            'user_type': 'participant',
            'is_organizer': False,
            'is_participant': True,
            'is_active': True,
            'is_upcoming': False,
            'is_past': False
        }
    
    def generate_meet_jwt(self, user, room_name, access_data=None):
        """
        Generate JWT token for meet.avinoo.ir
        """
        try:
            # Get current time
            now = timezone.now()
            
            # Calculate token expiration based on meeting time
            if access_data and access_data.get('start_time') and access_data.get('end_time'):
                start_time = datetime.fromisoformat(access_data['start_time'].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(access_data['end_time'].replace('Z', '+00:00'))
                
                # Token valid from 10 minutes before start to 10 minutes after end
                token_start = start_time - timedelta(minutes=10)
                token_end = end_time + timedelta(minutes=10)
                
                # Ensure token doesn't start in the future
                if token_start > now:
                    token_start = now
                
                exp = int(token_end.timestamp())
                nbf = int(token_start.timestamp())
            else:
                # Default: 1 hour from now
                exp = int((now + timedelta(hours=1)).timestamp())
                nbf = int(now.timestamp())
            
            # Get user data
            user_data = user.get_meet_user_data()
            
            # Determine user role and permissions
            is_moderator = False
            if access_data:
                is_moderator = access_data.get('is_organizer', False) or access_data.get('user_type') == 'organizer'
            else:
                is_moderator = user.is_superuser or user.is_staff
            
            # Build JWT payload - exact format as requested
            payload = {
                "aud": self.app_id,
                "iss": self.app_id,
                "sub": self.domain,
                "room": room_name,
                "exp": exp,
                "nbf": nbf,
                "moderator": is_moderator,
            "context": {
                "user": {
                    "id": str(user.id),
                    "name": user_data.get('name', ''),
                    "email": user_data.get('email', ''),
                    "avatar": user_data.get('avatar', ''),
                    "affiliation": user_data.get('affiliation', 'member'),
                    "moderator": user_data.get('moderator', False),
                    "region": user_data.get('region', 'us-east'),
                    "displayName": user_data.get('displayName', '')
                },
                "group": "dev-team",
                "features": {
                    "livestreaming": True,
                    "recording": True,
                    "screen-sharing": True,
                    "transcription": True
                }
            },
                "identity": {
                    "type": "user",
                    "guest": False,
                    "externalId": f"ext-{user.id}"
                },
                "custom": {
                    "theme": "green",
                    "allowKnocking": True,
                    "enablePolls": True
                }
            }
            
            # Generate JWT token
            token = jwt.encode(payload, self.app_secret, algorithm="HS256")
            
            logger.info(f"Meet JWT generated for user {user.username} in room {room_name}")
            return token
            
        except Exception as e:
            logger.error(f"Error generating meet JWT: {str(e)}")
            return None
    
    def generate_meet_redirect_url(self, user, room_name, access_data=None):
        """
        Generate complete redirect URL with JWT token for meet.avinoo.ir
        """
        try:
            # Generate JWT token
            jwt_token = self.generate_meet_jwt(user, room_name, access_data)
            
            if not jwt_token:
                return None
            
            # Build redirect URL
            redirect_url = f"https://meet.avinoo.ir/{room_name}?jwt={jwt_token}"
            
            logger.info(f"Meet redirect URL generated for user {user.username} in room {room_name}")
            return redirect_url
            
        except Exception as e:
            logger.error(f"Error generating meet redirect URL: {str(e)}")
            return None


def get_meet_jwt_generator():
    """
    Get MeetJWTGenerator instance
    """
    return MeetJWTGenerator()
