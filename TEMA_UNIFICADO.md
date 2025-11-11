# 🎨 Tema Unificado de StreamPoint

## Resumen de Cambios

Se ha aplicado una temática consistente en todo el proyecto StreamPoint, basada en la estética del dashboard con colores morados/azules y estilo moderno tipo Netflix.

## 🎨 Paleta de Colores

### Colores Principales
- **Primary**: `#6366f1` (Azul-Morado)
- **Primary Dark**: `#4f46e5`
- **Secondary**: `#8b5cf6` (Morado)
- **Success**: `#46d369` (Verde)
- **Warning**: `#fbbf24` (Dorado)
- **Danger**: `#ef4444` (Rojo)

### Tonos Oscuros (Fondo)
- **Netflix Black**: `#141414` (Fondo principal)
- **Netflix Dark Gray**: `#1f1f1f` (Tarjetas)
- **Netflix Gray**: `#2f2f2f` (Elementos hover)

### Textos
- **Netflix White**: `#e8e8e8` (Títulos)
- **Netflix Text**: `#d1d1d1` (Texto normal)
- **Netflix Light Gray**: `#808080` (Texto secundario)

## 🎯 Componentes Estilizados

### 1. Tarjetas (Cards)
```html
<div class="card-custom">
    <!-- Contenido -->
</div>
```
- Fondo oscuro con bordes sutiles
- Hover con efecto de escala y brillo morado
- Bordes redondeados

### 2. Tarjetas de Estadísticas (Dashboard Stats)
```html
<div class="dashboard-stat-card">
    <div class="stat-icon mb-3">
        <i class="fas fa-coins" style="font-size: 2.5rem; color: var(--warning);"></i>
    </div>
    <div class="stat-value">120</div>
    <div class="stat-label">Puntos Disponibles</div>
</div>
```
- Valores con gradiente morado/azul
- Animación de hover (levitar)
- Iconos grandes con sombra

### 3. Botones

#### Botón Principal
```html
<button class="btn btn-primary-custom">Texto</button>
```
- Gradiente morado/azul
- Efecto de escala en hover
- Sombra brillante

#### Botones Outline
```html
<button class="btn btn-outline-primary">Texto</button>
<button class="btn btn-outline-danger">Texto</button>
<button class="btn btn-outline-secondary">Texto</button>
```
- Bordes con colores temáticos
- Relleno en hover con animación

### 4. Headers con Gradiente
```html
<div class="card-custom p-4 bg-gradient-primary text-white">
    <h1>Título</h1>
</div>
```

### 5. Texto con Gradiente
```html
<h3 class="text-gradient">
    <i class="fas fa-history me-2"></i>Historial de Puntos
</h3>
```

### 6. Tablas
```html
<table class="table table-hover">
    <thead class="table-light">
        <!-- Headers con gradiente morado -->
    </thead>
    <tbody>
        <!-- Filas con hover morado suave -->
    </tbody>
</table>
```

### 7. Barras de Progreso
```html
<div class="progress" style="height: 8px;">
    <div class="progress-bar bg-success" style="width: 75%"></div>
</div>
```
- Fondo oscuro transparente
- Gradientes en las barras

### 8. Badges
```html
<span class="badge bg-success">Activo</span>
<span class="badge bg-warning text-dark fw-bold">120 PTS</span>
<span class="badge bg-danger">Cancelado</span>
```

### 9. Tarjetas de Suscripción
```html
<div class="subscription-card active">
    <!-- Contenido -->
</div>
```
- Borde izquierdo colorido según estado
- Gradiente de fondo
- Animación de deslizamiento en hover

## 🎨 Gradientes Disponibles

### Primario (Morado/Azul)
```css
.bg-gradient-primary
/* linear-gradient(135deg, #667eea 0%, #764ba2 100%) */
```

### Advertencia (Amarillo/Naranja)
```css
.bg-gradient-warning
/* linear-gradient(135deg, #f59e0b 0%, #d97706 100%) */
```

### Éxito (Verde)
```css
.bg-gradient-success
/* linear-gradient(135deg, #10b981 0%, #059669 100%) */
```

### Peligro (Rojo)
```css
.bg-gradient-danger
/* linear-gradient(135deg, #ef4444 0%, #dc2626 100%) */
```

## 🔧 Características Técnicas

### Animaciones
- Transiciones suaves de 0.3s en todos los elementos interactivos
- Efectos de hover con `transform: scale()` y `translateY()`
- Sombras dinámicas con colores temáticos

### Responsive
- Breakpoints en 768px para tablets y móviles
- Reducción de tamaños de fuente en pantallas pequeñas
- Tarjetas apiladas en móviles

### Accesibilidad
- Contraste adecuado entre texto y fondo
- Textos legibles con colores claros sobre fondos oscuros
- Indicadores visuales claros para estados (hover, active, disabled)

## 📱 Navegación

### Navbar
- Fondo oscuro con efecto blur
- Borde inferior morado sutil
- Links con subrayado animado
- Dropdown con fondo oscuro y hover morado

### Badge de Puntos
```html
<span class="badge bg-warning ms-2 text-dark fw-bold">120 PTS</span>
```
- Gradiente dorado
- Texto negro en negrita
- Border-radius redondeado

## 🎯 Páginas Actualizadas

Todas las páginas del proyecto ahora utilizan la misma temática:

- ✅ Dashboard de Usuario
- ✅ Página Principal (Index)
- ✅ Catálogo de Servicios
- ✅ Detalle de Servicios
- ✅ Login y Registro
- ✅ Gestión de Suscripciones
- ✅ Historial de Compras
- ✅ Sobre Nosotros

## 📝 Notas para Desarrollo

1. **Siempre usar `card-custom`** para tarjetas en lugar de `card` de Bootstrap
2. **Botones principales** deben usar `btn-primary-custom`
3. **Tablas** deben usar `table-hover` con `thead` que tenga clase `table-light`
4. **Gradientes de texto** se aplican con clase `text-gradient`
5. **Estados de suscripción** usar clases: `active`, `pending`, `cancelled`

## 🚀 Próximos Pasos

Para mantener la consistencia:
- Revisar nuevas páginas que se agreguen
- Usar las variables CSS definidas en `:root`
- Seguir la guía de componentes al crear nuevos elementos
- Mantener la paleta de colores establecida

---

**Tema creado**: Noviembre 2025  
**Inspiración**: Netflix + Dashboard Moderno  
**Colores principales**: Morado (#6366f1) y Azul (#764ba2)
