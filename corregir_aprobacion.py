import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StreamPoint.settings')
django.setup()

from core_user.models import RegistroCompra
from django.contrib.auth.models import User

# Obtener el registro y el admin
registro = RegistroCompra.objects.get(id=1)
admin = User.objects.filter(is_staff=True).first()

print(f'Registro ID: {registro.id}')
print(f'Usuario: {registro.usuario.username}')
print(f'Estado actual: {registro.estado}')
print(f'Puntos otorgados: {registro.puntos_otorgados}')
print(f'Puntos del usuario ANTES: {registro.usuario.perfil.puntos_disponibles}')

# Re-aprobar correctamente el registro
if admin:
    print(f'\nEjecutando aprobar() con admin: {admin.username}')
    registro.aprobar(admin, puntos=120)
    
    # Verificar después
    registro.refresh_from_db()
    registro.usuario.perfil.refresh_from_db()
    
    print(f'\nDespués de aprobar:')
    print(f'  Estado: {registro.estado}')
    print(f'  Fecha revisión: {registro.fecha_revision}')
    print(f'  Revisado por: {registro.revisado_por}')
    print(f'  Puntos del usuario: {registro.usuario.perfil.puntos_disponibles}')
    print(f'  Puntos totales: {registro.usuario.perfil.puntos_totales}')
else:
    print('ERROR: No hay usuarios admin')
