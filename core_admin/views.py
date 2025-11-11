from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum
from core_user.models import Suscripcion, PerfilUsuario, TransaccionPuntos, RegistroCompra
from core_public.models import ConfiguracionRecompensa, ServicioStreaming
from .models import CorreoVerificado


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
    # Filtro por estado
    estado_filtro = request.GET.get('estado', 'pendiente')
    
    if estado_filtro == 'todas':
        suscripciones = Suscripcion.objects.all()
    elif estado_filtro == 'pendiente':
        suscripciones = Suscripcion.objects.filter(
            validada=False,
            estado='pendiente'
        )
    elif estado_filtro == 'validadas':
        suscripciones = Suscripcion.objects.filter(
            validada=True
        )
    else:
        suscripciones = Suscripcion.objects.filter(
            validada=False,
            estado='pendiente'
        )
    
    suscripciones = suscripciones.select_related(
        'usuario', 'plan', 'plan__servicio'
    ).order_by('-fecha_creacion')
    
    # Estadísticas
    stats = {
        'pendientes': Suscripcion.objects.filter(validada=False, estado='pendiente').count(),
        'validadas': Suscripcion.objects.filter(validada=True).count(),
        'activas': Suscripcion.objects.filter(estado='activa').count(),
        'total': Suscripcion.objects.count(),
    }
    
    context = {
        'suscripciones': suscripciones,
        'estado_filtro': estado_filtro,
        'stats': stats,
    }
    return render(request, 'admin_custom/validar_suscripciones.html', context)


@staff_member_required
def validar_suscripcion_accion(request, suscripcion_id):
    """Validar o rechazar una suscripción"""
    suscripcion = get_object_or_404(Suscripcion, id=suscripcion_id)
    
    # Detectar si es primera compra
    es_primera_compra = not Suscripcion.objects.filter(
        usuario=suscripcion.usuario,
        plan__servicio=suscripcion.plan.servicio,
        validada=True
    ).exclude(id=suscripcion.id).exists()
    
    # Calcular puntos sugeridos
    if es_primera_compra:
        puntos_sugeridos = suscripcion.plan.puntos_primera_compra
    else:
        puntos_sugeridos = suscripcion.plan.puntos_renovacion
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'aprobar':
            puntos = int(request.POST.get('puntos', puntos_sugeridos))
            notas = request.POST.get('notas', '')
            
            suscripcion.validada = True
            suscripcion.fecha_validacion = timezone.now()
            suscripcion.estado = 'activa'
            suscripcion.es_primera_compra = es_primera_compra
            
            if notas:
                suscripcion.notas = notas
            
            suscripcion.save()
            
            # Los puntos ya se otorgan automáticamente en el save del modelo
            # pero podemos forzar la actualización si es necesario
            if suscripcion.puntos_otorgados == 0:
                perfil, created = PerfilUsuario.objects.get_or_create(user=suscripcion.usuario)
                tipo_compra = "Primera compra" if es_primera_compra else "Renovación"
                perfil.agregar_puntos(
                    puntos,
                    f"{tipo_compra} - {suscripcion.plan.servicio.nombre} - {suscripcion.plan.nombre}"
                )
                suscripcion.puntos_otorgados = puntos
                suscripcion.save(update_fields=['puntos_otorgados'])
            
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
        'es_primera_compra': es_primera_compra,
        'puntos_sugeridos': puntos_sugeridos,
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


@staff_member_required
def gestionar_correos_verificados(request):
    """Gestionar correos verificados para cada servicio"""
    servicios = ServicioStreaming.objects.filter(activo=True)
    correos = CorreoVerificado.objects.select_related('servicio').order_by('-fecha_agregado')
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'agregar':
            correo = request.POST.get('correo')
            servicio_id = request.POST.get('servicio_id')
            notas = request.POST.get('notas', '')
            
            if correo and servicio_id:
                try:
                    servicio = ServicioStreaming.objects.get(id=servicio_id)
                    CorreoVerificado.objects.create(
                        correo=correo,
                        servicio=servicio,
                        agregado_por=request.user,
                        notas=notas,
                        activo=True
                    )
                    messages.success(request, f'Correo {correo} verificado para {servicio.nombre}')
                except Exception as e:
                    messages.error(request, f'Error: {str(e)}')
        
        elif accion == 'eliminar':
            correo_id = request.POST.get('correo_id')
            try:
                correo_obj = CorreoVerificado.objects.get(id=correo_id)
                correo_obj.delete()
                messages.success(request, 'Correo eliminado de la lista de verificados')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        
        elif accion == 'toggle_activo':
            correo_id = request.POST.get('correo_id')
            try:
                correo_obj = CorreoVerificado.objects.get(id=correo_id)
                correo_obj.activo = not correo_obj.activo
                correo_obj.save()
                estado = 'activado' if correo_obj.activo else 'desactivado'
                messages.success(request, f'Correo {estado} exitosamente')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        
        return redirect('admin_custom:gestionar_correos')
    
    context = {
        'servicios': servicios,
        'correos': correos,
    }
    return render(request, 'admin_custom/gestionar_correos.html', context)


@staff_member_required
def gestionar_compras(request):
    """
    Listado de compras registradas por usuarios.
    El admin puede filtrar por estado y aprobar/rechazar.
    """
    # Filtro por estado
    estado_filtro = request.GET.get('estado', 'pendiente')
    
    if estado_filtro == 'todas':
        compras = RegistroCompra.objects.all()
    else:
        compras = RegistroCompra.objects.filter(estado=estado_filtro)
    
    compras = compras.select_related('usuario', 'servicio', 'plan', 'revisado_por').order_by('-fecha_registro')
    
    # Estadísticas
    stats = {
        'pendientes': RegistroCompra.objects.filter(estado='pendiente').count(),
        'aprobadas': RegistroCompra.objects.filter(estado='aprobada').count(),
        'rechazadas': RegistroCompra.objects.filter(estado='rechazada').count(),
        'total': RegistroCompra.objects.count(),
    }
    
    context = {
        'compras': compras,
        'estado_filtro': estado_filtro,
        'stats': stats,
    }
    return render(request, 'admin_custom/gestionar_compras.html', context)


@staff_member_required
def detalle_compra_admin(request, compra_id):
    """
    Detalle de una compra registrada con opciones de aprobar/rechazar.
    """
    compra = get_object_or_404(RegistroCompra, id=compra_id)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'aprobar':
            puntos = int(request.POST.get('puntos', 0))
            notas = request.POST.get('notas_admin', '')
            
            if puntos > 0:
                compra.aprobar(request.user, puntos)
                if notas:
                    compra.notas_admin = notas
                    compra.save()
                
                messages.success(
                    request,
                    f'Compra aprobada. Se otorgaron {puntos} puntos a {compra.usuario.username}.'
                )
                return redirect('admin_custom:gestionar_compras')
            else:
                messages.error(request, 'Debes ingresar una cantidad de puntos válida.')
        
        elif accion == 'rechazar':
            motivo = request.POST.get('motivo_rechazo', '')
            compra.rechazar(request.user, motivo)
            messages.warning(request, f'Compra rechazada.')
            return redirect('admin_custom:gestionar_compras')
    
    context = {
        'compra': compra,
    }
    return render(request, 'admin_custom/detalle_compra.html', context)
