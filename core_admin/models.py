from django.db import models
from core_public.models import ServicioStreaming
from django.contrib.auth.models import User


class CorreoVerificado(models.Model):
    """
    Tabla de correos verificados por el administrador.
    Solo usuarios con correos aquí guardados pueden suscribirse a servicios específicos.
    """
    correo = models.EmailField(help_text="Correo electrónico verificado")
    servicio = models.ForeignKey(
        ServicioStreaming,
        on_delete=models.CASCADE,
        related_name='correos_verificados',
        help_text="Servicio de streaming al que pertenece este correo"
    )
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    agregado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Administrador que agregó este correo"
    )
    activo = models.BooleanField(default=True, help_text="Si está activo para verificación")
    notas = models.TextField(blank=True, help_text="Notas adicionales")
    
    class Meta:
        verbose_name = "Correo Verificado"
        verbose_name_plural = "Correos Verificados"
        unique_together = ['correo', 'servicio']
        ordering = ['-fecha_agregado']
    
    def __str__(self):
        return f"{self.correo} - {self.servicio.nombre}"
