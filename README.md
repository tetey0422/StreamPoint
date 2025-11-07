# 🎬 StreamPoint

**Sistema de Gestión de Suscripciones de Streaming con Recompensas**

StreamPoint es una plataforma web desarrollada en Django que permite a los usuarios gestionar sus suscripciones a servicios de streaming de manera legal y segura, mientras ganan puntos por cada compra y renovación que pueden canjear por nuevas suscripciones.

![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Comandos Útiles](#-comandos-útiles)
- [API y Endpoints](#-api-y-endpoints)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## ✨ Características

### 🎯 Funcionalidades Principales

- **Sistema de Autenticación Completo**
  - Registro de usuarios con validación de contraseñas seguras
  - Inicio de sesión y cierre de sesión
  - Creación automática de perfiles de usuario

- **Gestión de Suscripciones**
  - Catálogo de servicios de streaming (Netflix, Spotify, Disney+, etc.)
  - Múltiples planes por servicio (Mensual, Anual, Familiar)
  - Estados de suscripción: Pendiente, Activa, Cancelada, Vencida
  - Notificaciones de vencimiento

- **Sistema de Puntos y Recompensas** ⭐
  - Gana puntos con cada compra inicial
  - Puntos adicionales por renovaciones
  - Conversión: 10 puntos = $1 COP
  - Canje de puntos por suscripciones gratuitas

- **Panel de Administración**
  - Dashboard con estadísticas en tiempo real
  - Validación manual de suscripciones
  - Gestión de puntos de usuarios
  - Configuración de recompensas
  - Reportes y analíticas

- **Interfaz de Usuario Moderna**
  - Diseño responsive con Bootstrap 5.3.0
  - Animaciones y transiciones suaves
  - Iconos con Font Awesome 6.4.0
  - Gradientes y efectos visuales atractivos

## 🛠️ Tecnologías

### Backend
- **Django 5.2.7** - Framework web de alto nivel
- **Python 3.13.7** - Lenguaje de programación
- **SQLite** - Base de datos (puede cambiarse a PostgreSQL/MySQL)

### Frontend
- **Bootstrap 5.3.0** - Framework CSS
- **Font Awesome 6.4.0** - Biblioteca de iconos
- **JavaScript (Vanilla)** - Interactividad del cliente
- **CSS3** - Estilos personalizados con variables CSS

### Herramientas de Desarrollo
- **Git** - Control de versiones
- **VSCode** - Editor recomendado

## 📦 Instalación

### Requisitos Previos

- Python 3.13 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tetey0422/StreamPoint.git
cd StreamPoint
```

2. **Crear entorno virtual**
```bash
# Windows
python -m venv env
env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crear superusuario**
```bash
python manage.py createsuperuser
```

6. **Poblar datos de prueba (opcional)**
```bash
python manage.py poblar_datos
```

7. **Crear perfiles para usuarios existentes (si es necesario)**
```bash
python manage.py crear_perfiles
```

8. **Iniciar servidor de desarrollo**
```bash
python manage.py runserver
```

9. **Acceder a la aplicación**
- Frontend: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## ⚙️ Configuración

### Variables de Entorno (Opcional)

Puedes crear un archivo `.env` en la raíz del proyecto:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Configuración de la Base de Datos

Para producción, se recomienda usar PostgreSQL:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'streampoint_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚀 Uso

### Para Usuarios

1. **Registro**: Crea una cuenta desde `/user/registro/`
2. **Explorar Catálogo**: Navega por los servicios disponibles
3. **Seleccionar Plan**: Elige el plan que más te convenga
4. **Comprar**: Realiza la compra (en desarrollo, actualmente manual)
5. **Acumular Puntos**: Recibe puntos automáticamente
6. **Canjear**: Usa tus puntos para obtener suscripciones gratis

### Para Administradores

1. **Acceder al Admin**: http://127.0.0.1:8000/admin/
2. **Dashboard**: http://127.0.0.1:8000/admin/dashboard/
3. **Validar Suscripciones**: Aprobar compras pendientes
4. **Gestionar Puntos**: Asignar o quitar puntos manualmente
5. **Configurar Recompensas**: Ajustar el sistema de puntos
6. **Ver Reportes**: Analizar estadísticas del sistema

## 📁 Estructura del Proyecto

```
StreamPoint/
│
├── StreamPoint/              # Configuración principal del proyecto
│   ├── __init__.py
│   ├── settings.py          # Configuración de Django
│   ├── urls.py              # URLs principales
│   ├── wsgi.py
│   └── asgi.py
│
├── core_public/              # App pública (catálogo, servicios)
│   ├── models.py            # Servicio, PlanSuscripcion, Categoría
│   ├── views.py             # Vistas públicas
│   ├── urls.py
│   ├── templates/public/
│   │   ├── index.html       # Página principal
│   │   ├── catalogo.html    # Catálogo de servicios
│   │   └── detalle_servicio.html
│   └── management/commands/
│       └── poblar_datos.py  # Comando para datos de prueba
│
├── core_user/                # App de usuarios
│   ├── models.py            # PerfilUsuario, Suscripcion
│   ├── views.py             # Login, registro, dashboard
│   ├── signals.py           # Señales para crear perfiles
│   ├── urls.py
│   ├── templates/user/
│   │   ├── login.html
│   │   ├── registro.html
│   │   ├── dashboard.html
│   │   └── ...
│   ├── templatetags/
│   │   └── user_extras.py   # Filtros personalizados
│   └── management/commands/
│       └── crear_perfiles.py
│
├── core_admin/               # App de administración
│   ├── views.py             # Dashboard admin, validaciones
│   ├── urls.py
│   └── templates/admin_custom/
│       ├── dashboard.html
│       ├── validar_suscripciones.html
│       └── ...
│
├── static/                   # Archivos estáticos globales
│   ├── css/
│   │   └── style.css        # Estilos principales
│   ├── js/
│   │   └── scripts.js
│   └── img/
│
├── templates/                # Templates globales
│   └── base.html            # Template base
│
├── db.sqlite3               # Base de datos SQLite
├── manage.py                # Script de gestión de Django
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Este archivo
```

## 🔧 Comandos Útiles

### Gestión de la Base de Datos

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Poblar datos de prueba
python manage.py poblar_datos

# Crear perfiles para usuarios sin perfil
python manage.py crear_perfiles
```

### Servidor de Desarrollo

```bash
# Iniciar servidor
python manage.py runserver

# Iniciar en puerto específico
python manage.py runserver 8080

# Iniciar accesible en red local
python manage.py runserver 0.0.0.0:8000
```

### Shell Interactivo

```bash
# Acceder al shell de Django
python manage.py shell

# Ejecutar comando directo
python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.count())"
```

### Otros Comandos

```bash
# Verificar errores
python manage.py check

# Recolectar archivos estáticos
python manage.py collectstatic

# Crear dump de la base de datos
python manage.py dumpdata > backup.json

# Cargar dump
python manage.py loaddata backup.json
```

## 🌐 API y Endpoints

### URLs Públicas

- `/` - Página principal
- `/catalogo/` - Catálogo de servicios
- `/servicio/<id>/` - Detalle de servicio
- `/informacion/` - Información del proyecto

### URLs de Usuario

- `/user/registro/` - Registro de usuarios
- `/user/login/` - Inicio de sesión
- `/user/logout/` - Cerrar sesión
- `/user/dashboard/` - Panel de usuario
- `/user/suscripcion/iniciar/` - Iniciar suscripción
- `/user/suscripcion/<id>/cancelar/` - Cancelar suscripción
- `/user/suscripcion/<id>/renovar/` - Renovar suscripción

### URLs de Administración

- `/admin/` - Panel de administración de Django
- `/admin/dashboard/` - Dashboard personalizado
- `/admin/validar-suscripciones/` - Validar compras
- `/admin/gestionar-puntos/` - Gestión de puntos
- `/admin/configurar-recompensas/` - Configuración del sistema
- `/admin/reportes/` - Reportes y estadísticas

## 🎨 Características de Diseño

- **Gradientes modernos**: Combinación de morado y azul
- **Animaciones suaves**: Hover effects y transiciones
- **Responsive**: Adaptable a móviles, tablets y escritorio
- **Dark mode ready**: Base preparada para modo oscuro
- **Accesibilidad**: Uso apropiado de etiquetas ARIA

## 🔐 Seguridad

- Validación de contraseñas robustas (Django defaults)
- Protección CSRF habilitada
- Sanitización de inputs
- Autenticación requerida para acciones sensibles
- Separación de roles (Usuario/Administrador)

## 📊 Modelo de Datos

### Modelos Principales

**PerfilUsuario**
- Puntos disponibles
- Puntos totales ganados
- Puntos canjeados
- Relación uno a uno con User

**Suscripcion**
- Usuario, Plan, Servicio
- Fechas de inicio y vencimiento
- Estado (pendiente/activa/cancelada/vencida)
- Puntos ganados

**PlanSuscripcion**
- Nombre, precio, duración
- Puntos por primera compra
- Puntos por renovación
- Características (JSON)

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Notas de Desarrollo

- El sistema de pagos está pendiente de implementación
- Se recomienda integrar Stripe o PayU para producción
- Los archivos estáticos deben servirse con nginx en producción
- Configurar email backend para notificaciones

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Tetey0422**
- GitHub: [@tetey0422](https://github.com/tetey0422)
- Proyecto: [StreamPoint](https://github.com/tetey0422/StreamPoint)

## 🙏 Agradecimientos

- Django Documentation
- Bootstrap Team
- Font Awesome
- Comunidad de desarrolladores Python

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub**

Desarrollado con ❤️ usando Django
