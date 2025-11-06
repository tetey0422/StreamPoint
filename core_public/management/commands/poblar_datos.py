# Crear estructura de directorios:
# core_public/management/__init__.py (vacío)
# core_public/management/commands/__init__.py (vacío)
# core_public/management/commands/poblar_datos.py (este archivo)

from django.core.management.base import BaseCommand
from core_public.models import (
    CategoriaStreaming, ServicioStreaming, PlanSuscripcion,
    ConfiguracionRecompensa
)


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de ejemplo para StreamPoint'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando población de datos...'))

        # Crear configuración de recompensas (cashback)
        config, created = ConfiguracionRecompensa.objects.get_or_create(
            activo=True,
            defaults={
                'puntos_por_peso': 10,
                'puntos_minimos_canje': 500
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ Configuración de recompensas creada'))

        # Crear Categorías
        categorias_data = [
            {'nombre': 'Películas y Series', 'descripcion': 'Contenido de video on-demand', 'icono': 'fa-film'},
            {'nombre': 'Música', 'descripcion': 'Streaming de música y podcasts', 'icono': 'fa-music'},
            {'nombre': 'Gaming', 'descripcion': 'Servicios de juegos y cloud gaming', 'icono': 'fa-gamepad'},
        ]

        categorias = {}
        for cat_data in categorias_data:
            cat, created = CategoriaStreaming.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults=cat_data
            )
            categorias[cat_data['nombre']] = cat
            self.stdout.write(self.style.SUCCESS(f'✓ Categoría: {cat.nombre}'))

        # Crear Servicios de Streaming
        servicios_data = [
            # Películas y Series
            {
                'nombre': 'Netflix',
                'categoria': categorias['Películas y Series'],
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg',
                'descripcion': 'El servicio de streaming líder mundial con miles de películas, series y documentales.',
                'sitio_web': 'https://www.netflix.com',
            },
            {
                'nombre': 'Disney+',
                'categoria': categorias['Películas y Series'],
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/3/3e/Disney%2B_logo.svg',
                'descripcion': 'Todo el contenido de Disney, Pixar, Marvel, Star Wars y National Geographic.',
                'sitio_web': 'https://www.disneyplus.com',
            },
            {
                'nombre': 'HBO Max',
                'categoria': categorias['Películas y Series'],
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/1/17/HBO_Max_Logo.svg',
                'descripcion': 'Series premium, películas de Warner Bros y contenido exclusivo.',
                'sitio_web': 'https://www.hbomax.com',
            },
            {
                'nombre': 'Amazon Prime Video',
                'categoria': categorias['Películas y Series'],
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/f/f1/Prime_Video.png',
                'descripcion': 'Películas, series originales y contenido exclusivo de Amazon.',
                'sitio_web': 'https://www.primevideo.com',
            },
            {
                'nombre': 'Star+',
                'categoria': categorias['Películas y Series'],
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/7/71/Star%2B_logo.svg',
                'descripcion': 'Contenido de entretenimiento general, deportes y series exclusivas.',
                'sitio_web': 'https://www.starplus.com',
            },
            {
                'nombre': 'Paramount+',
                'categoria': categorias['Películas y Series'],
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/a/a5/Paramount_Plus.svg',
                'descripcion': 'Películas y series de Paramount, MTV, Nickelodeon y más.',
                'sitio_web': 'https://www.paramountplus.com',
            },
            # Música
            {
                'nombre': 'Spotify',
                'categoria': categorias['Música'],
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg',
                'descripcion': 'Millones de canciones y podcasts. El líder en streaming de música.',
                'sitio_web': 'https://www.spotify.com',
            },
            {
                'nombre': 'Apple Music',
                'categoria': categorias['Música'],
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/5/5f/Apple_Music_icon.svg',
                'descripcion': 'Música sin anuncios, contenido exclusivo y radio en vivo.',
                'sitio_web': 'https://www.apple.com/music',
            },
            {
                'nombre': 'YouTube Music',
                'categoria': categorias['Música'],
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/6/6a/Youtube_Music_icon.svg',
                'descripcion': 'Música, videos musicales y contenido exclusivo de YouTube.',
                'sitio_web': 'https://music.youtube.com',
            },
            # Gaming
            {
                'nombre': 'Xbox Game Pass',
                'categoria': categorias['Gaming'],
                'logo_url': 'https://upload.wikimedia.org/wikipedia/commons/b/bc/Xbox_Game_Pass_logo_%282020%29.svg',
                'descripcion': 'Acceso a cientos de juegos de alta calidad en consola, PC y nube.',
                'sitio_web': 'https://www.xbox.com/gamepass',
            },
        ]

        servicios = {}
        for serv_data in servicios_data:
            serv, created = ServicioStreaming.objects.get_or_create(
                nombre=serv_data['nombre'],
                defaults=serv_data
            )
            servicios[serv_data['nombre']] = serv
            self.stdout.write(self.style.SUCCESS(f'✓ Servicio: {serv.nombre}'))

        # Crear Planes de Suscripción
        planes_data = [
            # Netflix
            {'servicio': 'Netflix', 'nombre': 'Básico', 'precio': 16900, 'duracion': 'mensual',
             'caracteristicas': ['1 pantalla', 'Calidad SD', 'Descargas en 1 dispositivo'],
             'puntos_primera_compra': 150, 'puntos_renovacion': 75},
            {'servicio': 'Netflix', 'nombre': 'Estándar', 'precio': 32900, 'duracion': 'mensual',
             'caracteristicas': ['2 pantallas simultáneas', 'Calidad HD', 'Descargas en 2 dispositivos'],
             'puntos_primera_compra': 200, 'puntos_renovacion': 100},
            {'servicio': 'Netflix', 'nombre': 'Premium', 'precio': 44900, 'duracion': 'mensual',
             'caracteristicas': ['4 pantallas simultáneas', 'Calidad 4K+HDR', 'Descargas en 6 dispositivos'],
             'puntos_primera_compra': 250, 'puntos_renovacion': 125},
            
            # Disney+
            {'servicio': 'Disney+', 'nombre': 'Mensual', 'precio': 20900, 'duracion': 'mensual',
             'caracteristicas': ['Streaming ilimitado', 'Calidad 4K', '4 pantallas simultáneas'],
             'puntos_primera_compra': 150, 'puntos_renovacion': 75},
            {'servicio': 'Disney+', 'nombre': 'Anual', 'precio': 189900, 'duracion': 'anual',
             'caracteristicas': ['Streaming ilimitado', 'Calidad 4K', 'Ahorra 25%'],
             'puntos_primera_compra': 500, 'puntos_renovacion': 250},
            
            # HBO Max
            {'servicio': 'HBO Max', 'nombre': 'Mensual', 'precio': 19900, 'duracion': 'mensual',
             'caracteristicas': ['Todo el catálogo', 'Calidad 4K', '3 perfiles'],
             'puntos_primera_compra': 150, 'puntos_renovacion': 75},
            
            # Amazon Prime Video
            {'servicio': 'Amazon Prime Video', 'nombre': 'Mensual', 'precio': 18900, 'duracion': 'mensual',
             'caracteristicas': ['Streaming ilimitado', 'Contenido original', 'Incluye Prime'],
             'puntos_primera_compra': 150, 'puntos_renovacion': 75},
            
            # Star+
            {'servicio': 'Star+', 'nombre': 'Mensual', 'precio': 16900, 'duracion': 'mensual',
             'caracteristicas': ['Series y películas', 'Deportes en vivo', 'Contenido exclusivo'],
             'puntos_primera_compra': 150, 'puntos_renovacion': 75},
            
            # Paramount+
            {'servicio': 'Paramount+', 'nombre': 'Mensual', 'precio': 12900, 'duracion': 'mensual',
             'caracteristicas': ['Miles de películas', 'Series originales', 'TV en vivo'],
             'puntos_primera_compra': 120, 'puntos_renovacion': 60},
            
            # Spotify
            {'servicio': 'Spotify', 'nombre': 'Premium Individual', 'precio': 10900, 'duracion': 'mensual',
             'caracteristicas': ['Sin anuncios', 'Descarga música', 'Calidad alta'],
             'puntos_primera_compra': 120, 'puntos_renovacion': 60},
            {'servicio': 'Spotify', 'nombre': 'Premium Familiar', 'precio': 18900, 'duracion': 'mensual',
             'caracteristicas': ['Hasta 6 cuentas', 'Control parental', 'Mismo domicilio'],
             'puntos_primera_compra': 150, 'puntos_renovacion': 75},
            
            # Apple Music
            {'servicio': 'Apple Music', 'nombre': 'Individual', 'precio': 10900, 'duracion': 'mensual',
             'caracteristicas': ['90 millones de canciones', 'Sin anuncios', 'Audio espacial'],
             'puntos_primera_compra': 120, 'puntos_renovacion': 60},
            
            # YouTube Music
            {'servicio': 'YouTube Music', 'nombre': 'Premium', 'precio': 11900, 'duracion': 'mensual',
             'caracteristicas': ['Sin anuncios', 'Reproducción en segundo plano', 'Descargas'],
             'puntos_primera_compra': 120, 'puntos_renovacion': 60},
            
            # Xbox Game Pass
            {'servicio': 'Xbox Game Pass', 'nombre': 'Ultimate', 'precio': 34900, 'duracion': 'mensual',
             'caracteristicas': ['PC + Consola + Nube', 'Cientos de juegos', 'Nuevos lanzamientos'],
             'puntos_primera_compra': 200, 'puntos_renovacion': 100},
        ]

        for plan_data in planes_data:
            servicio_nombre = plan_data.pop('servicio')
            plan, created = PlanSuscripcion.objects.get_or_create(
                servicio=servicios[servicio_nombre],
                nombre=plan_data['nombre'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Plan: {servicio_nombre} - {plan.nombre}'))

        self.stdout.write(self.style.SUCCESS('\n¡Datos poblados exitosamente!'))
        self.stdout.write(self.style.SUCCESS(f'Total de servicios: {ServicioStreaming.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total de planes: {PlanSuscripcion.objects.count()}'))