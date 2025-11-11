from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user'

urlpatterns = [
    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Suscripciones
    path('suscribirse/<int:plan_id>/', views.iniciar_suscripcion, name='iniciar_suscripcion'),
    path('pasarela-pago/', views.pasarela_pago, name='pasarela_pago'),
    path('renovar/<int:suscripcion_id>/', views.renovar_suscripcion, name='renovar_suscripcion'),
    path('cancelar/<int:suscripcion_id>/', views.cancelar_suscripcion, name='cancelar_suscripcion'),
    
    # Registro de compras
    path('registrar-compra/', views.registrar_compra, name='registrar_compra'),
    path('mis-compras/', views.mis_registros_compra, name='mis_registros_compra'),
    path('compra/<int:registro_id>/', views.detalle_registro_compra, name='detalle_registro_compra'),
]
