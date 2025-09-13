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
        self.app_secret = getattr(settings, 'MEET_JWT_SECRET', 'meet_secret_key_2024')
        self.external_api_url = getattr(settings, 'MEET_EXTERNAL_API_URL', 'http://avinoo.ir/api/meets/access/')
    
    def check_user_access(self, room_name, user_guid):
        """
        Check user access to meet room via external API
        """
        try:
            response = requests.get(self.external_api_url, params={
                'room_name': room_name,
                'user_guid': str(user_guid)
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data['data']
            
            logger.warning(f"External API check failed for room: {room_name}, user: {user_guid}")
            return None
            
        except Exception as e:
            logger.error(f"Error checking user access: {str(e)}")
            return None
    
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
                
                # Ensure token doesn't start in the past
                if token_start < now:
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
                        "sip": False,
                        "etherpad": False,
                        "transcription": True,
                        "breakout-rooms": True
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
