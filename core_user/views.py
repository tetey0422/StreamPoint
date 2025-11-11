from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings
from .models import Suscripcion, PerfilUsuario, Factura, RegistroCompra
from .forms import RegistroCompraForm
from core_public.models import PlanSuscripcion, ConfiguracionRecompensa
from core_admin.models import CorreoVerificado


def registro(request):
    """Registro de nuevos usuarios"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            try:
                user = form.save()
                perfil, created = PerfilUsuario.objects.get_or_create(user=user)
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.username}! Tu cuenta ha sido creada exitosamente.')
                return redirect('user:dashboard')
            except Exception as e:
                messages.error(request, f'Error al crear la cuenta: {str(e)}')
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
    else:
        form = UserCreationForm()
    
    return render(request, 'user/registro.html', {'form': form})


def cerrar_sesion(request):
    """Cerrar sesión del usuario"""
    username = request.user.username if request.user.is_authenticated else 'Usuario'
    logout(request)
    messages.success(request, f'¡Hasta pronto, {username}! Has cerrado sesión exitosamente.')
    return redirect('public:index')


@login_required
def dashboard(request):
    """Dashboard del usuario con sus suscripciones y puntos"""
    perfil, created = PerfilUsuario.objects.get_or_create(user=request.user)
    if created:
        messages.info(request, 'Tu perfil ha sido creado exitosamente.')
    
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
    """
    PASO 1: Formulario inicial para seleccionar el plan
    Aquí el usuario ingresa su correo del servicio y nombre de usuario
    """
    plan = get_object_or_404(PlanSuscripcion, id=plan_id, activo=True)
    
    if request.method == 'POST':
        email_servicio = request.POST.get('email_servicio')
        usuario_servicio = request.POST.get('usuario_servicio')
        
        if not email_servicio or not usuario_servicio:
            messages.error(request, 'Por favor completa todos los campos.')
            return redirect('user:iniciar_suscripcion', plan_id=plan_id)
        
        # VERIFICAR QUE EL CORREO ESTÉ EN LA TABLA DE CORREOS VERIFICADOS
        correo_verificado = CorreoVerificado.objects.filter(
            correo=email_servicio,
            servicio=plan.servicio,
            activo=True
        ).exists()
        
        if not correo_verificado:
            messages.error(
                request,
                f'El correo {email_servicio} no está verificado para {plan.servicio.nombre}. '
                'Por favor contacta con un administrador.'
            )
            return redirect('user:iniciar_suscripcion', plan_id=plan_id)
        
        # Guardar los datos en la sesión y redirigir a la pasarela de pago
        request.session['email_servicio'] = email_servicio
        request.session['usuario_servicio'] = usuario_servicio
        request.session['plan_id'] = plan_id
        return redirect('user:pasarela_pago')
    
    context = {
        'plan': plan,
    }
    return render(request, 'user/iniciar_suscripcion.html', context)


@login_required
def pasarela_pago(request):
    """
    PASO 2: Pasarela de pago
    Formulario para ingresar datos de facturación y seleccionar método de pago
    """
    plan_id = request.session.get('plan_id')
    email_servicio = request.session.get('email_servicio')
    
    if not plan_id or not email_servicio:
        messages.error(request, 'Sesión expirada. Por favor, intenta nuevamente.')
        return redirect('public:catalogo')
    
    plan = get_object_or_404(PlanSuscripcion, id=plan_id, activo=True)
    perfil = request.user.perfil
    config = ConfiguracionRecompensa.objects.filter(activo=True).first()
    
    # Calcular puntos necesarios para pagar el total
    puntos_necesarios_total = 0
    if config:
        puntos_necesarios_total = int(plan.precio * config.puntos_por_peso)
    
    if request.method == 'POST':
        # Datos de facturación
        nombre_completo = request.POST.get('nombre_completo')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        correo = request.POST.get('correo')
        metodo_pago = request.POST.get('metodo_pago')
        
        # Pago con puntos
        usar_puntos = request.POST.get('usar_puntos') == 'on'
        puntos_a_usar = int(request.POST.get('puntos_a_usar', 0))
        
        # Validaciones
        if not all([nombre_completo, telefono, direccion, correo, metodo_pago]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('user:pasarela_pago')
        
        # Calcular montos
        monto_total = plan.precio
        valor_puntos = Decimal('0')
        puntos_usados = 0
        monto_pendiente = monto_total
        metodo_pago_final = metodo_pago
        metodo_pago_secundario = None
        
        if usar_puntos and puntos_a_usar > 0:
            # Verificar que tenga los puntos
            if puntos_a_usar > perfil.puntos_disponibles:
                messages.error(request, 'No tienes suficientes puntos disponibles.')
                return redirect('user:pasarela_pago')
            
            # Calcular valor de los puntos
            if config:
                valor_puntos = Decimal(puntos_a_usar) / Decimal(config.puntos_por_peso)
                puntos_usados = puntos_a_usar
                monto_pendiente = max(Decimal('0'), monto_total - valor_puntos)
                
                if monto_pendiente > 0:
                    # Pago mixto
                    metodo_pago_final = 'mixto'
                    metodo_pago_secundario = metodo_pago
                else:
                    # Pago solo con puntos
                    metodo_pago_final = 'puntos'
                    metodo_pago_secundario = None
        
        # Verificar si es primera compra
        es_primera = not Suscripcion.objects.filter(
            usuario=request.user,
            plan__servicio=plan.servicio
        ).exists()
        
        # Crear la suscripción
        suscripcion = Suscripcion.objects.create(
            usuario=request.user,
            plan=plan,
            fecha_inicio=timezone.now().date(),
            metodo_pago=metodo_pago_final,
            monto_pagado=monto_total,
            email_servicio=email_servicio,
            es_primera_compra=es_primera,
            estado='activa'  # Ahora se activa directamente
        )
        
        # Crear la factura
        factura = Factura.objects.create(
            suscripcion=suscripcion,
            nombre_completo=nombre_completo,
            telefono=telefono,
            direccion=direccion,
            correo=correo,
            metodo_pago=metodo_pago_final,
            monto_total=monto_total,
            puntos_usados=puntos_usados,
            valor_puntos=valor_puntos,
            monto_pendiente=monto_pendiente,
            metodo_pago_secundario=metodo_pago_secundario,
            pagado=True,
            fecha_pago=timezone.now()
        )
        
        # Descontar puntos si se usaron
        if puntos_usados > 0:
            perfil.canjear_puntos(
                puntos_usados,
                f"Pago de {plan.servicio.nombre} - {plan.nombre} (Factura #{factura.numero_factura})"
            )
        
        # Otorgar puntos de cashback (solo si no pagó 100% con puntos)
        if metodo_pago_final != 'puntos':
            puntos_cashback = plan.puntos_primera_compra if es_primera else plan.puntos_renovacion
            perfil.agregar_puntos(
                puntos_cashback,
                f"Cashback por {plan.servicio.nombre} - {plan.nombre}"
            )
            suscripcion.puntos_otorgados = puntos_cashback
            suscripcion.save()
        
        # Enviar confirmación por correo
        try:
            enviar_confirmacion_pago(factura, suscripcion, request.user)
        except Exception as e:
            messages.warning(request, f'Pago procesado pero no se pudo enviar el correo: {str(e)}')
        
        # Limpiar sesión
        del request.session['email_servicio']
        del request.session['plan_id']
        
        messages.success(
            request,
            f'¡Pago confirmado! Tu suscripción a {plan.servicio.nombre} está ahora activa. '
            f'Revisa tu correo para más detalles.'
        )
        return redirect('user:dashboard')
    
    context = {
        'plan': plan,
        'email_servicio': email_servicio,
        'perfil': perfil,
        'config': config,
        'puntos_necesarios_total': puntos_necesarios_total,
    }
    return render(request, 'user/pasarela_pago.html', context)


def enviar_confirmacion_pago(factura, suscripcion, usuario):
    """Enviar correo de confirmación de pago"""
    asunto = f'Confirmación de Compra - {suscripcion.plan.servicio.nombre}'
    
    mensaje = f"""
    Hola {factura.nombre_completo},
    
    ¡Tu suscripción ha sido confirmada exitosamente!
    
    DETALLES DE LA COMPRA:
    -----------------------
    Servicio: {suscripcion.plan.servicio.nombre}
    Plan: {suscripcion.plan.nombre}
    Precio: ${suscripcion.monto_pagado:,.2f} COP
    
    INFORMACIÓN DE FACTURACIÓN:
    -----------------------
    Número de Factura: {factura.numero_factura}
    Método de Pago: {factura.get_metodo_pago_display()}
    Fecha: {factura.fecha_pago.strftime('%d/%m/%Y %H:%M')}
    
    {f'Puntos Usados: {factura.puntos_usados}' if factura.puntos_usados > 0 else ''}
    {f'Valor Puntos: ${factura.valor_puntos:,.2f} COP' if factura.puntos_usados > 0 else ''}
    {f'Monto Pagado ({factura.get_metodo_pago_secundario_display()}): ${factura.monto_pendiente:,.2f} COP' if factura.monto_pendiente > 0 else ''}
    
    SUSCRIPCIÓN:
    -----------------------
    Email del Servicio: {suscripcion.email_servicio}
    Fecha de Inicio: {suscripcion.fecha_inicio.strftime('%d/%m/%Y')}
    Fecha de Vencimiento: {suscripcion.fecha_vencimiento.strftime('%d/%m/%Y')}
    {f'Puntos Ganados (Cashback): {suscripcion.puntos_otorgados}' if suscripcion.puntos_otorgados > 0 else ''}
    
    Gracias por confiar en StreamPoint.
    
    Saludos,
    El equipo de StreamPoint
    """
    
    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [factura.correo],
        fail_silently=False,
    )


@login_required
def renovar_suscripcion(request, suscripcion_id):
    """Renovar una suscripción existente"""
    suscripcion = get_object_or_404(
        Suscripcion,
        id=suscripcion_id,
        usuario=request.user
    )
    
    # Guardar datos en sesión y redirigir a pasarela de pago
    request.session['email_servicio'] = suscripcion.email_servicio
    request.session['plan_id'] = suscripcion.plan.id
    request.session['es_renovacion'] = True
    
    return redirect('user:pasarela_pago')


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


@login_required
def registrar_compra(request):
    """
    Formulario para que los usuarios registren sus compras manualmente.
    El admin las revisa y aprueba para otorgar puntos.
    """
    if request.method == 'POST':
        form = RegistroCompraForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            registro = form.save(commit=False)
            registro.usuario = request.user
            registro.save()
            
            messages.success(
                request,
                '¡Compra registrada exitosamente! '
                'El administrador la revisará pronto y te otorgará tus puntos.'
            )
            return redirect('user:mis_registros_compra')
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        # Pre-llenar el formulario si vienen parámetros en la URL
        initial_data = {}
        servicio_id = request.GET.get('servicio')
        plan_id = request.GET.get('plan')
        
        if servicio_id:
            try:
                from core_public.models import ServicioStreaming
                servicio = ServicioStreaming.objects.get(id=servicio_id)
                initial_data['servicio'] = servicio
            except:
                pass
        
        if plan_id:
            try:
                from core_public.models import PlanSuscripcion
                plan = PlanSuscripcion.objects.get(id=plan_id)
                initial_data['plan'] = plan
                if not servicio_id and plan.servicio:
                    initial_data['servicio'] = plan.servicio
                # Pre-llenar el monto con el precio del plan
                initial_data['monto_pagado'] = plan.precio
            except:
                pass
        
        form = RegistroCompraForm(initial=initial_data, user=request.user)
    
    context = {
        'form': form,
        'titulo': 'Registrar Compra'
    }
    return render(request, 'user/registrar_compra.html', context)


@login_required
def mis_registros_compra(request):
    """
    Listado de compras registradas por el usuario.
    """
    registros = RegistroCompra.objects.filter(usuario=request.user)
    
    context = {
        'registros': registros,
        'titulo': 'Mis Compras Registradas'
    }
    return render(request, 'user/mis_registros_compra.html', context)


@login_required
def detalle_registro_compra(request, registro_id):
    """
    Detalle de un registro de compra específico.
    """
    registro = get_object_or_404(
        RegistroCompra,
        id=registro_id,
        usuario=request.user
    )
    
    context = {
        'registro': registro,
        'titulo': 'Detalle de Compra'
    }
    return render(request, 'user/detalle_registro_compra.html', context)
