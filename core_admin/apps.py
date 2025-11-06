# ============================================
# core_admin/apps.py
# ============================================
from django.apps import AppConfig


class CoreAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_admin'
    verbose_name = 'Administración Personalizada'