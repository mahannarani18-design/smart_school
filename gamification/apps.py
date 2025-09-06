# مسیر: gamification/apps.py

from django.apps import AppConfig

class GamificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gamification'
    verbose_name = "امتیاز و پاداش"

    def ready(self):
        import gamification.signals # سیگنال‌ها را وارد کن