# ============================================
# core_user/templatetags/user_extras.py
# Template tags y filtros personalizados para usuarios
# ============================================
from django import template
from core_user.models import PerfilUsuario

register = template.Library()


@register.simple_tag
def get_perfil(user):
    """
    Obtiene o crea el perfil de un usuario de forma segura.
    Uso en templates: {% get_perfil user as perfil %}
    """
    if not user.is_authenticated:
        return None
    
    perfil, created = PerfilUsuario.objects.get_or_create(user=user)
    return perfil


@register.filter
def puntos_disponibles(user):
    """
    Obtiene los puntos disponibles de un usuario de forma segura.
    Uso en templates: {{ user|puntos_disponibles }}
    """
    if not user.is_authenticated:
        return 0
    
    perfil, created = PerfilUsuario.objects.get_or_create(user=user)
    return perfil.puntos_disponibles


@register.filter
def puntos_a_pesos(puntos):
    """
    Convierte puntos a pesos colombianos.
    10 puntos = 1 peso
    Uso en templates: {{ puntos|puntos_a_pesos }}
    """
    try:
        return int(puntos) // 10
    except (ValueError, TypeError):
        return 0


@register.filter
def pesos_a_puntos(pesos):
    """
    Convierte pesos colombianos a puntos.
    1 peso = 10 puntos
    Uso en templates: {{ precio|pesos_a_puntos }}
    """
    try:
        return int(float(pesos) * 10)
    except (ValueError, TypeError):
        return 0
