# Guía de Contribución a StreamPoint

¡Gracias por tu interés en contribuir a StreamPoint! 🎉

## Código de Conducta

Este proyecto se adhiere a un código de conducta que todos los contribuidores deben seguir:
- Ser respetuoso con otros contribuidores
- Aceptar críticas constructivas
- Enfocarse en lo que es mejor para la comunidad

## ¿Cómo puedo contribuir?

### Reportar Bugs 🐛

Si encuentras un bug, por favor:

1. Verifica que el bug no haya sido reportado anteriormente en [Issues](https://github.com/tetey0422/StreamPoint/issues)
2. Si no existe, crea un nuevo issue incluyendo:
   - Descripción clara y concisa del problema
   - Pasos para reproducir el bug
   - Comportamiento esperado vs. comportamiento actual
   - Screenshots si es posible
   - Versión de Python y Django que estás usando

### Sugerir Mejoras 💡

Las sugerencias son bienvenidas. Crea un issue con:
- Descripción detallada de la mejora propuesta
- Casos de uso donde sería útil
- Mockups o ejemplos si aplica

### Pull Requests

1. **Fork el repositorio**
   ```bash
   git clone https://github.com/tetey0422/StreamPoint.git
   ```

2. **Crea una rama para tu feature**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

3. **Realiza tus cambios**
   - Sigue las convenciones de código de Django
   - Escribe código limpio y documentado
   - Agrega comentarios donde sea necesario

4. **Asegúrate que todo funcione**
   ```bash
   python manage.py check
   python manage.py test  # Si hay tests
   ```

5. **Commit tus cambios**
   ```bash
   git add .
   git commit -m "Add: descripción breve de los cambios"
   ```
   
   Usa prefijos en los commits:
   - `Add:` para nuevas funcionalidades
   - `Fix:` para corrección de bugs
   - `Update:` para actualizaciones
   - `Refactor:` para refactorización de código
   - `Docs:` para cambios en documentación

6. **Push a tu fork**
   ```bash
   git push origin feature/nueva-funcionalidad
   ```

7. **Abre un Pull Request**
   - Describe los cambios realizados
   - Referencia issues relacionados si los hay
   - Espera feedback del mantenedor

## Estilo de Código

### Python/Django

- Sigue [PEP 8](https://pep8.org/)
- Usa nombres descriptivos para variables y funciones
- Máximo 79 caracteres por línea (120 aceptable en casos especiales)
- Usa docstrings para funciones y clases

```python
def calcular_puntos(monto, tipo_transaccion):
    """
    Calcula los puntos a otorgar según el monto y tipo de transacción.
    
    Args:
        monto (float): Monto de la transacción en COP
        tipo_transaccion (str): 'primera_compra' o 'renovacion'
    
    Returns:
        int: Cantidad de puntos a otorgar
    """
    # Implementación
```

### HTML/Templates

- Indentación de 4 espacios
- Usa clases de Bootstrap cuando sea posible
- Separa lógica de presentación

### CSS

- Usa variables CSS para colores y valores reutilizables
- Organiza por secciones con comentarios
- Mobile-first approach

### JavaScript

- Usa ES6+ cuando sea posible
- Evita jQuery, prefiere vanilla JS
- Comenta código complejo

## Estructura de Commits

Ejemplo de buen commit:
```
Add: sistema de notificaciones por email

- Implementa envío de emails para vencimientos
- Agrega templates de email
- Configura backend de email en settings
- Actualiza documentación

Closes #42
```

## Testing

Si agregas nuevas funcionalidades, por favor incluye tests:

```python
from django.test import TestCase

class TestSistemaRecompensas(TestCase):
    def test_calcular_puntos_primera_compra(self):
        # Test implementation
        pass
```

## Documentación

- Actualiza el README si es necesario
- Documenta nuevas funcionalidades
- Actualiza comentarios en el código

## Preguntas

Si tienes preguntas, puedes:
- Abrir un issue con la etiqueta "question"
- Contactar al mantenedor del proyecto

---

¡Gracias por contribuir a StreamPoint! 🚀
