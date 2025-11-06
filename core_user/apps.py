# ============================================
# core_user/apps.py
# ============================================
from django.apps import AppConfig


class CoreUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_user'
    verbose_name = 'Gestión de Usuarios'
    
    def ready(self):
        # Importar signals cuando la app esté lista
        import core_user.signals
