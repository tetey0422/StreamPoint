from django.shortcuts import render, get_object_or_404
from .models import ServicioStreaming, CategoriaStreaming, PlanSuscripcion


def index(request):
    """Página principal - Vista pública"""
    servicios_destacados = ServicioStreaming.objects.filter(activo=True)[:6]
    categorias = CategoriaStreaming.objects.filter(activo=True)
    
    context = {
        'servicios_destacados': servicios_destacados,
        'categorias': categorias,
    }
    return render(request, 'public/index.html', context)


def catalogo_servicios(request):
    """Catálogo completo de servicios de streaming"""
    categoria_id = request.GET.get('categoria')
    
    if categoria_id:
        servicios = ServicioStreaming.objects.filter(
            categoria_id=categoria_id,
            activo=True
        )
    else:
        servicios = ServicioStreaming.objects.filter(activo=True)
    
    categorias = CategoriaStreaming.objects.filter(activo=True)
    
    context = {
        'servicios': servicios,
        'categorias': categorias,
        'categoria_seleccionada': categoria_id,
    }
    return render(request, 'public/catalogo.html', context)


def detalle_servicio(request, servicio_id):
    """Detalle de un servicio con sus planes"""
    servicio = get_object_or_404(ServicioStreaming, id=servicio_id, activo=True)
    planes = servicio.planes.filter(activo=True)
    
    # Obtener puntos del usuario y configuración
    puntos_disponibles = 0
    config = None
    if request.user.is_authenticated:
        from core_user.models import PerfilUsuario
        from .models import ConfiguracionRecompensa
        try:
            perfil = PerfilUsuario.objects.get(user=request.user)
            puntos_disponibles = perfil.puntos_disponibles
            config = ConfiguracionRecompensa.objects.filter(activo=True).first()
        except PerfilUsuario.DoesNotExist:
            pass
    
    # Calcular para cada plan si puede pagarse con puntos
    planes_con_info = []
    for plan in planes:
        plan_info = {
            'plan': plan,
            'puede_pagar_con_puntos': False,
            'puntos_necesarios': 0,
            'puntos_faltantes': 0,
        }
        
        if config:
            puntos_necesarios = int(plan.precio * config.puntos_por_peso)
            plan_info['puntos_necesarios'] = puntos_necesarios
            plan_info['puede_pagar_con_puntos'] = puntos_disponibles >= puntos_necesarios
            plan_info['puntos_faltantes'] = max(0, puntos_necesarios - puntos_disponibles)
        
        planes_con_info.append(plan_info)
    
    context = {
        'servicio': servicio,
        'planes': planes,
        'planes_con_info': planes_con_info,
        'puntos_disponibles': puntos_disponibles,
        'config': config,
    }
    return render(request, 'public/detalle_servicio.html', context)


def informacion_proyecto(request):
    """Información sobre el proyecto StreamPoint"""
    return render(request, 'public/informacion_proyecto.html')
