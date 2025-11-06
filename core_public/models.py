from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class CategoriaStreaming(models.Model):
    """Categorías: Películas/Series, Música, Gaming, etc."""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=50, blank=True, help_text="Clase de ícono CSS (ej: fa-film)")
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Categorías de Streaming"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class ServicioStreaming(models.Model):
    """Servicios como Netflix, Spotify, Disney+, etc."""
    nombre = models.CharField(max_length=100, unique=True)
    categoria = models.ForeignKey(CategoriaStreaming, on_delete=models.CASCADE, related_name='servicios')
    logo_url = models.URLField(blank=True, help_text="URL del logo del servicio")
    descripcion = models.TextField()
    sitio_web = models.URLField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Servicios de Streaming"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class PlanSuscripcion(models.Model):
    """Planes de suscripción para cada servicio"""
    DURACION_CHOICES = [
        ('mensual', 'Mensual'),
        ('trimestral', 'Trimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
    ]
    
    servicio = models.ForeignKey(ServicioStreaming, on_delete=models.CASCADE, related_name='planes')
    nombre = models.CharField(max_length=100, help_text="Ej: Básico, Premium, Familiar")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.CharField(max_length=20, choices=DURACION_CHOICES, default='mensual')
    caracteristicas = models.JSONField(default=list, help_text="Lista de características del plan")
    puntos_primera_compra = models.IntegerField(default=100, help_text="Puntos por primera compra")
    puntos_renovacion = models.IntegerField(default=50, help_text="Puntos por cada renovación")
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Planes de Suscripción"
        ordering = ['servicio', 'precio']
    
    def __str__(self):
        return f"{self.servicio.nombre} - {self.nombre}"
    
    def get_duracion_dias(self):
        """Retorna la duración en días"""
        duraciones = {
            'mensual': 30,
            'trimestral': 90,
            'semestral': 180,
            'anual': 365,
        }
        return duraciones.get(self.duracion, 30)


class ConfiguracionRecompensa(models.Model):
    """Configuración del sistema de puntos (cashback)"""
    puntos_por_peso = models.IntegerField(default=10, help_text="Puntos necesarios por cada peso COP")
    puntos_minimos_canje = models.IntegerField(default=500, help_text="Mínimo de puntos para canjear")
    activo = models.BooleanField(default=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Configuración de Recompensas"
    
    def __str__(self):
        return f"Config: {self.puntos_por_peso} puntos = $1 COP"