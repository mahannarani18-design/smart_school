# مسیر: omr/apps.py

from django.apps import AppConfig

class OmrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'omr'
    verbose_name = "سیستم تصحیح آزمون (OMR)"