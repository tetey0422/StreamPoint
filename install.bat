@echo off
REM ============================================
REM StreamPoint - Script de Instalacion Rapida (Windows)
REM ============================================
REM Este script automatiza la instalacion de StreamPoint en Windows
REM ============================================

echo.
echo ========================================
echo    StreamPoint - Instalacion Rapida
echo ========================================
echo.

REM 1. Verificar Python
echo [1/9] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado. Por favor, instala Python 3.8 o superior.
    pause
    exit /b 1
)
python --version
echo OK: Python encontrado
echo.

REM 2. Crear entorno virtual
echo [2/9] Creando entorno virtual...
python -m venv env
if errorlevel 1 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)
echo OK: Entorno virtual creado
echo.

REM 3. Activar entorno virtual
echo [3/9] Activando entorno virtual...
call env\Scripts\activate.bat
echo OK: Entorno virtual activado
echo.

REM 4. Actualizar pip
echo [4/9] Actualizando pip...
python -m pip install --upgrade pip --quiet
echo OK: pip actualizado
echo.

REM 5. Instalar dependencias
echo [5/9] Instalando dependencias (esto puede tardar unos minutos)...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo OK: Dependencias instaladas
echo.

REM 6. Copiar .env.example si no existe .env
echo [6/9] Configurando variables de entorno...
if not exist .env (
    copy .env.example .env >nul
    echo OK: Archivo .env creado desde .env.example
    echo NOTA: Puedes editar .env con tus configuraciones personalizadas
) else (
    echo NOTA: Archivo .env ya existe, no se sobrescribira
)
echo.

REM 7. Aplicar migraciones
echo [7/9] Aplicando migraciones de base de datos...
python manage.py migrate --no-input
if errorlevel 1 (
    echo ERROR: No se pudieron aplicar las migraciones
    pause
    exit /b 1
)
echo OK: Migraciones aplicadas
echo.

REM 8. Poblar datos de prueba
echo [8/9] Poblar base de datos con datos de prueba? (S/N)
set /p poblar="Tu respuesta: "
if /i "%poblar%"=="S" (
    python manage.py poblar_datos
    echo OK: Datos de prueba cargados
) else (
    echo NOTA: Puedes poblar datos despues con: python manage.py poblar_datos
)
echo.

REM 9. Crear superusuario
echo [9/9] Crear un superusuario (admin)? (S/N)
set /p crear_admin="Tu respuesta: "
if /i "%crear_admin%"=="S" (
    python manage.py createsuperuser
) else (
    echo NOTA: Puedes crear un superusuario despues con: python manage.py createsuperuser
)
echo.

REM Finalizar
echo.
echo ========================================
echo   Instalacion completada exitosamente!
echo ========================================
echo.
echo Para iniciar el servidor, ejecuta:
echo     python manage.py runserver
echo.
echo URLs disponibles:
echo     http://127.0.0.1:8000/ - Aplicacion principal
echo     http://127.0.0.1:8000/admin/ - Panel admin Django
echo     http://127.0.0.1:8000/admin-custom/dashboard/ - Panel admin personalizado
echo.
echo Documentacion:
echo     README.md - Guia de uso
echo     DEPLOYMENT.md - Guia de deployment
echo.
echo Feliz desarrollo!
echo.
pause
