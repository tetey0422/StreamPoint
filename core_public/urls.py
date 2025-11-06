from django.urls import path
from . import views

app_name = 'public'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalogo/', views.catalogo_servicios, name='catalogo'),
    path('servicio/<int:servicio_id>/', views.detalle_servicio, name='detalle_servicio'),
    path('proyecto/', views.informacion_proyecto, name='informacion_proyecto'),
]
