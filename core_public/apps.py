# ============================================
# core_public/apps.py
# ============================================
from django.apps import AppConfig


class CorePublicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_public'
    verbose_name = 'Contenido Público'
