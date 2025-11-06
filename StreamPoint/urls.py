# ============================================
# StreamPoint/urls.py (URLs Principales)
# ============================================
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),
    
    # Core Public (Acceso para todos)
    path('', include('core_public.urls')),
    
    # Core User (Usuarios registrados)
    path('user/', include('core_user.urls')),
    
    # Core Admin (Staff/Administradores)
    path('management/', include('core_admin.urls')),
]

# Personalización del admin
admin.site.site_header = "StreamPoint - Administración"
admin.site.site_title = "StreamPoint Admin"
admin.site.index_title = "Panel de Control"

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)