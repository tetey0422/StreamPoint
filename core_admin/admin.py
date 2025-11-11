from django.contrib import admin
from .models import CorreoVerificado
from core_user.models import Suscripcion, PerfilUsuario, Factura

# Registrar modelos en el admin de Django
@admin.register(CorreoVerificado)
class CorreoVerificadoAdmin(admin.ModelAdmin):
    list_display = ['correo', 'servicio', 'activo', 'fecha_agregado', 'agregado_por']
    list_filter = ['servicio', 'activo', 'fecha_agregado']
    search_fields = ['correo', 'servicio__nombre']
    ordering = ['-fecha_agregado']


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['numero_factura', 'nombre_completo', 'monto_total', 'metodo_pago', 'pagado', 'fecha_creacion']
    list_filter = ['metodo_pago', 'pagado', 'fecha_creacion']
    search_fields = ['numero_factura', 'nombre_completo', 'correo']
    readonly_fields = ['numero_factura', 'fecha_creacion']
    ordering = ['-fecha_creacion']

