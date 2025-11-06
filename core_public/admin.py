# ============================================
# core_public/admin.py
# ============================================
from django.contrib import admin
from .models import CategoriaStreaming, ServicioStreaming, PlanSuscripcion, ConfiguracionRecompensa


@admin.register(CategoriaStreaming)
class CategoriaStreamingAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'activo', 'icono']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['activo']


@admin.register(ServicioStreaming)
class ServicioStreamingAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'activo', 'fecha_creacion']
    list_filter = ['categoria', 'activo']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['activo']
    date_hierarchy = 'fecha_creacion'


@admin.register(PlanSuscripcion)
class PlanSuscripcionAdmin(admin.ModelAdmin):
    list_display = ['servicio', 'nombre', 'precio', 'duracion', 'puntos_primera_compra', 'puntos_renovacion', 'activo']
    list_filter = ['servicio', 'duracion', 'activo']
    search_fields = ['nombre', 'servicio__nombre']
    list_editable = ['activo', 'precio']


@admin.register(ConfiguracionRecompensa)
class ConfiguracionRecompensaAdmin(admin.ModelAdmin):
    list_display = ['puntos_por_peso', 'puntos_minimos_canje', 'activo', 'fecha_modificacion']
    list_editable = ['activo']
