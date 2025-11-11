# 🎬 StreamPoint

**Sistema de Gestión de Suscripciones de Streaming con Sistema de Recompensas por Puntos**

StreamPoint es una plataforma web desarrollada en Django que permite a los usuarios gestionar sus suscripciones a servicios de streaming de manera legal y segura, mientras ganan puntos por cada compra registrada que pueden canjear por nuevas suscripciones.

![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Comandos Útiles](#-comandos-útiles)
- [Endpoints](#-endpoints)
- [Licencia](#-licencia)

---

## ✨ Características

### 🎯 Funcionalidades Principales

- **Sistema de Autenticación Completo**
  - Registro de usuarios con creación automática de perfil
  - Inicio y cierre de sesión seguros
  - Gestión de perfiles de usuario

- **Catálogo de Servicios de Streaming**
  - Servicios populares: Netflix, Spotify, Disney+, HBO Max, Prime Video, etc.
  - Múltiples planes por servicio (Individual, Familiar, Premium)
  - Información detallada de cada servicio
  - Búsqueda y filtrado por categorías

- **Sistema de Registro de Compras** 📝
  - Los usuarios registran sus compras con comprobante
  - Validación manual por administradores
  - Estados: Pendiente, Aprobado, Rechazado
  - Subida de imágenes de facturas

- **Sistema de Puntos y Recompensas** ⭐
  - Gana puntos por cada compra aprobada
  - Bonificación especial por primera compra
  - Puntos adicionales por renovaciones
  - Conversión: 1 punto = 12 COP
  - Historial completo de transacciones de puntos

- **Gestión de Suscripciones**
  - Suscripción a planes de servicios
  - Estados: Pendiente, Activa, Cancelada, Vencida
  - Cancelación de suscripciones
  - Notificaciones de estado

- **Panel de Administración Personalizado** 🔧
  - Dashboard con estadísticas en tiempo real
  - Gestión de compras registradas (aprobar/rechazar)
  - Validación de suscripciones
  - Gestión manual de puntos de usuarios
  - Configuración del sistema de recompensas
  - Reportes y analíticas detalladas
  - Gestión de correos de notificación

- **Interfaz de Usuario Moderna** 🎨
  - Diseño responsive con Bootstrap 5
  - Tema oscuro elegante (estilo Netflix)
  - Animaciones y transiciones suaves
  - Iconos con Font Awesome
  - Bordes redondeados y sombras modernas

---

## 🛠️ Tecnologías

### Backend
- **Django 5.2.7** - Framework web de alto nivel
- **Python 3.13** - Lenguaje de programación
- **SQLite** - Base de datos (desarrollo)

### Frontend
- **Bootstrap 5** - Framework CSS responsive
- **Font Awesome** - Biblioteca de iconos
- **JavaScript Vanilla** - Interactividad del cliente
- **CSS3** - Estilos personalizados con tema oscuro

### Herramientas
- **Git** - Control de versiones
- **Pillow** - Procesamiento de imágenes (facturas)

---

## 📦 Instalación

### Requisitos Previos

- Python 3.13 o superior
- pip (gestor de paquetes de Python)
- Git (opcional)

### Pasos de Instalación

1. **Clonar o descargar el repositorio**
```bash
git clone https://github.com/tetey0422/StreamPoint.git
cd StreamPoint
```

2. **Crear y activar entorno virtual**
```bash
# Windows
python -m venv env
.\env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno (opcional para desarrollo)**
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones (opcional en desarrollo)
# Para desarrollo local, las configuraciones por defecto funcionan bien
```

5. **Aplicar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario (administrador)**
```bash
python manage.py createsuperuser
```

7. **Poblar base de datos con datos de prueba**
```bash
python manage.py poblar_datos
```

8. **Iniciar servidor de desarrollo**
```bash
python manage.py runserver
```

9. **Acceder a la aplicación**
- **Aplicación:** http://127.0.0.1:8000/
- **Admin Django:** http://127.0.0.1:8000/admin/
- **Panel Admin Personalizado:** http://127.0.0.1:8000/admin-custom/dashboard/

### ⚙️ Configuración Avanzada

#### Variables de Entorno

El proyecto usa variables de entorno para configuraciones sensibles. Para desarrollo local no es necesario configurarlas, pero para producción sí.

**Archivo `.env.example`** incluido como plantilla:
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con tus configuraciones
nano .env  # o tu editor preferido
```

**Variables importantes:**
- `DEBUG` - Modo debug (True/False)
- `SECRET_KEY` - Clave secreta de Django (generar nueva para producción)
- `ALLOWED_HOSTS` - Hosts permitidos (separados por comas)
- `DB_*` - Configuración de base de datos PostgreSQL
- `EMAIL_*` - Configuración SMTP para emails

**Generar SECRET_KEY segura:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

#### Base de Datos para Producción

Para producción se recomienda PostgreSQL:

1. **Instalar dependencia:**
```bash
pip install psycopg2-binary
```

2. **Configurar en `.env`:**
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=streampoint_db
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
```

3. **Actualizar `settings.py` para leer variables:**
```python
import os
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', ''),
    }
}
```

---

## 🚀 Uso

### Para Usuarios Normales

1. **Registrarse** en `/user/registro/`
2. **Explorar catálogo** de servicios de streaming
3. **Ver detalles** de cada servicio y sus planes
4. **Registrar compra** desde el dashboard con comprobante
5. **Esperar aprobación** del administrador
6. **Recibir puntos** automáticamente al aprobar la compra
7. **Acumular y canjear** puntos por suscripciones

### Para Administradores

1. **Acceder al panel admin** en `/admin-custom/dashboard/`
2. **Revisar compras pendientes** en "Gestionar Compras"
3. **Aprobar o rechazar** compras con asignación de puntos
4. **Validar suscripciones** de usuarios
5. **Gestionar puntos** manualmente si es necesario
6. **Configurar recompensas** del sistema
7. **Ver reportes** y estadísticas

---

## 📁 Estructura del Proyecto

```
StreamPoint/
├── 📁 StreamPoint/              # Configuración principal Django
│   ├── settings.py             # Configuración del proyecto
│   ├── urls.py                 # URLs principales
│   ├── wsgi.py                 # WSGI para producción
│   └── asgi.py                 # ASGI para async
│
├── 📁 core_public/              # App pública (sin autenticación)
│   ├── models.py               # CategoriaStreaming, ServicioStreaming, PlanSuscripcion, ConfiguracionRecompensa
│   ├── views.py                # index, catalogo, detalle_servicio, informacion_proyecto
│   ├── urls.py                 # URLs públicas
│   ├── admin.py                # Registro de modelos en admin
│   ├── templates/public/       # Templates públicos
│   │   ├── index.html
│   │   ├── catalogo.html
│   │   ├── detalle_servicio.html
│   │   └── informacion_proyecto.html
│   ├── static/public/          # CSS, JS, imágenes públicas
│   │   ├── css/public_styles.css
│   │   └── js/
│   └── management/commands/
│       └── poblar_datos.py     # Comando para poblar BD
│
├── 📁 core_user/                # App de usuarios (requiere login)
│   ├── models.py               # PerfilUsuario, Suscripcion, RegistroCompra, TransaccionPuntos, Factura
│   ├── views.py                # Dashboard, suscripciones, compras, puntos
│   ├── forms.py                # RegistroCompraForm
│   ├── signals.py              # Crear perfil automáticamente
│   ├── urls.py                 # URLs de usuario
│   ├── admin.py                # Modelos en admin
│   ├── templates/user/         # Templates de usuario
│   │   ├── registro.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── mis_suscripciones.html
│   │   ├── mis_registros_compra.html
│   │   ├── registrar_compra.html
│   │   └── historial_puntos.html
│   ├── static/user/            # CSS, JS de usuario
│   ├── templatetags/
│   │   └── user_extras.py      # Filtros personalizados
│   └── management/commands/
│       └── crear_perfiles.py   # Crear perfiles faltantes
│
├── 📁 core_admin/               # App administrativa (staff only)
│   ├── views.py                # Dashboard admin, gestión, reportes
│   ├── urls.py                 # URLs administrativas
│   ├── templates/admin_custom/ # Templates admin personalizados
│   │   ├── dashboard.html
│   │   ├── gestionar_compras.html
│   │   ├── validar_suscripciones.html
│   │   ├── gestionar_puntos.html
│   │   ├── configurar_recompensas.html
│   │   ├── reportes.html
│   │   └── gestionar_correos.html
│   └── static/admin_custom/    # CSS, JS admin
│
├── 📁 templates/                # Templates base globales
│   └── base.html               # Template base con navbar y footer
│
├── 📁 static/                   # Archivos estáticos globales
│   ├── css/
│   │   └── style.css           # Estilos globales (tema oscuro)
│   ├── js/
│   │   └── scripts.js          # JavaScript global
│   └── img/                    # Imágenes globales
│
├── 📁 env/                      # Entorno virtual (no en Git)
├── 📄 db.sqlite3                # Base de datos SQLite
├── 📄 manage.py                 # Script de gestión Django
├── 📄 requirements.txt          # Dependencias Python
├── 📄 README.md                 # Este archivo
├── 📄 LICENSE                   # Licencia MIT
└── 📄 .gitignore                # Archivos ignorados por Git
```

---

## 🔧 Comandos Útiles

### Comandos de Base de Datos
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

### Comandos de Servidor
```bash
# Iniciar servidor de desarrollo
python manage.py runserver

# Iniciar en puerto específico
python manage.py runserver 8080

# Accesible desde red local
python manage.py runserver 0.0.0.0:8000
```

### Comandos de Shell
```bash
# Abrir shell interactivo de Django
python manage.py shell

# Verificar errores del proyecto
python manage.py check

# Recolectar archivos estáticos (para producción)
python manage.py collectstatic
```

---

## 🌐 Endpoints

### URLs Públicas
```
/                           # Página principal
/catalogo/                  # Catálogo de servicios
/servicio/<id>/             # Detalle de servicio específico
/proyecto/                  # Información del proyecto académico
```

### URLs de Usuario (requiere login)
```
/user/registro/             # Registro de nuevos usuarios
/user/login/                # Inicio de sesión
/user/logout/               # Cerrar sesión
/user/dashboard/            # Panel principal del usuario
/user/suscripciones/        # Mis suscripciones
/user/suscribirse/<plan_id>/    # Suscribirse a un plan
/user/cancelar-suscripcion/<id>/  # Cancelar suscripción
/user/compras/              # Historial de compras registradas
/user/registrar-compra/     # Registrar nueva compra
/user/puntos/               # Historial de puntos
```

### URLs Administrativas (requiere staff)
```
/admin/                              # Django admin nativo
/admin-custom/dashboard/             # Dashboard personalizado
/admin-custom/gestionar-compras/     # Aprobar/rechazar compras
/admin-custom/gestionar-compras/<id>/  # Detalle de compra
/admin-custom/validar-suscripciones/   # Validar suscripciones
/admin-custom/validar-suscripciones/<id>/  # Detalle de suscripción
/admin-custom/gestionar-puntos/      # Gestión manual de puntos
/admin-custom/configurar-recompensas/  # Configurar sistema de puntos
/admin-custom/reportes/              # Reportes y estadísticas
/admin-custom/gestionar-correos/     # Gestión de correos
```

---

## � Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

**Tetey0422**
- GitHub: [@tetey0422](https://github.com/tetey0422)
- Repositorio: [StreamPoint](https://github.com/tetey0422/StreamPoint)

---

## 🙏 Agradecimientos

- [Django Project](https://www.djangoproject.com/) - Framework web
- [Bootstrap](https://getbootstrap.com/) - Framework CSS
- [Font Awesome](https://fontawesome.com/) - Iconos
- Comunidad de desarrolladores Python/Django

---

<div align="center">

**⭐ Si te gusta este proyecto, dale una estrella en GitHub ⭐**

Desarrollado con ❤️ usando Django

</div>
