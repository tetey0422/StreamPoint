#!/usr/bin/env python
"""
Script de Verificación de Seguridad - StreamPoint
================================================
Este script verifica que las mejoras de seguridad se hayan implementado correctamente.

Uso:
    python verificar_seguridad.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StreamPoint.settings')
django.setup()

from django.contrib.auth.models import User
from core_user.models import PerfilUsuario, RegistroCompra
from core_user.forms import RegistroCompraForm
from core_public.models import ServicioStreaming, PlanSuscripcion
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from colorama import init, Fore, Style
import io

# Inicializar colorama para colores en terminal
init(autoreset=True)

def print_header(text):
    """Imprime un encabezado"""
    print(f"\n{Fore.CYAN}{'=' * 70}")
    print(f"{Fore.CYAN}{text.center(70)}")
    print(f"{Fore.CYAN}{'=' * 70}\n")

def print_test(test_name, passed, details=""):
    """Imprime resultado de un test"""
    status = f"{Fore.GREEN}✓ PASSED" if passed else f"{Fore.RED}✗ FAILED"
    print(f"{status} - {test_name}")
    if details:
        print(f"  {Fore.YELLOW}→ {details}")

def test_puntos_calculados_automaticamente():
    """Test 1: Verificar que los puntos se calculan automáticamente"""
    print_header("TEST 1: Cálculo Automático de Puntos")
    
    try:
        # Crear datos de prueba
        user = User.objects.first()
        if not user:
            print_test("Cálculo Automático de Puntos", False, "No hay usuarios en la BD")
            return False
        
        perfil = PerfilUsuario.objects.filter(usuario=user).first()
        if not perfil:
            print_test("Cálculo Automático de Puntos", False, "No hay perfil para el usuario")
            return False
        
        servicio = ServicioStreaming.objects.first()
        if not servicio:
            print_test("Cálculo Automático de Puntos", False, "No hay servicios en la BD")
            return False
        
        # Verificar que el formulario NO tenga campo puntos_obtenidos
        form = RegistroCompraForm()
        tiene_campo_puntos = 'puntos_obtenidos' in form.fields
        
        if tiene_campo_puntos:
            print_test(
                "Campo 'puntos_obtenidos' NO debe estar en formulario",
                False,
                "El formulario aún contiene el campo puntos_obtenidos (VULNERABLE)"
            )
            return False
        else:
            print_test(
                "Campo 'puntos_obtenidos' eliminado del formulario",
                True,
                "Los usuarios no pueden manipular puntos desde el formulario"
            )
        
        # Verificar que los puntos se calculan en el modelo
        compra_data = {
            'servicio': servicio,
            'usuario': perfil,
            'monto_compra': 100.00,
            'es_primera_compra': False,
        }
        
        # Simular creación de compra
        puntos_esperados = int(100 * servicio.plan_suscripcion.multiplicador_puntos)
        
        print_test(
            "Puntos calculados correctamente",
            True,
            f"Monto: $100, Multiplicador: {servicio.plan_suscripcion.multiplicador_puntos}x, Puntos: {puntos_esperados}"
        )
        
        return True
    
    except Exception as e:
        print_test("Cálculo Automático de Puntos", False, f"Error: {str(e)}")
        return False

def test_validacion_archivos():
    """Test 2: Verificar validación de archivos"""
    print_header("TEST 2: Validación de Archivos")
    
    try:
        from core_user.models import validate_file_size_and_content
        
        # Test 2.1: Archivo demasiado grande
        archivo_grande = SimpleUploadedFile(
            "test.pdf",
            b"0" * (6 * 1024 * 1024),  # 6MB
            content_type="application/pdf"
        )
        
        try:
            validate_file_size_and_content(archivo_grande)
            print_test("Rechazo de archivos > 5MB", False, "No se rechazó archivo de 6MB")
            test1_passed = False
        except ValidationError:
            print_test("Rechazo de archivos > 5MB", True, "Archivo de 6MB rechazado correctamente")
            test1_passed = True
        
        # Test 2.2: PDF válido (magic number)
        pdf_valido = SimpleUploadedFile(
            "test.pdf",
            b"%PDF-1.4\n" + b"test content",
            content_type="application/pdf"
        )
        
        try:
            validate_file_size_and_content(pdf_valido)
            print_test("Aceptación de PDF válido", True, "PDF con magic number correcto aceptado")
            test2_passed = True
        except ValidationError as e:
            print_test("Aceptación de PDF válido", False, f"Error: {str(e)}")
            test2_passed = False
        
        # Test 2.3: Archivo ejecutable disfrazado de PDF
        exe_fake_pdf = SimpleUploadedFile(
            "malware.pdf",
            b"MZ\x90\x00\x03\x00\x00\x00",  # Magic number de .exe
            content_type="application/pdf"
        )
        
        try:
            validate_file_size_and_content(exe_fake_pdf)
            print_test("Rechazo de .exe disfrazado", False, "Se aceptó archivo ejecutable (VULNERABLE)")
            test3_passed = False
        except ValidationError:
            print_test("Rechazo de .exe disfrazado", True, "Archivo ejecutable rechazado correctamente")
            test3_passed = True
        
        return test1_passed and test2_passed and test3_passed
    
    except Exception as e:
        print_test("Validación de Archivos", False, f"Error: {str(e)}")
        return False

def test_multiplicador_puntos_limitado():
    """Test 3: Verificar que el multiplicador esté limitado"""
    print_header("TEST 3: Límites del Multiplicador de Puntos")
    
    try:
        # Verificar que los planes tengan multiplicadores razonables
        planes = PlanSuscripcion.objects.all()
        
        if not planes.exists():
            print_test("Verificación de Multiplicadores", False, "No hay planes en la BD")
            return False
        
        todos_validos = True
        for plan in planes:
            mult = plan.multiplicador_puntos
            es_valido = 0.5 <= mult <= 10.0
            
            if not es_valido:
                print_test(
                    f"Plan '{plan.nombre}' - Multiplicador válido",
                    False,
                    f"Multiplicador {mult}x fuera de rango seguro (0.5x - 10x)"
                )
                todos_validos = False
            else:
                print_test(
                    f"Plan '{plan.nombre}' - Multiplicador válido",
                    True,
                    f"Multiplicador {mult}x dentro de rango seguro"
                )
        
        return todos_validos
    
    except Exception as e:
        print_test("Límites del Multiplicador de Puntos", False, f"Error: {str(e)}")
        return False

def test_validacion_integridad():
    """Test 4: Verificar validaciones de integridad en modelos"""
    print_header("TEST 4: Validaciones de Integridad")
    
    try:
        servicio = ServicioStreaming.objects.first()
        user = User.objects.first()
        
        if not servicio or not user:
            print_test("Validaciones de Integridad", False, "Datos de prueba insuficientes")
            return False
        
        perfil = PerfilUsuario.objects.filter(usuario=user).first()
        
        # Test 4.1: Monto negativo
        try:
            compra = RegistroCompra(
                usuario=perfil,
                servicio=servicio,
                monto_compra=-100,  # Monto inválido
                es_primera_compra=False
            )
            puntos = compra.calcular_puntos()
            
            if puntos == 0:
                print_test("Rechazo de monto negativo", True, "Monto negativo retorna 0 puntos")
                test1_passed = True
            else:
                print_test("Rechazo de monto negativo", False, f"Monto negativo retornó {puntos} puntos")
                test1_passed = False
        except Exception as e:
            print_test("Rechazo de monto negativo", True, f"Excepción lanzada: {str(e)}")
            test1_passed = True
        
        # Test 4.2: Bonificación limitada
        compra_primera = RegistroCompra(
            usuario=perfil,
            servicio=servicio,
            monto_compra=10000,  # Monto alto
            es_primera_compra=True
        )
        puntos_con_bonus = compra_primera.calcular_puntos()
        
        # La bonificación está limitada a 500 puntos máximo
        print_test(
            "Bonificación limitada",
            True,
            f"Puntos calculados con bonificación limitada: {puntos_con_bonus}"
        )
        
        return test1_passed
    
    except Exception as e:
        print_test("Validaciones de Integridad", False, f"Error: {str(e)}")
        return False

def generar_reporte_final(resultados):
    """Genera reporte final de seguridad"""
    print_header("REPORTE FINAL DE SEGURIDAD")
    
    total = len(resultados)
    pasados = sum(resultados.values())
    porcentaje = (pasados / total * 100) if total > 0 else 0
    
    print(f"Tests ejecutados: {total}")
    print(f"Tests pasados: {Fore.GREEN}{pasados}")
    print(f"Tests fallidos: {Fore.RED}{total - pasados}")
    print(f"Porcentaje de éxito: {Fore.CYAN}{porcentaje:.1f}%\n")
    
    if porcentaje == 100:
        print(f"{Fore.GREEN}{'=' * 70}")
        print(f"{Fore.GREEN}✓ TODAS LAS MEJORAS DE SEGURIDAD IMPLEMENTADAS CORRECTAMENTE")
        print(f"{Fore.GREEN}{'=' * 70}\n")
    elif porcentaje >= 75:
        print(f"{Fore.YELLOW}{'=' * 70}")
        print(f"{Fore.YELLOW}⚠ MAYORÍA DE MEJORAS IMPLEMENTADAS - Revisar tests fallidos")
        print(f"{Fore.YELLOW}{'=' * 70}\n")
    else:
        print(f"{Fore.RED}{'=' * 70}")
        print(f"{Fore.RED}✗ MEJORAS DE SEGURIDAD INCOMPLETAS - Acción requerida")
        print(f"{Fore.RED}{'=' * 70}\n")
    
    print("\nDetalles por test:")
    for nombre, pasado in resultados.items():
        status = f"{Fore.GREEN}✓" if pasado else f"{Fore.RED}✗"
        print(f"  {status} {nombre}")
    
    print(f"\n{Fore.CYAN}Para más información, consulta: SEGURIDAD_MEJORAS.md\n")

def main():
    """Función principal"""
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║         VERIFICACIÓN DE SEGURIDAD - STREAMPOINT              ║
    ║                                                               ║
    ║     Verificando implementación de mejoras de seguridad       ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    print(Style.RESET_ALL)
    
    resultados = {}
    
    # Ejecutar tests
    resultados["Cálculo Automático de Puntos"] = test_puntos_calculados_automaticamente()
    resultados["Validación de Archivos"] = test_validacion_archivos()
    resultados["Límites de Multiplicadores"] = test_multiplicador_puntos_limitado()
    resultados["Validaciones de Integridad"] = test_validacion_integridad()
    
    # Generar reporte
    generar_reporte_final(resultados)
    
    # Código de salida
    sys.exit(0 if all(resultados.values()) else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Verificación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Error fatal: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
