# 📋 Estructura del Proyecto StreamPoint

## 🎯 Arquitectura Modular

```
StreamPoint/
├── 📁 StreamPoint/          # Configuración principal de Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── 📁 core_public/          # Módulo público (sin autenticación)
│   ├── models.py           # CategoriaStreaming, ServicioStreaming, PlanSuscripcion, ConfiguracionRecompensa
│   ├── views.py            # Vistas públicas
│   ├── urls.py             # URLs: /, /catalogo/, /servicio/<id>/, /proyecto/
│   ├── templates/public/   # Templates públicos
│   └── static/public/      # CSS, JS, imágenes públicas
│
├── 📁 core_user/            # Módulo de usuario (requiere login)
│   ├── models.py           # PerfilUsuario, Suscripcion, RegistroCompra, TransaccionPuntos, Factura
│   ├── views.py            # Dashboard, suscripciones, compras, puntos
│   ├── urls.py             # URLs de usuario
│   ├── forms.py            # Formularios de usuario
│   ├── signals.py          # Señales para crear perfiles automáticamente
│   ├── templates/user/     # Templates de usuario
│   └── static/user/        # CSS, JS específicos de usuario
│
├── 📁 core_admin/           # Módulo administrativo
│   ├── views.py            # Panel admin, gestión de compras, reportes
│   ├── urls.py             # URLs administrativas
│   ├── templates/admin_custom/ # Templates admin personalizados
│   └── static/admin_custom/    # CSS, JS admin
│
├── 📁 templates/            # Templates base compartidos
│   └── base.html           # Template base con navbar y footer
│
├── 📁 static/               # Archivos estáticos globales
│   ├── css/style.css       # Estilos globales (tema oscuro)
│   ├── js/scripts.js       # JavaScript global
│   └── img/                # Imágenes globales
│
└── 📁 env/                  # Entorno virtual Python (no en Git)
```

## 🔗 URLs del Proyecto

### Públicas (core_public)
- `/` - Página principal
- `/catalogo/` - Catálogo de servicios
- `/servicio/<id>/` - Detalle de servicio
- `/proyecto/` - Información del proyecto

### Usuario (core_user) - Requiere Login
- `/user/dashboard/` - Panel de usuario
- `/user/suscripciones/` - Gestión de suscripciones
- `/user/suscribirse/<plan_id>/` - Suscribirse a un plan
- `/user/cancelar-suscripcion/<suscripcion_id>/` - Cancelar suscripción
- `/user/compras/` - Historial de compras
- `/user/registrar-compra/` - Registrar nueva compra
- `/user/puntos/` - Historial de puntos

### Administrativas (core_admin) - Requiere Staff
- `/admin-custom/dashboard/` - Panel administrativo
- `/admin-custom/gestionar-compras/` - Gestión de compras registradas
- `/admin-custom/validar-suscripciones/` - Validación de suscripciones
- `/admin-custom/reportes/` - Reportes y estadísticas
- `/admin-custom/configurar-recompensas/` - Configuración de recompensas

## 🎨 Tema Visual

**Estilo:** Tema oscuro inspirado en Netflix
- Fondo principal: `#141414`
- Fondo secundario: `#1f1f1f`
- Color primario: `#6366f1` (púrpura)
- Color de advertencia: `#ffc107` (amarillo)
- Texto claro: `#e8e8e8`
- Bordes redondeados: `50px` para secciones principales
- Sombras: `0 10px 40px rgba(0, 0, 0, 0.5)`

## 🗄️ Modelos Principales

### core_public
- `CategoriaStreaming` - Categorías de servicios
- `ServicioStreaming` - Servicios disponibles
- `PlanSuscripcion` - Planes de suscripción
- `ConfiguracionRecompensa` - Configuración de puntos

### core_user
- `PerfilUsuario` - Perfil extendido del usuario
- `Suscripcion` - Suscripciones activas
- `RegistroCompra` - Compras registradas por usuarios
- `TransaccionPuntos` - Historial de movimientos de puntos
- `Factura` - Facturas generadas

## 📦 Comandos de Gestión

```bash
# Poblar datos de prueba
python manage.py poblar_datos

# Crear perfiles para usuarios existentes
python manage.py crear_perfiles
```

## 🚀 Instalación y Ejecución

```bash
# Activar entorno virtual
.\env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Poblar datos de prueba
python manage.py poblar_datos

# Ejecutar servidor
python manage.py runserver
```

## 📝 Funcionalidades Principales

1. **Sistema de Puntos y Recompensas**
   - Los usuarios ganan puntos por registrar compras
   - Bonificación por primera compra
   - Historial completo de transacciones

2. **Gestión de Suscripciones**
   - Suscripción a planes de servicios
   - Renovación automática
   - Cancelación de suscripciones

3. **Registro de Compras**
   - Los usuarios registran compras con comprobante
   - Validación por administradores
   - Aprobación/Rechazo con asignación de puntos

4. **Panel Administrativo Personalizado**
   - Dashboard con estadísticas
   - Gestión de compras pendientes
   - Validación de suscripciones
   - Reportes y métricas

## 🔐 Seguridad

- Autenticación requerida para módulos de usuario y admin
- Decoradores `@login_required` y `@user_passes_test`
- Validación de permisos en todas las vistas sensibles
- CSRF protection en formularios
