# ============================================
# core_user/admin.py
# ============================================
from django.contrib import admin
from .models import PerfilUsuario, Suscripcion, TransaccionPuntos, RegistroCompra
from django.utils import timezone

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'puntos_totales', 'puntos_disponibles', 'fecha_registro', 'telefono']
    search_fields = ['user__username', 'user__email', 'telefono']
    readonly_fields = ['fecha_registro', 'puntos_totales']
    list_filter = ['fecha_registro']


@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'plan', 'estado', 'validada', 'es_primera_compra', 'fecha_vencimiento', 'puntos_otorgados']
    list_filter = ['estado', 'validada', 'es_primera_compra', 'metodo_pago']
    search_fields = ['usuario__username', 'plan__servicio__nombre', 'email_servicio']
    readonly_fields = ['fecha_creacion', 'puntos_otorgados', 'fecha_validacion']
    date_hierarchy = 'fecha_inicio'
    
    actions = ['validar_suscripciones', 'rechazar_suscripciones']
    
    def validar_suscripciones(self, request, queryset):
        """Acción para validar múltiples suscripciones"""
        count = 0
        for suscripcion in queryset.filter(validada=False):
            suscripcion.validada = True
            suscripcion.fecha_validacion = timezone.now()
            suscripcion.estado = 'activa'
            suscripcion.save()
            count += 1
        self.message_user(request, f'{count} suscripción(es) validada(s) exitosamente.')
    validar_suscripciones.short_description = "Validar suscripciones seleccionadas"
    
    def rechazar_suscripciones(self, request, queryset):
        """Acción para rechazar suscripciones"""
        count = queryset.filter(validada=False).update(estado='cancelada')
        self.message_user(request, f'{count} suscripción(es) rechazada(s).')
    rechazar_suscripciones.short_description = "Rechazar suscripciones seleccionadas"


@admin.register(TransaccionPuntos)
class TransaccionPuntosAdmin(admin.ModelAdmin):
    list_display = ['perfil', 'tipo', 'cantidad', 'descripcion', 'fecha']
    list_filter = ['tipo', 'fecha']
    search_fields = ['perfil__user__username', 'descripcion']
    readonly_fields = ['fecha']


@admin.register(RegistroCompra)
class RegistroCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'servicio', 'monto_pagado', 'estado', 'fecha_compra', 'fecha_registro', 'puntos_otorgados']
    list_filter = ['estado', 'servicio', 'fecha_compra', 'fecha_registro']
    search_fields = ['usuario__username', 'nombre_completo', 'correo', 'nombre_usuario_app']
    readonly_fields = ['fecha_registro', 'fecha_revision']
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('usuario', 'nombre_completo', 'correo', 'nombre_usuario_app', 'telefono')
        }),
        ('Información de la Compra', {
            'fields': ('servicio', 'plan', 'monto_pagado', 'fecha_compra', 'comprobante', 'descripcion')
        }),
        ('Estado y Revisión', {
            'fields': ('estado', 'fecha_registro', 'fecha_revision', 'revisado_por', 'puntos_otorgados', 'notas_admin')
        }),
    )


