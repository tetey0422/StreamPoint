from django.urls import path
from . import views

app_name = 'admin_custom'

urlpatterns = [
    # Dashboard
    path('', views.admin_dashboard, name='dashboard'),
    
    # Validación de suscripciones
    path('validar-suscripciones/', views.validar_suscripciones, name='validar_suscripciones'),
    path('validar-suscripcion/<int:suscripcion_id>/', views.validar_suscripcion_accion, name='validar_suscripcion_accion'),
    
    # Gestión de puntos
    path('gestionar-puntos/', views.gestionar_puntos, name='gestionar_puntos'),
    
    # Gestión de compras registradas
    path('gestionar-compras/', views.gestionar_compras, name='gestionar_compras'),
    path('compra/<int:compra_id>/', views.detalle_compra_admin, name='detalle_compra_admin'),
    
    # Gestión de correos verificados
    path('gestionar-correos/', views.gestionar_correos_verificados, name='gestionar_correos'),
    
    # Reportes
    path('reportes/', views.reportes, name='reportes'),
    
    # Configuración
    path('configurar-recompensas/', views.configurar_recompensas, name='configurar_recompensas'),
]
