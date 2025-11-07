from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Suscripcion, PerfilUsuario
from core_public.models import PlanSuscripcion


def registro(request):
    """Registro de nuevos usuarios"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}! Tu cuenta ha sido creada exitosamente.')
            return redirect('user:dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'user/registro.html', {'form': form})


@login_required
def dashboard(request):
    """Dashboard del usuario con sus suscripciones y puntos"""
    perfil = request.user.perfil
    suscripciones_activas = Suscripcion.objects.filter(
        usuario=request.user,
        estado='activa'
    )
    suscripciones_pendientes = Suscripcion.objects.filter(
        usuario=request.user,
        estado='pendiente'
    )
    
    historial_puntos = perfil.transacciones.all()[:10]
    
    context = {
        'perfil': perfil,
        'suscripciones_activas': suscripciones_activas,
        'suscripciones_pendientes': suscripciones_pendientes,
        'historial_puntos': historial_puntos,
    }
    return render(request, 'user/dashboard.html', context)


@login_required
def iniciar_suscripcion(request, plan_id):
    """Iniciar una nueva suscripción"""
    plan = get_object_or_404(PlanSuscripcion, id=plan_id, activo=True)
    
    if request.method == 'POST':
        # Obtener datos del formulario
        metodo_pago = request.POST.get('metodo_pago')
        email_servicio = request.POST.get('email_servicio')
        
        # VALIDAR SI PAGA CON PUNTOS
        if metodo_pago == 'puntos':
            puntos_necesarios = int(plan.precio * 10)  # 10 puntos = $1
            if request.user.perfil.puntos_disponibles < puntos_necesarios:
                messages.error(request, 'No tienes suficientes puntos disponibles.')
                return redirect('user:iniciar_suscripcion', plan_id=plan_id)
            
            # Descontar puntos
            request.user.perfil.canjear_puntos(
                puntos_necesarios,
                f"Canje por {plan.servicio.nombre} - {plan.nombre}"
            )
        
        # Verificar si es primera compra de este servicio
        es_primera = not Suscripcion.objects.filter(
            usuario=request.user,
            plan__servicio=plan.servicio
        ).exists()
        
        # Crear la suscripción
        suscripcion = Suscripcion.objects.create(
            usuario=request.user,
            plan=plan,
            fecha_inicio=timezone.now().date(),
            metodo_pago=metodo_pago,
            monto_pagado=plan.precio,
            email_servicio=email_servicio,
            es_primera_compra=es_primera,
            estado='pendiente'  # Requiere validación del admin
        )
        
        messages.success(
            request,
            f'Tu suscripción a {plan.servicio.nombre} ha sido registrada. '
            'Está pendiente de validación por un administrador.'
        )
        return redirect('user:dashboard')
    
    context = {
        'plan': plan,
    }
    return render(request, 'user/iniciar_suscripcion.html', context)


@login_required
def renovar_suscripcion(request, suscripcion_id):
    """Renovar una suscripción existente"""
    suscripcion = get_object_or_404(
        Suscripcion,
        id=suscripcion_id,
        usuario=request.user
    )
    
    if request.method == 'POST':
        # Crear nueva suscripción (renovación)
        nueva_suscripcion = Suscripcion.objects.create(
            usuario=request.user,
            plan=suscripcion.plan,
            fecha_inicio=suscripcion.fecha_vencimiento + timedelta(days=1),
            metodo_pago=request.POST.get('metodo_pago'),
            monto_pagado=suscripcion.plan.precio,
            email_servicio=suscripcion.email_servicio,
            es_primera_compra=False,
            estado='pendiente'
        )
        
        messages.success(request, 'Renovación registrada exitosamente.')
        return redirect('user:dashboard')
    
    context = {
        'suscripcion': suscripcion,
    }
    return render(request, 'user/renovar_suscripcion.html', context)


@login_required
def cancelar_suscripcion(request, suscripcion_id):
    """Cancelar una suscripción"""
    suscripcion = get_object_or_404(
        Suscripcion,
        id=suscripcion_id,
        usuario=request.user
    )
    
    if request.method == 'POST':
        suscripcion.estado = 'cancelada'
        suscripcion.save()
        messages.warning(request, f'Suscripción a {suscripcion.plan.servicio.nombre} cancelada.')
        return redirect('user:dashboard')
    
    context = {
        'suscripcion': suscripcion,
    }
    return render(request, 'user/cancelar_suscripcion.html', context)
