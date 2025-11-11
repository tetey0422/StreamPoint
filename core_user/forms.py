from django import forms
from .models import RegistroCompra
from core_public.models import ServicioStreaming, PlanSuscripcion


class RegistroCompraForm(forms.ModelForm):
    """
    Formulario para que los usuarios registren sus compras.
    """
    
    class Meta:
        model = RegistroCompra
        fields = [
            'nombre_completo',
            'correo',
            'nombre_usuario_app',
            'telefono',
            'servicio',
            'plan',
            'monto_pagado',
            'fecha_compra',
            'comprobante',
            'descripcion'
        ]
        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Juan Pérez'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tu@email.com'
            }),
            'nombre_usuario_app': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Usuario en Netflix, Spotify, etc.'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+57 300 123 4567'
            }),
            'servicio': forms.Select(attrs={
                'class': 'form-control'
            }),
            'plan': forms.Select(attrs={
                'class': 'form-control'
            }),
            'monto_pagado': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'fecha_compra': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'comprobante': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detalles adicionales sobre tu compra...'
            })
        }
        labels = {
            'nombre_completo': 'Nombre completo',
            'correo': 'Correo electrónico',
            'nombre_usuario_app': 'Usuario en la app del servicio',
            'telefono': 'Teléfono (opcional)',
            'servicio': 'Servicio de streaming',
            'plan': 'Plan adquirido (opcional)',
            'monto_pagado': 'Monto pagado ($)',
            'fecha_compra': 'Fecha de compra',
            'comprobante': 'Comprobante de pago (opcional)',
            'descripcion': 'Descripción adicional (opcional)'
        }
        help_texts = {
            'nombre_usuario_app': 'El nombre de usuario que utilizas en la plataforma (Netflix, Spotify, etc.)',
            'comprobante': 'Sube una captura de pantalla o foto del comprobante de pago',
            'plan': 'Si conoces el plan específico, selecciónalo. De lo contrario, déjalo vacío.'
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Pre-rellenar datos del usuario si está disponible
        if user and user.is_authenticated:
            if not self.instance.pk:  # Solo para nuevos registros
                self.initial['correo'] = user.email
                if hasattr(user, 'perfil'):
                    self.initial['telefono'] = user.perfil.telefono
                self.initial['nombre_completo'] = user.get_full_name() or user.username
        
        # Hacer el plan opcional
        self.fields['plan'].required = False
        self.fields['plan'].empty_label = "Selecciona un plan (opcional)"
        
        # Hacer campos opcionales
        self.fields['telefono'].required = False
        self.fields['comprobante'].required = False
        self.fields['descripcion'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        servicio = cleaned_data.get('servicio')
        plan = cleaned_data.get('plan')
        
        # Si se seleccionó un plan, verificar que pertenezca al servicio
        if plan and servicio and plan.servicio != servicio:
            raise forms.ValidationError(
                'El plan seleccionado no corresponde al servicio elegido.'
            )
        
        return cleaned_data
