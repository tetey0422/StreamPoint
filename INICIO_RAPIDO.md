# 🚀 INICIO RÁPIDO - STREAMPOINT

## ⚡ Para comenzar a usar el sistema AHORA MISMO

---

## 1️⃣ INICIAR EL SERVIDOR

```powershell
cd C:\Users\PC\Desktop\StreamPoint
C:\Users\PC\Desktop\StreamPoint\env\Scripts\python.exe manage.py runserver
```

**Servidor corriendo en:** http://127.0.0.1:8000

---

## 2️⃣ CREAR UN SUPERUSUARIO (ADMIN)

```powershell
C:\Users\PC\Desktop\StreamPoint\env\Scripts\python.exe manage.py createsuperuser
```

Ingresar:
- Username: admin
- Email: admin@streampoint.com
- Password: (tu contraseña segura)

---

## 3️⃣ ACCEDER AL PANEL DE ADMINISTRACIÓN

### Django Admin (Estándar):
```
http://127.0.0.1:8000/admin/
```
- Usuario: admin
- Contraseña: (la que creaste)

### Panel Admin Personalizado:
```
http://127.0.0.1:8000/admin-panel/
```
- Requiere estar logueado como staff

---

## 4️⃣ AGREGAR CORREOS VERIFICADOS (IMPORTANTE)

**Antes de que los usuarios puedan comprar, debes agregar correos verificados:**

1. Ir a: http://127.0.0.1:8000/admin-panel/gestionar-correos/

2. Agregar correos de ejemplo:
   ```
   - test1@gmail.com → Netflix
   - test2@gmail.com → Spotify
   - test3@gmail.com → Disney+
   - usuario@ejemplo.com → Amazon Prime
   ```

3. Click en "Agregar Correo Verificado"

**Sin este paso, los usuarios NO podrán comprar suscripciones.**

---

## 5️⃣ POBLAR LA BASE DE DATOS CON DATOS DE PRUEBA

```powershell
C:\Users\PC\Desktop\StreamPoint\env\Scripts\python.exe manage.py poblar_datos
```

Esto creará:
- ✅ Categorías de streaming
- ✅ Servicios (Netflix, Spotify, Disney+, etc.)
- ✅ Planes de suscripción
- ✅ Configuración de recompensas

---

## 6️⃣ CREAR UN USUARIO DE PRUEBA

### Opción A - Desde la interfaz:
1. Ir a: http://127.0.0.1:8000/user/registro/
2. Completar formulario
3. Iniciar sesión

### Opción B - Desde comando:
```powershell
C:\Users\PC\Desktop\StreamPoint\env\Scripts\python.exe manage.py crear_perfiles
```

---

## 7️⃣ PROBAR EL SISTEMA DE COMPRA

### Paso a paso:

1. **Login como usuario:**
   ```
   http://127.0.0.1:8000/user/login/
   ```

2. **Ver catálogo:**
   ```
   http://127.0.0.1:8000/catalogo/
   ```

3. **Seleccionar un servicio** (ej: Netflix)

4. **Seleccionar un plan** (ej: Premium)

5. **Ingresar correo del servicio:**
   - Usar uno de los correos verificados que agregaste
   - Ejemplo: test1@gmail.com

6. **Completar pasarela de pago:**
   - Nombre completo
   - Teléfono
   - Dirección
   - Correo para confirmación
   - Método de pago

7. **Ver confirmación en consola:**
   - El email se mostrará en la terminal donde corre el servidor

8. **Verificar en dashboard:**
   ```
   http://127.0.0.1:8000/user/dashboard/
   ```
   - Suscripción activa ✅
   - Puntos acreditados ✅

---

## 8️⃣ PROBAR PAGO CON PUNTOS

### Darle puntos a un usuario:

1. Ir al panel admin:
   ```
   http://127.0.0.1:8000/admin-panel/gestionar-puntos/
   ```

2. Buscar el usuario

3. Agregar puntos (ejemplo: 500,000 puntos)

4. Volver al catálogo y comprar otra suscripción

5. En la pasarela de pago:
   - Marcar "Usar puntos para pagar"
   - Ingresar cantidad de puntos
   - Ver descuento en tiempo real
   - Seleccionar método para el resto (si aplica)

---

## 🔍 URLS PRINCIPALES

### Usuario:
- **Inicio:** http://127.0.0.1:8000/
- **Catálogo:** http://127.0.0.1:8000/catalogo/
- **Registro:** http://127.0.0.1:8000/user/registro/
- **Login:** http://127.0.0.1:8000/user/login/
- **Dashboard:** http://127.0.0.1:8000/user/dashboard/

### Admin:
- **Django Admin:** http://127.0.0.1:8000/admin/
- **Panel Custom:** http://127.0.0.1:8000/admin-panel/
- **Correos Verificados:** http://127.0.0.1:8000/admin-panel/gestionar-correos/
- **Gestionar Puntos:** http://127.0.0.1:8000/admin-panel/gestionar-puntos/
- **Configurar Recompensas:** http://127.0.0.1:8000/admin-panel/configurar-recompensas/

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### El servidor no inicia:
```powershell
# Verificar que el entorno virtual esté activado
C:\Users\PC\Desktop\StreamPoint\env\Scripts\python.exe manage.py check

# Ver errores específicos
C:\Users\PC\Desktop\StreamPoint\env\Scripts\python.exe manage.py runserver --traceback
```

### Error "Correo no verificado":
- Ve a: http://127.0.0.1:8000/admin-panel/gestionar-correos/
- Agrega el correo que el usuario está intentando usar
- Asegúrate de seleccionar el servicio correcto

### No se envían emails:
- **Normal en desarrollo**
- Los emails se muestran en la consola/terminal
- Para producción, configurar SMTP en `settings.py`

### Sin puntos después de comprar:
- Verificar que el pago NO sea 100% con puntos
- Los pagos solo con puntos NO otorgan cashback
- Revisar en: http://127.0.0.1:8000/admin-panel/gestionar-puntos/

---

## 📋 CHECKLIST RÁPIDO

Antes de probar compras, asegúrate de:

- [ ] Servidor corriendo
- [ ] Superusuario creado
- [ ] Datos poblados (`poblar_datos`)
- [ ] Al menos un correo verificado agregado
- [ ] Usuario de prueba creado
- [ ] Usuario tiene puntos (opcional, para probar pago con puntos)

---

## 🎨 VER EL NUEVO DISEÑO

El diseño tipo Netflix está aplicado en todas las páginas:

- ✅ Fondo negro
- ✅ Rojo Netflix como acento
- ✅ Contraste mejorado
- ✅ Animaciones suaves
- ✅ Hover effects

**Prueba navegar por:**
- Inicio
- Catálogo
- Dashboard usuario
- Panel admin

---

## ⚙️ CONFIGURACIÓN OPCIONAL

### Cambiar puntos por peso:
```
http://127.0.0.1:8000/admin-panel/configurar-recompensas/
```
- Puntos por peso: 10 (default)
- Modificar según necesites

### Activar emails reales:
Editar `StreamPoint/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'contraseña-de-aplicación'
```

---

## 💡 TIPS

### Ver emails en consola:
- Mira la terminal donde corre el servidor
- Después de cada compra, aparecerá el email completo

### Verificar suscripciones:
- Como admin: http://127.0.0.1:8000/admin/
- Ver modelo "Suscripciones"

### Ver facturas:
- Como admin: http://127.0.0.1:8000/admin/
- Ver modelo "Facturas"

### Historial de puntos:
- En el dashboard del usuario
- Se muestran las últimas 10 transacciones

---

## 🎉 ¡LISTO!

El sistema está completamente funcional y listo para usar.

**Documentación completa en:**
- `NUEVAS_FUNCIONALIDADES.md` - Detalles técnicos
- `IMPLEMENTACION_COMPLETA.md` - Resumen ejecutivo
- `README.md` - Documentación general

---

**¡Disfruta de StreamPoint!** 🚀
