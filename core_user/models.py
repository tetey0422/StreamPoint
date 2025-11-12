from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from datetime import timedelta
from core_public.models import PlanSuscripcion
from decimal import Decimal
from PIL import Image
import io


def validate_file_size(value):
    """Valida que el archivo no supere los 5MB"""
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB en bytes
        raise ValidationError("El archivo no puede ser mayor a 5MB. Por favor, comprima la imagen o use un archivo más pequeño.")
    return value


def validate_file_content(value):
    """Valida el contenido real del archivo, no solo la extensión"""
    # Leer los primeros bytes para detectar el tipo MIME
    value.seek(0)
    header = value.read(512)
    value.seek(0)
    
    # Detectar tipo de archivo por magic numbers
    if header.startswith(b'%PDF'):
        # Es un PDF válido
        return value
    elif header.startswith(b'\xff\xd8\xff'):
        # Es JPEG - validar que sea imagen válida
        try:
            img = Image.open(value)
            img.verify()
            value.seek(0)
            return value
        except Exception:
            raise ValidationError("El archivo JPEG está corrupto o no es una imagen válida")
    elif header.startswith(b'\x89PNG\r\n\x1a\n'):
        # Es PNG - validar que sea imagen válida
        try:
            img = Image.open(value)
            img.verify()
            value.seek(0)
            return value
        except Exception:
            raise ValidationError("El archivo PNG está corrupto o no es una imagen válida")
    elif header.startswith(b'RIFF') and b'WEBP' in header[:20]:
        # Es WEBP - validar que sea imagen válida
        try:
            img = Image.open(value)
            img.verify()
            value.seek(0)
            return value
        except Exception:
            raise ValidationError("El archivo WEBP está corrupto o no es una imagen válida")
    else:
        raise ValidationError("Tipo de archivo no permitido. Solo se aceptan PDF, JPG, PNG o WEBP válidos.")


def validate_file_size_and_content(value):
    """Validador combinado de tamaño y contenido"""
    validate_file_size(value)
    validate_file_content(value)
    return value


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
    
    def usar_puntos(self, cantidad, descripcion=""):
        """Alias de canjear_puntos para usar puntos"""
        return self.canjear_puntos(cantidad, descripcion)


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
    usuario_servicio = models.CharField(max_length=200, blank=True, help_text="Nombre de usuario en el servicio (Netflix, Spotify, etc.)")
    notas = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Suscripciones"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['usuario', 'estado']),
            models.Index(fields=['fecha_vencimiento']),
            models.Index(fields=['-fecha_creacion']),
            models.Index(fields=['validada', 'estado']),
        ]
    
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
            
            # Crear o obtener perfil de forma segura
            perfil, created = PerfilUsuario.objects.get_or_create(user=self.usuario)
            perfil.agregar_puntos(
                puntos,
                f"Cashback por {self.plan.servicio.nombre} - {self.plan.nombre}"
            )
            self.puntos_otorgados = puntos
            # Guardar de nuevo solo si se otorgaron puntos
            super().save(update_fields=['puntos_otorgados'])
        
    
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


class Factura(models.Model):
    """
    Información de facturación para cada compra de suscripción.
    """
    METODO_PAGO_CHOICES = [
        ('tarjeta', 'Tarjeta de crédito/débito'),
        ('pse', 'PSE'),
        ('efectivo', 'Efectivo'),
        ('puntos', 'Puntos'),
        ('mixto', 'Mixto (Puntos + Otro método)'),
    ]
    
    # Relación con suscripción
    suscripcion = models.OneToOneField(
        'Suscripcion',
        on_delete=models.CASCADE,
        related_name='factura',
        null=True,
        blank=True
    )
    
    # Información del comprador
    nombre_completo = models.CharField(max_length=200, help_text="Nombre completo del comprador")
    telefono = models.CharField(max_length=15, help_text="Teléfono de contacto")
    direccion = models.TextField(help_text="Dirección de facturación")
    correo = models.EmailField(help_text="Correo electrónico para confirmación")
    
    # Información de pago
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto total de la compra")
    
    # Pago con puntos
    puntos_usados = models.IntegerField(default=0, help_text="Puntos utilizados en el pago")
    valor_puntos = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Valor en pesos de los puntos usados"
    )
    monto_pendiente = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Monto restante a pagar por otro método"
    )
    metodo_pago_secundario = models.CharField(
        max_length=20,
        choices=METODO_PAGO_CHOICES,
        blank=True,
        null=True,
        help_text="Método de pago para el monto restante (pago mixto)"
    )
    
    # Control
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    pagado = models.BooleanField(default=False, help_text="Si el pago ha sido confirmado")
    fecha_pago = models.DateTimeField(null=True, blank=True)
    numero_factura = models.CharField(max_length=50, unique=True, blank=True)
    
    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Factura #{self.numero_factura} - {self.nombre_completo}"
    
    def save(self, *args, **kwargs):
        # Generar número de factura automáticamente
        if not self.numero_factura:
            from django.utils.crypto import get_random_string
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            random_str = get_random_string(4, allowed_chars='0123456789')
            self.numero_factura = f"FAC-{timestamp}-{random_str}"
        super().save(*args, **kwargs)


class RegistroCompra(models.Model):
    """
    Registro manual de compras realizadas por usuarios.
    El admin revisa y aprueba estas compras para otorgar puntos.
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente de revisión'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    
    # Información del usuario
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='registros_compra',
        help_text="Usuario que registra la compra"
    )
    nombre_completo = models.CharField(max_length=200, help_text="Nombre completo")
    correo = models.EmailField(help_text="Correo electrónico")
    nombre_usuario_app = models.CharField(
        max_length=200,
        help_text="Nombre de usuario en la app del servicio (Netflix, Spotify, etc.)"
    )
    telefono = models.CharField(max_length=15, blank=True, help_text="Teléfono de contacto")
    
    # Información de la compra
    servicio = models.ForeignKey(
        'core_public.ServicioStreaming',
        on_delete=models.CASCADE,
        related_name='registros_compra',
        help_text="Servicio de streaming adquirido"
    )
    plan = models.ForeignKey(
        'core_public.PlanSuscripcion',
        on_delete=models.CASCADE,
        related_name='registros_compra',
        null=True,
        blank=True,
        help_text="Plan específico (opcional)"
    )
    monto_pagado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Monto pagado por la compra"
    )
    fecha_compra = models.DateField(help_text="Fecha en que realizó la compra")
    comprobante = models.FileField(
        upload_to='comprobantes/%Y/%m/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'webp'],
                message="Solo se permiten archivos PDF, JPG, JPEG, PNG o WEBP"
            ),
            validate_file_size_and_content
        ],
        help_text="Comprobante de pago en formato PDF o imagen (JPG, PNG). Máximo 5MB"
    )
    descripcion = models.TextField(
        blank=True,
        help_text="Detalles adicionales sobre la compra"
    )
    
    # Control y estado
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    es_primera_compra = models.BooleanField(
        default=False,
        help_text="Si es la primera compra del usuario en este servicio"
    )
    puntos_sugeridos = models.IntegerField(
        default=0,
        help_text="Puntos calculados automáticamente según el plan"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)
    revisado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='compras_revisadas',
        help_text="Admin que revisó la compra"
    )
    puntos_otorgados = models.IntegerField(
        default=0,
        help_text="Puntos otorgados al aprobar"
    )
    notas_admin = models.TextField(
        blank=True,
        help_text="Notas del administrador"
    )
    
    class Meta:
        verbose_name = "Registro de Compra"
        verbose_name_plural = "Registros de Compras"
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['usuario', 'estado']),
            models.Index(fields=['estado', '-fecha_registro']),
            models.Index(fields=['servicio', 'usuario']),
            models.Index(fields=['-fecha_registro']),
        ]
    
    def __str__(self):
        return f"{self.usuario.username} - {self.servicio.nombre} - {self.get_estado_display()}"
    
    def save(self, *args, **kwargs):
        """
        Al guardar, detecta automáticamente si es primera compra
        y calcula los puntos sugeridos según el plan
        """
        if not self.pk:  # Solo en la creación
            # Detectar si es primera compra en este servicio
            compras_anteriores = RegistroCompra.objects.filter(
                usuario=self.usuario,
                servicio=self.servicio,
                estado='aprobada'
            ).exists()
            
            # También revisar suscripciones anteriores
            suscripciones_anteriores = Suscripcion.objects.filter(
                usuario=self.usuario,
                plan__servicio=self.servicio,
                validada=True
            ).exists()
            
            self.es_primera_compra = not (compras_anteriores or suscripciones_anteriores)
            
            # Calcular puntos sugeridos basándose en el monto pagado
            from core_public.models import ConfiguracionRecompensa
            try:
                config = ConfiguracionRecompensa.objects.filter(activo=True).first()
                if config and self.monto_pagado:
                    # Calcular puntos basándose en el monto pagado
                    # Ejemplo: $100,000 × 10 puntos/peso = 1,000,000 puntos
                    self.puntos_sugeridos = int(self.monto_pagado * config.puntos_por_peso)
                else:
                    # Fallback: usar valores del plan o por defecto
                    if self.plan:
                        if self.es_primera_compra:
                            self.puntos_sugeridos = self.plan.puntos_primera_compra
                        else:
                            self.puntos_sugeridos = self.plan.puntos_renovacion
                    else:
                        self.puntos_sugeridos = 100 if self.es_primera_compra else 50
            except:
                # Valores por defecto si no hay configuración
                self.puntos_sugeridos = 100 if self.es_primera_compra else 50
        
        super().save(*args, **kwargs)
    
    def calcular_puntos_automaticos(self):
        """
        Calcula los puntos que deberían otorgarse automáticamente
        basándose en el monto pagado y la configuración de puntos por peso.
        """
        from core_public.models import ConfiguracionRecompensa
        
        try:
            config = ConfiguracionRecompensa.objects.filter(activo=True).first()
            if config and self.monto_pagado:
                # Calcular puntos basándose en el monto pagado
                # Ejemplo: $100,000 × 10 puntos/peso = 1,000,000 puntos
                puntos_calculados = int(self.monto_pagado * config.puntos_por_peso)
                return puntos_calculados
        except:
            pass
        
        # Fallback: Si hay plan, usar sus valores fijos
        if self.plan:
            if self.es_primera_compra:
                return self.plan.puntos_primera_compra
            else:
                return self.plan.puntos_renovacion
        
        # Valores por defecto
        return 100 if self.es_primera_compra else 50
    
    def aprobar(self, admin_user, puntos=None):
        """
        Aprobar la compra y otorgar puntos.
        Si no se especifican puntos, usa los puntos sugeridos automáticamente.
        """
        # Si no se especifican puntos, usar los sugeridos
        if puntos is None:
            puntos = self.puntos_sugeridos if self.puntos_sugeridos > 0 else self.calcular_puntos_automaticos()
        
        self.estado = 'aprobada'
        self.fecha_revision = timezone.now()
        self.revisado_por = admin_user
        self.puntos_otorgados = puntos
        self.save()
        
        # Otorgar puntos al usuario
        perfil, created = PerfilUsuario.objects.get_or_create(user=self.usuario)
        tipo_compra = "Primera compra" if self.es_primera_compra else "Renovación"
        perfil.agregar_puntos(
            puntos,
            f"{tipo_compra} aprobada - {self.servicio.nombre}"
        )
    
    def rechazar(self, admin_user, motivo=""):
        """Rechazar la compra"""
        self.estado = 'rechazada'
        self.fecha_revision = timezone.now()
        self.revisado_por = admin_user
        if motivo:
            self.notas_admin = motivo
        self.save()
