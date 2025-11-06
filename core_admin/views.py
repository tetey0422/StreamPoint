from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum
from core_user.models import Suscripcion, PerfilUsuario, TransaccionPuntos
from core_public.models import ConfiguracionRecompensa


@staff_member_required
def admin_dashboard(request):
    """Dashboard administrativo con estadísticas"""
    # Estadísticas generales
    suscripciones_pendientes = Suscripcion.objects.filter(
        validada=False,
        estado='pendiente'
    ).count()
    
    suscripciones_activas = Suscripcion.objects.filter(
        estado='activa'
    ).count()
    
    usuarios_registrados = PerfilUsuario.objects.count()
    
    puntos_totales = PerfilUsuario.objects.aggregate(
        total=Sum('puntos_disponibles')
    )['total'] or 0
    
    context = {
        'suscripciones_pendientes': suscripciones_pendientes,
        'suscripciones_activas': suscripciones_activas,
        'usuarios_registrados': usuarios_registrados,
        'puntos_totales': puntos_totales,
    }
    return render(request, 'admin_custom/dashboard.html', context)


@staff_member_required
def validar_suscripciones(request):
    """Lista de suscripciones pendientes de validación"""
    suscripciones_pendientes = Suscripcion.objects.filter(
        validada=False,
        estado='pendiente'
    ).order_by('-fecha_creacion')
    
    context = {
        'suscripciones': suscripciones_pendientes,
    }
    return render(request, 'admin_custom/validar_suscripciones.html', context)


@staff_member_required
def validar_suscripcion_accion(request, suscripcion_id):
    """Validar o rechazar una suscripción"""
    suscripcion = get_object_or_404(Suscripcion, id=suscripcion_id)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'aprobar':
            suscripcion.validada = True
            suscripcion.fecha_validacion = timezone.now()
            suscripcion.estado = 'activa'
            suscripcion.save()
            
            messages.success(
                request,
                f'Suscripción de {suscripcion.usuario.username} aprobada. '
                f'Se otorgaron {suscripcion.puntos_otorgados} puntos.'
            )
        
        elif accion == 'rechazar':
            motivo = request.POST.get('motivo', '')
            suscripcion.estado = 'cancelada'
            suscripcion.notas = f'Rechazada: {motivo}'
            suscripcion.save()
            
            messages.warning(
                request,
                f'Suscripción de {suscripcion.usuario.username} rechazada.'
            )
        
        return redirect('admin_custom:validar_suscripciones')
    
    context = {
        'suscripcion': suscripcion,
    }
    return render(request, 'admin_custom/validar_suscripcion_detalle.html', context)


@staff_member_required
def gestionar_puntos(request):
    """Gestión de puntos de usuarios"""
    perfiles = PerfilUsuario.objects.select_related('user').order_by('-puntos_disponibles')
    
    if request.method == 'POST':
        perfil_id = request.POST.get('perfil_id')
        cantidad = int(request.POST.get('cantidad', 0))
        descripcion = request.POST.get('descripcion', '')
        accion = request.POST.get('accion')
        
        perfil = get_object_or_404(PerfilUsuario, id=perfil_id)
        
        if accion == 'agregar':
            perfil.agregar_puntos(cantidad, f'Ajuste manual: {descripcion}')
            messages.success(request, f'{cantidad} puntos agregados a {perfil.user.username}')
        
        elif accion == 'quitar':
            if perfil.canjear_puntos(cantidad, f'Ajuste manual: {descripcion}'):
                messages.success(request, f'{cantidad} puntos removidos de {perfil.user.username}')
            else:
                messages.error(request, 'No hay suficientes puntos disponibles')
        
        return redirect('admin_custom:gestionar_puntos')
    
    context = {
        'perfiles': perfiles,
    }
    return render(request, 'admin_custom/gestionar_puntos.html', context)


@staff_member_required
def reportes(request):
    """Reportes y estadísticas del sistema"""
    # Aquí irían reportes más detallados
    context = {
        'titulo': 'Reportes del Sistema'
    }
    return render(request, 'admin_custom/reportes.html', context)


@staff_member_required
def configurar_recompensas(request):
    """Configurar el sistema de recompensas (cashback)"""
    config = ConfiguracionRecompensa.objects.filter(activo=True).first()
    
    if request.method == 'POST':
        if config:
            config.puntos_por_peso = int(request.POST.get('puntos_por_peso'))
            config.puntos_minimos_canje = int(request.POST.get('puntos_minimos_canje'))
            config.save()
            messages.success(request, 'Configuración actualizada exitosamente')
        return redirect('admin_custom:configurar_recompensas')
    
    context = {
        'config': config,
    }
    return render(request, 'admin_custom/configurar_recompensas.html', context)
