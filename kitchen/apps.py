# مسیر: kitchen/apps.py
from django.apps import AppConfig

class KitchenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kitchen'
    verbose_name = "آشپزخانه و انبار"