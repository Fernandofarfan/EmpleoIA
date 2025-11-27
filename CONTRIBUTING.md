# Contributing to EmpleoIA

¡Gracias por tu interés en contribuir a EmpleoIA! 🎉

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo Puedo Contribuir?](#cómo-puedo-contribuir)
- [Guía de Estilo](#guía-de-estilo)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Features](#sugerir-features)

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que mantengas este código. Por favor reportá comportamientos inaceptables abriendo un issue.

## 🤝 ¿Cómo Puedo Contribuir?

### Reportar Bugs

Los bugs se rastrean como [GitHub issues](https://github.com/Fernandofarfan/EmpleoIA/issues). Antes de crear un bug report:

- ✅ Verificá que el bug no haya sido reportado ya
- ✅ Determiná en qué repositorio debería ir el issue
- ✅ Recopilá información sobre el bug

**Template de Bug Report:**

```markdown
**Descripción del Bug**
Una descripción clara y concisa del bug.

**Pasos para Reproducir**
1. Ir a '...'
2. Hacer clic en '...'
3. Scrollear hasta '...'
4. Ver error

**Comportamiento Esperado**
Descripción clara de lo que esperabas que sucediera.

**Screenshots**
Si es aplicable, agregá screenshots.

**Entorno:**
 - OS: [ej. Windows 11]
 - Python Version: [ej. 3.12.0]
 - Browser: [ej. Chrome 120]

**Información Adicional**
Cualquier otro contexto sobre el problema.
```

### Sugerir Features

Los feature requests también se rastrean como GitHub issues. Antes de crear un feature request:

- ✅ Verificá que el feature no haya sido sugerido ya
- ✅ Asegurate de que esté alineado con el scope del proyecto

**Template de Feature Request:**

```markdown
**¿Tu feature request está relacionado con un problema?**
Una descripción clara del problema. Ej: Siempre me frustra cuando [...]

**Describe la solución que te gustaría**
Una descripción clara y concisa de lo que querés que pase.

**Describe alternativas que hayas considerado**
Descripción de soluciones o features alternativos.

**Contexto Adicional**
Agregá cualquier otro contexto o screenshots sobre el feature request.
```

## 🎨 Guía de Estilo

### Python Code Style

- Seguí [PEP 8](https://pep8.org/)
- Usá nombres de variables descriptivos
- Agregá docstrings a funciones y clases
- Mantené las líneas bajo 100 caracteres cuando sea posible

**Ejemplo:**

```python
def scrape_jobs(platform: str, query: str, location: str) -> list:
    """
    Scrape job listings from specified platform.
    
    Args:
        platform: Job platform name ('indeed', 'linkedin', 'bumeran', or 'computrabajo')
        query: Job search query
        location: Job location
        
    Returns:
        List of job dictionaries with 'Apply_URL' for direct applications
        
    Raises:
        ValueError: If platform is not supported
    """
    # Implementation here
    pass
```

### Git Commit Messages

- Usá el tiempo presente ("Add feature" no "Added feature")
- Usá el modo imperativo ("Move cursor to..." no "Moves cursor to...")
- Limitá la primera línea a 72 caracteres
- Referenciá issues y pull requests después de la primera línea

**Prefijos de Commits:**

- `Add:` Nueva funcionalidad
- `Fix:` Corrección de bug
- `Update:` Actualización de funcionalidad existente
- `Remove:` Eliminación de código
- `Refactor:` Refactorización sin cambio de funcionalidad
- `Docs:` Cambios en documentación
- `Style:` Cambios de formato (no afectan el código)
- `Test:` Agregar o modificar tests
- `Chore:` Mantenimiento (actualizar dependencias, etc.)

**Ejemplos:**

```
Add: Bumeran and Computrabajo scrapers with login support
Fix: MySQL connection pool exhaustion
Update: Gemini API to use latest model
Docs: Improve installation instructions
```

### HTML/CSS/JavaScript

- Usá indentación de 2 espacios
- Usá nombres de clases descriptivos (BEM notation cuando sea apropiado)
- Comentá código complejo
- Mantené la accesibilidad (ARIA labels, semantic HTML)

## 🔄 Proceso de Pull Request

1. **Fork** el repositorio
2. **Crea una branch** desde `main`:
   ```bash
   git checkout -b feature/mi-nueva-feature
   ```
3. **Hacé tus cambios** siguiendo la guía de estilo
4. **Agregá tests** si es aplicable
5. **Actualizá la documentación** si es necesario
6. **Commit** tus cambios:
   ```bash
   git commit -m "Add: descripción clara del cambio"
   ```
7. **Push** a tu fork:
   ```bash
   git push origin feature/mi-nueva-feature
   ```
8. **Abrí un Pull Request** en GitHub

### Checklist de Pull Request

Antes de enviar tu PR, asegurate de que:

- [ ] El código sigue la guía de estilo del proyecto
- [ ] Has agregado tests que prueban tus cambios
- [ ] Todos los tests pasan localmente
- [ ] Has actualizado la documentación
- [ ] Tu commit message sigue las convenciones
- [ ] Has agregado comentarios en código complejo
- [ ] No hay conflictos con la branch `main`

### Review Process

1. Un maintainer revisará tu PR
2. Pueden solicitar cambios o mejoras
3. Una vez aprobado, será merged a `main`
4. Tu contribución aparecerá en el próximo release

## 🧪 Testing

Antes de enviar un PR, ejecutá los tests:

```bash
# Ejecutar todos los tests
python -m pytest

# Ejecutar tests específicos
python -m pytest tests/test_scraper.py

# Con coverage
python -m pytest --cov=.
```

## 📝 Documentación

Si tu contribución agrega o modifica funcionalidad:

- Actualizá el README.md
- Agregá docstrings a funciones/clases nuevas
- Actualizá el CHANGELOG.md
- Considerá agregar ejemplos de uso

## 🎯 Áreas de Contribución

Algunas áreas donde podés contribuir:

### 🔴 Alta Prioridad
- Mejorar detección anti-bot en scrapers
- Agregar más plataformas de scraping (Glassdoor, ZipRecruiter)
- Optimizar performance de base de datos
- Agregar tests unitarios

### 🟡 Media Prioridad
- Mejorar UI/UX del frontend
- Agregar soporte para más idiomas
- Implementar sistema de notificaciones
- Agregar analytics de búsqueda

### 🟢 Baja Prioridad
- Mejorar documentación
- Agregar más ejemplos
- Refactorizar código legacy
- Optimizar imports

## 💬 Preguntas

Si tenés preguntas sobre cómo contribuir:

- Abrí un [GitHub Discussion](https://github.com/Fernandofarfan/EmpleoIA/discussions)
- Comentá en un issue existente
- Contactá a los maintainers

## 🙏 Reconocimientos

Todos los contribuidores serán agregados al README.md y al archivo CONTRIBUTORS.md.

---

**¡Gracias por contribuir a EmpleoIA!** 🚀
