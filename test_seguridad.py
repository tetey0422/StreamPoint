#!/usr/bin/env python
"""
Script Simplificado de Verificación de Seguridad - StreamPoint
=============================================================
Verifica que las mejoras de seguridad críticas se hayan implementado.

Uso:
    python test_seguridad.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StreamPoint.settings')
django.setup()

from core_user.forms import RegistroCompraForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

def print_resultado(test_name, passed, details=""):
    """Imprime resultado de un test"""
    status = "[OK]" if passed else "[FAIL]"
    print(f"{status} {test_name}")
    if details:
        print(f"     -> {details}")

def test_campo_puntos_eliminado():
    """Verificar que el formulario NO permita manipular puntos"""
    print("\n" + "="*70)
    print("TEST 1: Campo puntos_obtenidos eliminado del formulario")
    print("="*70)
    
    try:
        form = RegistroCompraForm()
        tiene_campo_puntos = 'puntos_obtenidos' in form.fields
        
        if tiene_campo_puntos:
            print_resultado(
                "Campo puntos_obtenidos eliminado",
                False,
                "VULNERABILIDAD: El formulario permite manipular puntos"
            )
            return False
        else:
            print_resultado(
                "Campo puntos_obtenidos eliminado",
                True,
                "Los usuarios no pueden manipular puntos desde el formulario"
            )
            return True
    
    except Exception as e:
        print_resultado("Campo puntos_obtenidos eliminado", False, f"Error: {str(e)}")
        return False

def test_validacion_tamano_archivos():
    """Verificar validación de tamaño de archivos"""
    print("\n" + "="*70)
    print("TEST 2: Validación de tamaño de archivos (< 5MB)")
    print("="*70)
    
    try:
        from core_user.models import validate_file_size_and_content
        
        # Archivo demasiado grande
        archivo_grande = SimpleUploadedFile(
            "test.pdf",
            b"0" * (6 * 1024 * 1024),  # 6MB
            content_type="application/pdf"
        )
        
        try:
            validate_file_size_and_content(archivo_grande)
            print_resultado("Rechazo de archivos > 5MB", False, "No se rechazó archivo de 6MB")
            return False
        except ValidationError:
            print_resultado("Rechazo de archivos > 5MB", True, "Archivo de 6MB rechazado correctamente")
            return True
    
    except Exception as e:
        print_resultado("Validación de tamaño", False, f"Error: {str(e)}")
        return False

def test_validacion_contenido_archivos():
    """Verificar validación de contenido de archivos (magic numbers)"""
    print("\n" + "="*70)
    print("TEST 3: Validación de contenido de archivos (magic numbers)")
    print("="*70)
    
    try:
        from core_user.models import validate_file_size_and_content
        
        resultados = []
        
        # Test 3.1: PDF válido
        pdf_valido = SimpleUploadedFile(
            "test.pdf",
            b"%PDF-1.4\n" + b"test content",
            content_type="application/pdf"
        )
        
        try:
            validate_file_size_and_content(pdf_valido)
            print_resultado("Aceptación de PDF válido", True, "PDF con magic number correcto aceptado")
            resultados.append(True)
        except ValidationError as e:
            print_resultado("Aceptación de PDF válido", False, f"Error: {str(e)}")
            resultados.append(False)
        
        # Test 3.2: Archivo ejecutable disfrazado de PDF
        exe_fake_pdf = SimpleUploadedFile(
            "malware.pdf",
            b"MZ\x90\x00\x03\x00\x00\x00",  # Magic number de .exe
            content_type="application/pdf"
        )
        
        try:
            validate_file_size_and_content(exe_fake_pdf)
            print_resultado("Rechazo de .exe disfrazado", False, "VULNERABILIDAD: Se aceptó archivo ejecutable")
            resultados.append(False)
        except ValidationError:
            print_resultado("Rechazo de .exe disfrazado", True, "Archivo ejecutable rechazado correctamente")
            resultados.append(True)
        
        return all(resultados)
    
    except Exception as e:
        print_resultado("Validación de contenido", False, f"Error: {str(e)}")
        return False

def test_validadores_en_modelo():
    """Verificar que el modelo tenga los validadores configurados"""
    print("\n" + "="*70)
    print("TEST 4: Validadores configurados en modelo RegistroCompra")
    print("="*70)
    
    try:
        from core_user.models import RegistroCompra
        
        # Verificar que el campo comprobante tenga validadores
        field = RegistroCompra._meta.get_field('comprobante')
        validators = field.validators
        
        if len(validators) > 0:
            print_resultado(
                "Validadores en campo comprobante",
                True,
                f"Se encontraron {len(validators)} validadores configurados"
            )
            
            # Listar validadores
            for validator in validators:
                validator_name = validator.__class__.__name__
                print(f"     - {validator_name}")
            
            return True
        else:
            print_resultado(
                "Validadores en campo comprobante",
                False,
                "No se encontraron validadores"
            )
            return False
    
    except Exception as e:
        print_resultado("Validadores en modelo", False, f"Error: {str(e)}")
        return False

def generar_reporte_final(resultados):
    """Genera reporte final de seguridad"""
    print("\n" + "="*70)
    print("REPORTE FINAL DE SEGURIDAD")
    print("="*70)
    
    total = len(resultados)
    pasados = sum(resultados.values())
    porcentaje = (pasados / total * 100) if total > 0 else 0
    
    print(f"\nTests ejecutados: {total}")
    print(f"Tests pasados: {pasados}")
    print(f"Tests fallidos: {total - pasados}")
    print(f"Porcentaje de éxito: {porcentaje:.1f}%\n")
    
    if porcentaje == 100:
        print("="*70)
        print("[OK] TODAS LAS MEJORAS DE SEGURIDAD IMPLEMENTADAS CORRECTAMENTE")
        print("="*70)
    elif porcentaje >= 75:
        print("="*70)
        print("[WARNING] MAYORÍA DE MEJORAS IMPLEMENTADAS - Revisar tests fallidos")
        print("="*70)
    else:
        print("="*70)
        print("[FAIL] MEJORAS DE SEGURIDAD INCOMPLETAS - Acción requerida")
        print("="*70)
    
    print("\nDetalles por test:")
    for nombre, pasado in resultados.items():
        status = "[OK]" if pasado else "[FAIL]"
        print(f"  {status} {nombre}")
    
    print("\nPara más información, consulta: SEGURIDAD_MEJORAS.md\n")

def main():
    """Función principal"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║       VERIFICACIÓN DE SEGURIDAD - STREAMPOINT                ║
    ║                                                               ║
    ║   Verificando implementación de mejoras de seguridad         ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    resultados = {}
    
    # Ejecutar tests
    resultados["Campo puntos_obtenidos eliminado"] = test_campo_puntos_eliminado()
    resultados["Validación de tamaño de archivos"] = test_validacion_tamano_archivos()
    resultados["Validación de contenido de archivos"] = test_validacion_contenido_archivos()
    resultados["Validadores en modelo"] = test_validadores_en_modelo()
    
    # Generar reporte
    generar_reporte_final(resultados)
    
    # Código de salida
    sys.exit(0 if all(resultados.values()) else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nVerificación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\nError fatal: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
