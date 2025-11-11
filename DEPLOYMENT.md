# 🚀 Guía de Deployment - StreamPoint

## 📋 Checklist Pre-Producción

Antes de desplegar a producción, asegúrate de completar estos pasos:

### ✅ Configuración de Seguridad

- [ ] **SECRET_KEY única generada**
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(50))"
  ```
  
- [ ] **DEBUG = False**
  ```env
  DEBUG=False
  ```

- [ ] **ALLOWED_HOSTS configurado**
  ```env
  ALLOWED_HOSTS=tudominio.com,www.tudominio.com
  ```

- [ ] **Archivo .env creado y configurado** (nunca incluir en Git)

- [ ] **HTTPS habilitado** (Let's Encrypt recomendado)

- [ ] **Configuraciones de seguridad habilitadas**
  ```env
  SECURE_SSL_REDIRECT=True
  SESSION_COOKIE_SECURE=True
  CSRF_COOKIE_SECURE=True
  ```

### ✅ Base de Datos

- [ ] **PostgreSQL configurado**
  ```bash
  pip install psycopg2-binary
  ```

- [ ] **Migraciones aplicadas**
  ```bash
  python manage.py migrate
  ```

- [ ] **Backup automático configurado**

### ✅ Archivos Estáticos y Media

- [ ] **Archivos estáticos recolectados**
  ```bash
  python manage.py collectstatic --noinput
  ```

- [ ] **WhiteNoise o S3 configurado** para servir estáticos

- [ ] **Directorio media/ protegido** y con permisos correctos

### ✅ Email

- [ ] **SMTP configurado** (Gmail, SendGrid, AWS SES)
  ```env
  EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
  EMAIL_HOST=smtp.gmail.com
  EMAIL_PORT=587
  EMAIL_USE_TLS=True
  EMAIL_HOST_USER=tu-email@gmail.com
  EMAIL_HOST_PASSWORD=tu-app-password
  ```

### ✅ Logging y Monitoreo

- [ ] **Directorio logs/ creado** con permisos de escritura

- [ ] **Sentry configurado** (opcional pero recomendado)
  ```bash
  pip install sentry-sdk
  ```

- [ ] **Logs rotando correctamente**

### ✅ Performance

- [ ] **Gunicorn instalado**
  ```bash
  pip install gunicorn
  ```

- [ ] **Número de workers configurado** (2-4 × número de CPUs)

### ✅ Servidor Web

- [ ] **Nginx configurado** como proxy inverso

- [ ] **Certificado SSL instalado** (Let's Encrypt)

- [ ] **Firewall configurado** (puertos 80, 443 abiertos)

---

## 🐳 Deployment con Gunicorn + Nginx

### 1. Instalar Dependencias de Producción

```bash
pip install -r requirements.txt
pip install gunicorn whitenoise
```

### 2. Configurar Gunicorn

Crear archivo `gunicorn_config.py`:

```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 120
keepalive = 5
errorlog = "/var/log/streampoint/gunicorn_error.log"
accesslog = "/var/log/streampoint/gunicorn_access.log"
loglevel = "info"
```

### 3. Crear Servicio Systemd

Archivo `/etc/systemd/system/streampoint.service`:

```ini
[Unit]
Description=StreamPoint Django Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/streampoint
Environment="PATH=/var/www/streampoint/env/bin"
ExecStart=/var/www/streampoint/env/bin/gunicorn \
          --config /var/www/streampoint/gunicorn_config.py \
          StreamPoint.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Activar servicio:
```bash
sudo systemctl daemon-reload
sudo systemctl start streampoint
sudo systemctl enable streampoint
sudo systemctl status streampoint
```

### 4. Configurar Nginx

Archivo `/etc/nginx/sites-available/streampoint`:

```nginx
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;

    # Redirigir a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tudominio.com www.tudominio.com;

    # Certificados SSL (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/tudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tudominio.com/privkey.pem;

    # Configuraciones SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    # Archivos estáticos
    location /static/ {
        alias /var/www/streampoint/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Archivos media
    location /media/ {
        alias /var/www/streampoint/media/;
        expires 7d;
    }

    # Proxy a Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Tamaño máximo de archivos
    client_max_body_size 10M;
}
```

Activar sitio:
```bash
sudo ln -s /etc/nginx/sites-available/streampoint /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Configurar SSL con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

---

## 🌐 Variables de Entorno Producción

Crear archivo `.env` en el servidor:

```env
# Seguridad
DEBUG=False
SECRET_KEY=<generar-nueva-clave-segura>
ALLOWED_HOSTS=tudominio.com,www.tudominio.com

# Base de datos
DB_ENGINE=django.db.backends.postgresql
DB_NAME=streampoint_db
DB_USER=streampoint_user
DB_PASSWORD=<password-seguro>
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@tudominio.com
EMAIL_HOST_PASSWORD=<app-password>
DEFAULT_FROM_EMAIL=StreamPoint <noreply@tudominio.com>

# Seguridad SSL
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000

# Monitoreo (opcional)
SENTRY_DSN=<tu-sentry-dsn>
```

---

## 📊 Mantenimiento

### Backup de Base de Datos

```bash
# PostgreSQL
pg_dump -U streampoint_user streampoint_db > backup_$(date +%Y%m%d).sql

# Restaurar
psql -U streampoint_user streampoint_db < backup_20231201.sql
```

### Ver Logs

```bash
# Logs de Django
tail -f /var/www/streampoint/logs/streampoint.log
tail -f /var/www/streampoint/logs/errors.log

# Logs de Gunicorn
tail -f /var/log/streampoint/gunicorn_error.log

# Logs de Nginx
tail -f /var/log/nginx/error.log
```

### Reiniciar Servicios

```bash
sudo systemctl restart streampoint
sudo systemctl restart nginx
```

### Actualizar Código

```bash
cd /var/www/streampoint
git pull origin main
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart streampoint
```

---

## 🆘 Troubleshooting

### Error 502 Bad Gateway
- Verificar que Gunicorn esté corriendo: `sudo systemctl status streampoint`
- Revisar logs de Gunicorn: `tail -f /var/log/streampoint/gunicorn_error.log`

### Archivos estáticos no se cargan
- Ejecutar: `python manage.py collectstatic`
- Verificar permisos: `chmod -R 755 staticfiles/`

### Error de base de datos
- Verificar PostgreSQL: `sudo systemctl status postgresql`
- Verificar credenciales en `.env`
- Probar conexión: `psql -U streampoint_user -d streampoint_db`

### Emails no se envían
- Verificar configuración SMTP en `.env`
- Revisar logs de Django
- Probar con: `python manage.py shell` y enviar email de prueba

---

## 📱 Monitoring Recomendado

- **Uptime:** UptimeRobot, Pingdom
- **Errores:** Sentry
- **Performance:** New Relic, DataDog
- **Logs:** Papertrail, Loggly

---

**¡Proyecto listo para producción! 🚀**
