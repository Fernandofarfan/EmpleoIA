# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

### Planeado
- Mejoras en el UI de la página de scrapers
- Soporte para Docker
- Tests unitarios completos
- CI/CD con GitHub Actions
- Dashboard de analytics

## [1.2.0] - 2025-11-27

### Added
- ✨ **Scraper Universal**: Ejecuta Computrabajo y Bumeran simultáneamente
- ✨ Consolidación de resultados en un solo CSV con columna "Fuente"
- ✨ Seguimiento en tiempo real del estado de cada scraper
- ✨ UI mejorada con badges de estado por plataforma
- ✨ Configuración automática de credenciales desde `.env` para LinkedIn

### Changed
- 🔄 LinkedIn token ahora se lee automáticamente del `.env`
- 🔄 Scraper Universal optimizado para solo Computrabajo y Bumeran

### Removed
- 🗑️ Eliminados scrapers de ZonaJobs y Jooble (problemas de compatibilidad)
- 🗑️ Archivos temporales de desarrollo limpiados

### Fixed
- 🐛 Corrección de errores en la lectura de credenciales
- 🐛 Mejoras en el manejo de errores del scraper universal

## [1.1.0] - 2025-11-26

### Added
- ✨ Soporte completo para **Bumeran** y **Computrabajo**
- ✨ Sistema de **Login Automático** para portales de empleo
- ✨ **Deep Scraping**: Extracción de enlaces directos de postulación ("Apply URL")
- ✨ Nuevo botón "Apply" en la interfaz de resultados
- ✨ Mejoras en la organización de archivos CSV exportados

### Fixed
- 🐛 Corrección de selectores CSS para Bumeran
- 🐛 Solución a problemas de carga dinámica con React
- 🐛 Manejo de errores 403 en login de Computrabajo

## [1.0.0] - 2025-01-25

### Added
- ✨ Plataforma completa de búsqueda de empleo con IA
- ✨ Scraping de Indeed y LinkedIn
- ✨ Optimización de CVs con Google Gemini Pro
- ✨ Sistema de Job Tracker con Kanban board
- ✨ Generador de cartas de presentación con IA
- ✨ Soporte para múltiples perfiles profesionales
- ✨ Bot de conexiones automáticas de LinkedIn
- ✨ Sistema de filtrado inteligente de empleos
- ✨ Optimización por lotes de currículums
- 📝 Documentación profesional completa
- 📝 README.md con badges y guías
- 📝 CONTRIBUTING.md con guías de contribución
- 📝 CHANGELOG.md para tracking de cambios

### Technical
- 🔄 Backend con Flask y Python 3.12
- 🔄 Base de datos MySQL
- 🔄 UI con Bootstrap 5.3
- 🔄 Integración con Google Gemini Pro API
- � Web scraping con Selenium

### Security
- 🔒 Implementación de gitignore para credenciales
- 🔒 Encriptación de tokens de LinkedIn
- 🔒 Sanitización de inputs de usuario
- 🔒 Gestión segura de API keys

---

## Tipos de Cambios

- `Added` - Nuevas funcionalidades
- `Changed` - Cambios en funcionalidades existentes
- `Deprecated` - Funcionalidades que serán removidas
- `Removed` - Funcionalidades removidas
- `Fixed` - Corrección de bugs
- `Security` - Cambios de seguridad

## Emojis Usados

- ✨ Nueva funcionalidad
- 🐛 Bug fix
- 🔒 Seguridad
- 🔄 Cambio/Actualización
- 📝 Documentación
- 🎨 UI/Estilo
- ⚡ Performance
- 🧪 Tests
- 🔧 Configuración
- 🗑️ Deprecación/Remoción
