# Sistema de Registro de Compras - StreamPoint

## Descripción General
Se ha implementado un sistema completo para que los usuarios registren sus compras de servicios de streaming y el administrador pueda revisar y aprobar estas compras para otorgar puntos.

## Funcionalidades Implementadas

### 1. Modelo de Datos (`RegistroCompra`)

**Ubicación**: `core_user/models.py`

El modelo incluye:
- **Información del usuario**: nombre completo, correo, usuario en la app, teléfono
- **Información de la compra**: servicio, plan (opcional), monto, fecha de compra, comprobante (opcional)
- **Control de estado**: pendiente, aprobada, rechazada
- **Gestión de puntos**: puntos otorgados al aprobar
- **Notas del administrador**: para aprobar o rechazar

**Métodos principales**:
- `aprobar(admin_user, puntos)`: Aprueba la compra y otorga puntos automáticamente
- `rechazar(admin_user, motivo)`: Rechaza la compra con un motivo

### 2. Formulario de Usuario

**Ubicación**: `core_user/forms.py`

Formulario completo con:
- Validación de campos obligatorios
- Pre-llenado automático de datos del usuario logueado
- Soporte para carga de comprobantes (imágenes/PDF)
- Validación de que el plan corresponda al servicio seleccionado

### 3. Vistas de Usuario

**Archivo**: `core_user/views.py`

**Rutas implementadas**:
- `/usuario/registrar-compra/` - Formulario para registrar una nueva compra
- `/usuario/mis-compras/` - Listado de compras registradas
- `/usuario/compra/<id>/` - Detalle de una compra específica

**Características**:
- Protección con `@login_required`
- Mensajes de confirmación/error
- Vista completa del estado de cada compra

### 4. Templates de Usuario

**Ubicación**: `core_user/templates/user/`

#### `registrar_compra.html`
- Formulario moderno y responsivo
- Secciones separadas para información personal y de compra
- Instrucciones claras para el usuario
- Validación de formularios con feedback visual

#### `mis_registros_compra.html`
- Listado con tarjetas visuales
- Badges de estado (pendiente, aprobada, rechazada)
- Iconos de servicios populares (Netflix, Spotify, etc.)
- Estado vacío cuando no hay registros

#### `detalle_registro_compra.html`
- Vista completa de toda la información
- Visualización del comprobante si existe
- Timeline de eventos (registro, revisión)
- Alertas según el estado de la compra

### 5. Panel de Administración

**Archivo**: `core_admin/views.py`

**Rutas implementadas**:
- `/admin-custom/gestionar-compras/` - Listado con filtros
- `/admin-custom/compra/<id>/` - Detalle con acciones de aprobar/rechazar

**Características**:
- Estadísticas en tiempo real (pendientes, aprobadas, rechazadas)
- Filtros por estado
- Información completa del usuario y la compra
- Formularios para aprobar (con asignación de puntos) o rechazar (con motivo)

### 6. Templates de Administración

**Ubicación**: `core_admin/templates/admin_custom/`

#### `gestionar_compras.html`
- Dashboard con estadísticas
- Filtros por estado con botones activos
- Tabla completa con toda la información
- Avatar de usuario y badges de estado

#### `detalle_compra.html`
- Vista completa de la compra
- Visualización del comprobante
- Formularios separados para aprobar/rechazar
- Solo muestra acciones si está pendiente
- Confirmación antes de aprobar/rechazar

### 7. Integración con Sistema de Puntos

Cuando el admin **aprueba una compra**:
1. Se marca como "aprobada"
2. Se registra quién la aprobó y cuándo
3. Se otorgan los puntos especificados
4. Se crea automáticamente una `TransaccionPuntos`
5. Se actualiza el perfil del usuario

Cuando el admin **rechaza una compra**:
1. Se marca como "rechazada"
2. Se registra el motivo
3. El usuario puede ver el motivo del rechazo
4. No se otorgan puntos

## Flujo de Trabajo

### Para el Usuario:
1. Usuario hace clic en "Registrar Compra"
2. Completa el formulario con sus datos
3. Adjunta comprobante (opcional)
4. Envía el formulario
5. Ve su compra en "Mis Compras Registradas"
6. Espera la revisión del admin
7. Recibe notificación (visual) del estado

### Para el Administrador:
1. Accede a "Gestionar Compras"
2. Ve el listado de compras pendientes
3. Hace clic en "Ver Detalle"
4. Revisa la información y el comprobante
5. Decide:
   - **Aprobar**: Ingresa puntos a otorgar y envía
   - **Rechazar**: Escribe el motivo y envía
6. El usuario recibe los puntos automáticamente (si se aprueba)

## URLs Configuradas

### Usuario:
```python
path('registrar-compra/', views.registrar_compra, name='registrar_compra')
path('mis-compras/', views.mis_registros_compra, name='mis_registros_compra')
path('compra/<int:registro_id>/', views.detalle_registro_compra, name='detalle_registro_compra')
```

### Admin:
```python
path('gestionar-compras/', views.gestionar_compras, name='gestionar_compras')
path('compra/<int:compra_id>/', views.detalle_compra_admin, name='detalle_compra_admin')
```

## Archivos Modificados/Creados

### Modelos:
- ✅ `core_user/models.py` - Modelo `RegistroCompra` agregado

### Formularios:
- ✅ `core_user/forms.py` - Creado con `RegistroCompraForm`

### Vistas:
- ✅ `core_user/views.py` - 3 vistas agregadas
- ✅ `core_admin/views.py` - 2 vistas agregadas

### URLs:
- ✅ `core_user/urls.py` - 3 rutas agregadas
- ✅ `core_admin/urls.py` - 2 rutas agregadas

### Templates Usuario:
- ✅ `registrar_compra.html` - Formulario de registro
- ✅ `mis_registros_compra.html` - Listado de compras
- ✅ `detalle_registro_compra.html` - Detalle de compra

### Templates Admin:
- ✅ `gestionar_compras.html` - Listado con filtros
- ✅ `detalle_compra.html` - Detalle con acciones

### Admin de Django:
- ✅ `core_user/admin.py` - Registro de `RegistroCompra`

### Migraciones:
- ✅ `0003_suscripcion_usuario_servicio_registrocompra.py` - Aplicada

## Características Destacadas

### Seguridad:
- ✅ Protección `@login_required` en vistas de usuario
- ✅ Protección `@staff_member_required` en vistas de admin
- ✅ Validación de pertenencia (usuario solo ve sus compras)
- ✅ Confirmación antes de acciones importantes

### UX/UI:
- ✅ Diseño moderno y responsivo
- ✅ Iconos de Font Awesome
- ✅ Badges de estado con colores
- ✅ Mensajes de confirmación/error
- ✅ Estados vacíos informativos

### Funcionalidad:
- ✅ Carga de archivos (comprobantes)
- ✅ Filtros por estado
- ✅ Estadísticas en tiempo real
- ✅ Integración automática con sistema de puntos
- ✅ Historial completo de transacciones

## Próximos Pasos Sugeridos

1. **Notificaciones por Email**: Enviar email cuando se aprueba/rechaza una compra
2. **Dashboard de Usuario**: Mostrar compras pendientes en el dashboard
3. **Exportación de Reportes**: Exportar compras a Excel/PDF
4. **Carga Masiva**: Permitir al admin aprobar múltiples compras a la vez
5. **API de Carga de Planes**: Cargar planes dinámicamente según el servicio seleccionado

## Cómo Usar

### Para Usuarios:
1. Iniciar sesión
2. Ir a `/usuario/registrar-compra/`
3. Completar formulario
4. Revisar estado en `/usuario/mis-compras/`

### Para Admins:
1. Iniciar sesión como staff
2. Ir a `/admin-custom/gestionar-compras/`
3. Filtrar por estado
4. Revisar y aprobar/rechazar compras

## Configuración de Medios

Los comprobantes se guardan en `/media/comprobantes/`

Asegúrate de tener configurado en `settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Y en las URLs principales agregar (si no está):
```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
