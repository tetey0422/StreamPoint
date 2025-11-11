import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StreamPoint.settings')
django.setup()

from core_user.models import RegistroCompra, PerfilUsuario, TransaccionPuntos
from django.contrib.auth.models import User

# Verificar usuario tetey
try:
    u = User.objects.get(username='tetey')
    print(f'Usuario: {u.username}')
    print(f'Puntos disponibles: {u.perfil.puntos_disponibles}')
    print(f'Puntos totales: {u.perfil.puntos_totales}')
    
    print('\n--- Registros de compra ---')
    for r in RegistroCompra.objects.filter(usuario=u):
        print(f'  ID: {r.id}')
        print(f'  Servicio: {r.servicio.nombre}')
        print(f'  Estado: {r.estado}')
        print(f'  Puntos otorgados: {r.puntos_otorgados}')
        print(f'  Fecha revisión: {r.fecha_revision}')
        print(f'  Revisado por: {r.revisado_por}')
        print()
    
    print('--- Transacciones de puntos ---')
    transacciones = TransaccionPuntos.objects.filter(perfil=u.perfil)
    if transacciones.exists():
        for t in transacciones:
            print(f'  {t.tipo}: {t.cantidad} pts - {t.descripcion} ({t.fecha})')
    else:
        print('  No hay transacciones registradas')
        
except User.DoesNotExist:
    print('Usuario tetey no existe')
