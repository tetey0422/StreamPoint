# Core Public - Archivos Estáticos

Esta carpeta contiene todos los archivos estáticos (CSS, JavaScript, imágenes) específicos para la aplicación **core_public**.

## Estructura

```
core_public/static/public/
├── css/
│   └── public_styles.css      # Estilos específicos para templates públicos
├── js/
│   └── public_scripts.js      # Scripts JavaScript para funcionalidad pública
└── img/
    └── (imágenes específicas del módulo público)
```

## Archivos CSS

### `public_styles.css`
Contiene estilos específicos para:
- **Catálogo**: Búsqueda y filtros de servicios
- **Detalle Servicio**: Breadcrumbs, badges, planes destacados
- **Información Proyecto**: Iconos de categoría, gradientes, contadores
- **Animaciones**: Fade-in, slide-up, parallax
- **Responsive**: Media queries específicas para vistas públicas

## Archivos JavaScript

### `public_scripts.js`
Incluye funcionalidades como:
- **Búsqueda en tiempo real** en el catálogo
- **Animaciones** al hacer scroll (Intersection Observer)
- **Contadores animados** en la página de información
- **Smooth scroll** para enlaces internos
- **Lazy loading** de imágenes
- **Manejo de errores** de carga de imágenes
- **Tooltips** de Bootstrap
- **Prevención de doble envío** en formularios
- **Funciones auxiliares**: formatCurrency, formatNumber, debounce

## Uso en Templates

Para usar estos archivos en tus templates, agrega:

```django
{% load static %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'public/css/public_styles.css' %}">
{% endblock %}

{% block extra_js %}
<script src="{% static 'public/js/public_scripts.js' %}"></script>
{% endblock %}
```

## Imágenes

La carpeta `img/` está reservada para:
- Logos de servicios de streaming
- Banners promocionales
- Iconos personalizados
- Imágenes de categorías
- Fondos y recursos gráficos públicos

## Buenas Prácticas

1. **Separación de responsabilidades**: Mantén los estilos específicos de core_public aquí, no en el CSS global
2. **Nomenclatura**: Usa nombres descriptivos y prefijos si es necesario (ej: `public-`, `catalog-`)
3. **Optimización**: Comprime imágenes antes de subirlas
4. **Versionado**: Considera usar cache busting para actualizaciones (`?v=1.0`)
5. **Organización**: Agrupa estilos relacionados con comentarios claros

## Relación con Otros Archivos

- **`static/css/style.css`**: Estilos globales compartidos por toda la aplicación
- **`core_user/static/user/`**: Archivos estáticos del módulo de usuarios
- **`core_admin/static/admin_custom/`**: Archivos estáticos del panel de administración

## Mantenimiento

- Revisa periódicamente si hay código no utilizado
- Mantén los comentarios actualizados
- Documenta nuevas funcionalidades agregadas
- Prueba en diferentes navegadores y dispositivos
