# ============================================
# core_user/management/commands/crear_perfiles.py
# Comando para crear perfiles a usuarios existentes
# ============================================
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core_user.models import PerfilUsuario


class Command(BaseCommand):
    help = 'Crea perfiles para todos los usuarios que no tengan uno'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando creación de perfiles...'))
        
        # Obtener todos los usuarios
        usuarios = User.objects.all()
        creados = 0
        existentes = 0
        
        for usuario in usuarios:
            perfil, created = PerfilUsuario.objects.get_or_create(user=usuario)
            if created:
                creados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Perfil creado para: {usuario.username}')
                )
            else:
                existentes += 1
                self.stdout.write(
                    self.style.WARNING(f'  Perfil ya existía para: {usuario.username}')
                )
        
        self.stdout.write(self.style.SUCCESS(f'\n¡Proceso completado!'))
        self.stdout.write(self.style.SUCCESS(f'Perfiles creados: {creados}'))
        self.stdout.write(self.style.SUCCESS(f'Perfiles existentes: {existentes}'))
        self.stdout.write(self.style.SUCCESS(f'Total de usuarios: {usuarios.count()}'))
