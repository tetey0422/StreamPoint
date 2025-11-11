#!/bin/bash

# ============================================
# StreamPoint - Script de Instalación Rápida
# ============================================
# Este script automatiza la instalación de StreamPoint
# ============================================

echo "🎬 Instalando StreamPoint..."
echo ""

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Verificar Python
echo -e "${BLUE}📌 Verificando Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ Python no está instalado. Por favor, instala Python 3.8 o superior."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Python $PYTHON_VERSION encontrado${NC}"
echo ""

# 2. Crear entorno virtual
echo -e "${BLUE}📌 Creando entorno virtual...${NC}"
$PYTHON_CMD -m venv env
echo -e "${GREEN}✅ Entorno virtual creado${NC}"
echo ""

# 3. Activar entorno virtual
echo -e "${BLUE}📌 Activando entorno virtual...${NC}"
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source env/Scripts/activate
else
    source env/bin/activate
fi
echo -e "${GREEN}✅ Entorno virtual activado${NC}"
echo ""

# 4. Actualizar pip
echo -e "${BLUE}📌 Actualizando pip...${NC}"
pip install --upgrade pip --quiet
echo -e "${GREEN}✅ pip actualizado${NC}"
echo ""

# 5. Instalar dependencias
echo -e "${BLUE}📌 Instalando dependencias...${NC}"
pip install -r requirements.txt --quiet
echo -e "${GREEN}✅ Dependencias instaladas${NC}"
echo ""

# 6. Copiar .env.example si no existe .env
if [ ! -f .env ]; then
    echo -e "${BLUE}📌 Copiando archivo .env.example a .env...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ Archivo .env creado${NC}"
    echo -e "${YELLOW}⚠️  Recuerda editar .env con tus configuraciones si es necesario${NC}"
else
    echo -e "${YELLOW}⚠️  Archivo .env ya existe, no se sobrescribirá${NC}"
fi
echo ""

# 7. Aplicar migraciones
echo -e "${BLUE}📌 Aplicando migraciones de base de datos...${NC}"
python manage.py migrate --no-input
echo -e "${GREEN}✅ Migraciones aplicadas${NC}"
echo ""

# 8. Poblar datos de prueba
echo -e "${BLUE}📌 ¿Deseas poblar la base de datos con datos de prueba? (s/n)${NC}"
read -p "Respuesta: " poblar
if [[ $poblar == "s" || $poblar == "S" || $poblar == "yes" || $poblar == "YES" ]]; then
    python manage.py poblar_datos
    echo -e "${GREEN}✅ Datos de prueba cargados${NC}"
else
    echo -e "${YELLOW}⏭️  Saltando carga de datos de prueba${NC}"
fi
echo ""

# 9. Crear superusuario
echo -e "${BLUE}📌 ¿Deseas crear un superusuario (admin)? (s/n)${NC}"
read -p "Respuesta: " crear_admin
if [[ $crear_admin == "s" || $crear_admin == "S" || $crear_admin == "yes" || $crear_admin == "YES" ]]; then
    python manage.py createsuperuser
    echo -e "${GREEN}✅ Superusuario creado${NC}"
else
    echo -e "${YELLOW}⏭️  Puedes crear un superusuario después con: python manage.py createsuperuser${NC}"
fi
echo ""

# 10. Finalizar
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
echo -e "${GREEN}✨ ¡Instalación completada exitosamente! ✨${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}🚀 Para iniciar el servidor, ejecuta:${NC}"
echo -e "   ${YELLOW}python manage.py runserver${NC}"
echo ""
echo -e "${BLUE}📝 URLs disponibles:${NC}"
echo -e "   ${YELLOW}http://127.0.0.1:8000/${NC} - Aplicación principal"
echo -e "   ${YELLOW}http://127.0.0.1:8000/admin/${NC} - Panel de administración Django"
echo -e "   ${YELLOW}http://127.0.0.1:8000/admin-custom/dashboard/${NC} - Panel admin personalizado"
echo ""
echo -e "${BLUE}📚 Documentación:${NC}"
echo -e "   ${YELLOW}README.md${NC} - Guía de uso"
echo -e "   ${YELLOW}DEPLOYMENT.md${NC} - Guía de deployment"
echo ""
echo -e "${GREEN}¡Feliz desarrollo! 🎉${NC}"
