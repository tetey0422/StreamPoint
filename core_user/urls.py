from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user'

urlpatterns = [
    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='public:index'), name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Suscripciones
    path('suscribirse/<int:plan_id>/', views.iniciar_suscripcion, name='iniciar_suscripcion'),
    path('renovar/<int:suscripcion_id>/', views.renovar_suscripcion, name='renovar_suscripcion'),
    path('cancelar/<int:suscripcion_id>/', views.cancelar_suscripcion, name='cancelar_suscripcion'),
]
