from django import forms
from django.core.validators import RegexValidator
from .models import RegistroCompra
from core_public.models import ServicioStreaming, PlanSuscripcion
import re


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
                'placeholder': 'Ej: Juan Pérez',
                'required': 'required'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tu@email.com',
                'required': 'required',
                'pattern': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            }),
            'nombre_usuario_app': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Usuario en Netflix, Spotify, etc.',
                'required': 'required'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+57 300 123 4567',
                'required': 'required',
                'pattern': r'[\+]?[0-9\s\(\)]{7,20}'
            }),
            'servicio': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'plan': forms.Select(attrs={
                'class': 'form-control'
            }),
            'monto_pagado': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'required': 'required',
                'min': '0.01',
                'readonly': 'readonly'
            }),
            'fecha_compra': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': 'required'
            }),
            'comprobante': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf',
                'required': 'required'
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
            'telefono': 'Teléfono',
            'servicio': 'Servicio de streaming',
            'plan': 'Plan adquirido (opcional)',
            'monto_pagado': 'Monto a pagar ($)',
            'fecha_compra': 'Fecha de compra',
            'comprobante': 'Comprobante de pago',
            'descripcion': 'Descripción adicional (opcional)'
        }
        help_texts = {
            'nombre_usuario_app': 'El nombre de usuario que utilizas en la plataforma (Netflix, Spotify, etc.)',
            'comprobante': 'Sube una captura de pantalla o foto del comprobante de pago (OBLIGATORIO)',
            'plan': 'Si conoces el plan específico, selecciónalo. De lo contrario, déjalo vacío.',
            'correo': 'Ingresa un correo electrónico válido',
            'telefono': 'Ingresa un número de teléfono válido (Ej: +57 300 123 4567 o 3001234567)',
            'monto_pagado': 'El monto se actualiza automáticamente según el plan seleccionado'
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        pagar_con_puntos = kwargs.pop('pagar_con_puntos', False)
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
        self.fields['descripcion'].required = False
        
        # Si es pago con puntos, configuraciones especiales
        if pagar_con_puntos:
            # Comprobante NO es necesario
            self.fields['comprobante'].required = False
            self.fields['comprobante'].widget.attrs.pop('required', None)
            self.fields['comprobante'].help_text = 'No es necesario subir comprobante para pagos con puntos'
            
            # Fecha automática (fecha actual)
            from datetime import date
            self.initial['fecha_compra'] = date.today()
            self.fields['fecha_compra'].widget.attrs['readonly'] = 'readonly'
            self.fields['fecha_compra'].widget.attrs.pop('required', None)
            self.fields['fecha_compra'].required = False
            self.fields['fecha_compra'].help_text = 'La fecha se establece automáticamente al momento del pago'
        else:
            # Hacer el comprobante OBLIGATORIO para pagos normales
            self.fields['comprobante'].required = True
        
        # Configurar validaciones de correo y teléfono
        self.fields['correo'].required = True
        self.fields['telefono'].required = True
    
    def clean_correo(self):
        """Validar que el correo tenga formato válido"""
        correo = self.cleaned_data.get('correo')
        if correo:
            # Validar formato de correo electrónico
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, correo):
                raise forms.ValidationError('Ingresa un correo electrónico válido.')
        return correo
    
    def clean_telefono(self):
        """Validar que el teléfono tenga formato válido"""
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Verificar que no contenga caracteres inválidos como signos negativos
            if '-' in telefono.replace(' ', '').replace('(', '').replace(')', ''):
                raise forms.ValidationError(
                    'El número de teléfono no puede contener el signo menos. '
                    'Usa el signo + para códigos de país. Ejemplo: +57 300 123 4567'
                )
            
            # Eliminar espacios, guiones (entre números) y paréntesis para validación
            telefono_limpio = re.sub(r'[\s\(\)]', '', telefono)
            
            # Validar que contenga solo números y opcionalmente el símbolo + al inicio
            if not re.match(r'^\+?[0-9]{7,15}$', telefono_limpio):
                raise forms.ValidationError(
                    'Ingresa un número de teléfono válido. '
                    'Debe contener entre 7 y 15 dígitos. '
                    'Ejemplos: +57 300 123 4567 o 3001234567'
                )
        return telefono
    
    def clean_comprobante(self):
        """Validar que el comprobante sea una imagen o PDF (solo si es requerido)"""
        comprobante = self.cleaned_data.get('comprobante')
        
        # Si el campo no es requerido y no se subió archivo, retornar None
        if not self.fields['comprobante'].required and not comprobante:
            return None
            
        if comprobante:
            # Validar tamaño del archivo (máximo 5MB)
            if comprobante.size > 5 * 1024 * 1024:
                raise forms.ValidationError('El archivo no debe superar los 5MB.')
            
            # Validar tipo de archivo
            archivo_nombre = comprobante.name.lower()
            extensiones_validas = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.webp']
            
            if not any(archivo_nombre.endswith(ext) for ext in extensiones_validas):
                raise forms.ValidationError(
                    'Solo se permiten archivos de imagen (JPG, PNG, GIF, WEBP) o PDF.'
                )
        elif self.fields['comprobante'].required:
            raise forms.ValidationError('El comprobante de pago es obligatorio.')
            
        return comprobante
    
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
