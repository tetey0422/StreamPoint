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
    
    context = {
        'servicio': servicio,
        'planes': planes,
    }
    return render(request, 'public/detalle_servicio.html', context)


def informacion_proyecto(request):
    """Información sobre el proyecto StreamPoint"""
    return render(request, 'public/informacion_proyecto.html')
