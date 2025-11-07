from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from core_public.models import PlanSuscripcion


class PerfilUsuario(models.Model):
    """Perfil extendido del usuario con sistema de puntos"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=15, blank=True)
    puntos_totales = models.IntegerField(default=0, help_text="Total de puntos acumulados históricamente")
    puntos_disponibles = models.IntegerField(default=0, help_text="Puntos disponibles para canjear")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Perfiles de Usuario"
    
    def __str__(self):
        return f"{self.user.username} - {self.puntos_disponibles} puntos"
    
    def agregar_puntos(self, cantidad, descripcion=""):
        """Agregar puntos al usuario"""
        self.puntos_totales += cantidad
        self.puntos_disponibles += cantidad
        self.save()
        
        # Registrar transacción
        TransaccionPuntos.objects.create(
            perfil=self,
            tipo='ganado',
            cantidad=cantidad,
            descripcion=descripcion
        )
    
    def canjear_puntos(self, cantidad, descripcion=""):
        """Canjear puntos (restar)"""
        if cantidad <= self.puntos_disponibles:
            self.puntos_disponibles -= cantidad
            self.save()
            
            # Registrar transacción
            TransaccionPuntos.objects.create(
                perfil=self,
                tipo='canjeado',
                cantidad=cantidad,
                descripcion=descripcion
            )
            return True
        return False


class Suscripcion(models.Model):
    """Suscripciones de usuarios a servicios de streaming"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente de validación'),
        ('activa', 'Activa'),
        ('vencida', 'Vencida'),
        ('cancelada', 'Cancelada'),
    ]
    
    METODO_PAGO_CHOICES = [
        ('tarjeta', 'Tarjeta de crédito/débito'),
        ('pse', 'PSE'),
        ('efectivo', 'Efectivo'),
        ('puntos', 'Canje de puntos'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suscripciones')
    plan = models.ForeignKey(PlanSuscripcion, on_delete=models.CASCADE)
    
    # Información de la compra
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    # Validación
    validada = models.BooleanField(default=False, help_text="¿La compra ha sido validada por un admin?")
    fecha_validacion = models.DateTimeField(null=True, blank=True)
    
    # Pago y puntos
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    puntos_otorgados = models.IntegerField(default=0, help_text="Puntos de cashback otorgados")
    es_primera_compra = models.BooleanField(default=False)
    
    # Información del servicio
    email_servicio = models.EmailField(help_text="Email usado en el servicio de streaming")
    notas = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Suscripciones"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.plan.servicio.nombre}"
    
    def save(self, *args, **kwargs):
        # Si es nueva suscripción, calcular fecha de vencimiento
        if not self.pk:
            self.fecha_vencimiento = self.fecha_inicio + timedelta(days=self.plan.get_duracion_dias())
    
        # Guardar primero para tener el ID
        super().save(*args, **kwargs)
    
        # LUEGO otorgar puntos (evita problemas de sincronización)
        if self.validada and self.puntos_otorgados == 0 and self.metodo_pago != 'puntos':
            puntos = self.plan.puntos_primera_compra if self.es_primera_compra else self.plan.puntos_renovacion
        
            self.usuario.perfil.agregar_puntos(
                puntos,
                f"Cashback por {self.plan.servicio.nombre} - {self.plan.nombre}"
            )
            self.puntos_otorgados = puntos
            # Guardar de nuevo solo si se otorgaron puntos
            super().save(update_fields=['puntos_otorgados'])
        
        super().save(*args, **kwargs)
    
    def esta_activa(self):
        """Verifica si la suscripción está activa"""
        return self.estado == 'activa' and self.fecha_vencimiento >= timezone.now().date()
    
    def dias_restantes(self):
        """Días restantes de la suscripción"""
        if self.fecha_vencimiento:
            delta = self.fecha_vencimiento - timezone.now().date()
            return max(0, delta.days)
        return 0


class TransaccionPuntos(models.Model):
    """Historial de transacciones de puntos"""
    TIPO_CHOICES = [
        ('ganado', 'Puntos ganados'),
        ('canjeado', 'Puntos canjeados'),
    ]
    
    perfil = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='transacciones')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cantidad = models.IntegerField()
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Transacciones de Puntos"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.perfil.user.username} - {self.tipo} {self.cantidad} pts"
