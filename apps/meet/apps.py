"""
Meet integration app configuration
"""

from django.apps import AppConfig


class MeetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.meet'
    verbose_name = 'Meet Integration'
    
    def ready(self):
        """App is ready"""
        pass
