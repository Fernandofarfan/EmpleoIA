<div align="center">

# 🤖 EmpleoIA

### *Plataforma Inteligente de Búsqueda de Empleo con IA*

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Gemini AI](https://img.shields.io/badge/AI-Google%20Gemini-4285F4.svg)](https://ai.google.dev/)

*Automatizá tu búsqueda laboral con scraping inteligente y optimización de CVs potenciada por IA*

[Características](#-características) •
[Instalación](#-instalación-rápida) •
[Uso](#-guía-de-uso) •
[Documentación](#-documentación) •
[Contribuir](#-contribuir)

</div>

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos](#-requisitos-previos)
- [Instalación Rápida](#-instalación-rápida)
- [Guía de Uso](#-guía-de-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Configuración](#-configuración)
- [Solución de Problemas](#-solución-de-problemas)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)
- [Créditos](#-créditos)

---

## 🎯 Descripción

**EmpleoIA** es una plataforma integral de automatización de búsqueda de empleo que combina web scraping inteligente con optimización de currículums potenciada por IA. Diseñada para profesionales que buscan optimizar su proceso de búsqueda laboral.

### ¿Qué hace diferente a EmpleoIA?

- ✅ **Scraping sin APIs**: Extrae ofertas de Indeed y LinkedIn sin costos de API
- ✅ **IA Integrada**: Usa Google Gemini Pro para optimizar CVs con 90%+ de compatibilidad ATS
- ✅ **Gestión Completa**: Desde la búsqueda hasta el seguimiento de postulaciones
- ✅ **100% en Español**: Interfaz completamente localizada para Argentina/Latinoamérica
- ✅ **Open Source**: Código abierto y personalizable

---

## ✨ Características

### 🔍 **Scraping Multi-Plataforma**
- Búsqueda automatizada en **Indeed** y **LinkedIn**
- Filtrado inteligente por habilidades, ubicación y nivel de experiencia
- Exportación a CSV para análisis posterior
- Sistema anti-detección para scraping confiable

### 🤖 **Optimización de CVs con IA**
- Generación de currículums adaptados usando **Google Gemini Pro**
- Optimización para sistemas ATS (Applicant Tracking Systems)
- Análisis de compatibilidad con descripciones de trabajo
- Procesamiento por lotes para múltiples aplicaciones

### 📊 **Sistema de Seguimiento (Job Tracker)**
- Tablero Kanban para gestionar postulaciones
- Estados: Guardados → Aplicando → Aplicados → Entrevistando → Negociando → Aceptados
- Notas y recordatorios personalizados
- Métricas de progreso

### 👤 **Gestión de Perfiles**
- Soporte para múltiples perfiles profesionales
- Extracción automática de habilidades desde CVs
- Almacenamiento seguro de credenciales
- Historial de postulaciones

### 📝 **Generación de Cartas de Presentación**
- Creación automática con IA
- Personalización según empresa y puesto
- Plantillas profesionales
- Exportación a DOCX

---

## 🛠 Tecnologías

<table>
<tr>
<td align="center" width="25%">
<img src="https://www.python.org/static/community_logos/python-logo.png" width="60px" height="60px" alt="Python" />
<br><strong>Python 3.12</strong>
<br><sub>Backend</sub>
</td>
<td align="center" width="25%">
<img src="https://flask.palletsprojects.com/en/2.3.x/_images/flask-logo.png" width="60px" height="60px" alt="Flask" />
<br><strong>Flask 2.3</strong>
<br><sub>Web Framework</sub>
</td>
<td align="center" width="25%">
<img src="https://www.selenium.dev/images/selenium_logo_square_green.png" width="60px" height="60px" alt="Selenium" />
<br><strong>Selenium</strong>
<br><sub>Web Scraping</sub>
</td>
<td align="center" width="25%">
<img src="https://ai.google.dev/static/site-assets/images/share.png" width="60px" height="60px" alt="Gemini" />
<br><strong>Gemini Pro</strong>
<br><sub>IA Generativa</sub>
</td>
</tr>
<tr>
<td align="center" width="25%">
<img src="https://www.mysql.com/common/logos/logo-mysql-170x115.png" width="60px" height="60px" alt="MySQL" />
<br><strong>MySQL</strong>
<br><sub>Base de Datos</sub>
</td>
<td align="center" width="25%">
<img src="https://getbootstrap.com/docs/5.3/assets/brand/bootstrap-logo-shadow.png" width="60px" height="60px" alt="Bootstrap" />
<br><strong>Bootstrap 5</strong>
<br><sub>UI Framework</sub>
</td>
<td align="center" width="25%">
<img src="https://upload.wikimedia.org/wikipedia/commons/6/6a/JavaScript-logo.png" width="60px" height="60px" alt="JavaScript" />
<br><strong>JavaScript</strong>
<br><sub>Frontend</sub>
</td>
<td align="center" width="25%">
<img src="https://www.docker.com/wp-content/uploads/2022/03/vertical-logo-monochromatic.png" width="60px" height="60px" alt="Docker" />
<br><strong>Docker</strong>
<br><sub>Containerización</sub>
</td>
</tr>
</table>

---

## 📦 Requisitos Previos

Antes de comenzar, asegurate de tener instalado:

- ✅ **Python 3.12+** - [Descargar](https://www.python.org/downloads/)
- ✅ **MySQL 8.0+** - [Descargar](https://dev.mysql.com/downloads/)
- ✅ **Google Chrome** - Para Selenium WebDriver
- ✅ **Git** - Para clonar el repositorio
- ✅ **API Key de Google Gemini** - [Obtener gratis](https://makersuite.google.com/app/apikey)

---

## 🚀 Instalación Rápida

### Opción 1: Instalación Manual

```bash
# 1. Clonar el repositorio
git clone https://github.com/Fernandofarfan/EmpleoIA.git
cd EmpleoIA

# 2. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Instalar modelo de spaCy (IMPORTANTE)
python -m spacy download en_core_web_sm

# 5. Configurar base de datos MySQL
mysql -u root -p < setup_database.sql
# O ejecutar manualmente:
# CREATE DATABASE job_tracker;
# USE job_tracker;
# (copiar y ejecutar el contenido de setup_database.sql)

# 6. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales:
# - GEMINI_API_KEY: Tu API key de Google Gemini
# - DB_PASSWORD: Tu contraseña de MySQL
# - (Opcional) Credenciales de Indeed y LinkedIn

# 7. Ejecutar la aplicación
python app.py
```

### Opción 2: Docker (Próximamente)

```bash
docker-compose up -d
```

### 🌐 Acceder a la Aplicación

Abrí tu navegador en: **http://localhost:5000**

---

## 📖 Guía de Uso

### 1️⃣ Configuración Inicial

#### Cargar tu Currículum
1. Navegá a **Perfil** en el menú
2. Seleccioná tu tipo de rol (Data Analyst, Software Engineer, etc.)
3. Subí tu CV en formato PDF o DOCX
4. El sistema extraerá automáticamente tus habilidades

#### Configurar API de Gemini
1. Obtené tu API key en [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Agregala en el archivo `.env`:
   ```env
   GEMINI_API_KEY=tu_api_key_aqui
   ```

### 2️⃣ Buscar Empleos

#### 🔵 LinkedIn
1. Andá a **Buscar Empleos** → Pestaña LinkedIn
2. Ingresá puesto y ubicación
3. **Obtener token `li_at`**:
   - Iniciá sesión en LinkedIn
   - Presioná `F12` (DevTools)
   - Application → Cookies → `li_at`
   - Copiá el valor
4. Hacé clic en **Iniciar Scraper**

#### 🟢 Indeed
1. Andá a **Buscar Empleos** → Pestaña Indeed
2. Ingresá credenciales (o configuralas en `.env`)
3. Seleccioná puesto, ubicación y páginas
4. Hacé clic en **Iniciar Scraper**

### 3️⃣ Optimizar Currículums

1. Andá a **Resultados**
2. Seleccioná un archivo CSV
3. Hacé clic en **Optimización por Lotes**
4. Los CVs optimizados se guardan en `temp/resumes/`

### 4️⃣ Seguimiento de Aplicaciones

1. Andá a **Seguimiento**
2. Agregá trabajos desde resultados o manualmente
3. Arrastrá y soltá entre columnas del Kanban
4. Agregá notas y fechas de seguimiento

---

## 📁 Estructura del Proyecto

```
EmpleoIA/
│
├── 📂 scrapers/              # Módulos de web scraping
│   ├── indeed_scraper.py     # Scraper de Indeed
│   ├── linkedin_scraper.py   # Scraper de LinkedIn
│   └── linkedin_connection.py # Bot de conexiones
│
├── 📂 templates/             # Plantillas HTML (Frontend)
│   ├── base.html             # Plantilla base
│   ├── index.html            # Página principal
│   ├── scraper.html          # Interfaz de scraping
│   ├── results.html          # Visualización de resultados
│   ├── job_tracker.html      # Tablero Kanban
│   └── profile.html          # Gestión de perfiles
│
├── 📂 uploads/               # CVs subidos por usuarios
├── 📂 results/               # Datos scrapeados (CSV)
├── 📂 profiles/              # Perfiles de usuario
├── 📂 temp/resumes/          # CVs optimizados generados
├── 📂 logs/                  # Logs de la aplicación
│
├── 📄 app.py                 # Aplicación principal Flask
├── 📄 db_config.py           # Configuración de MySQL
├── 📄 resume_parser.py       # Parser de CVs
├── 📄 simple_resume_optimizer.py # Optimizador con IA
├── 📄 job_precheck.py        # Filtrado inteligente
├── 📄 cover_letter_generator.py # Generador de cartas
├── 📄 MASTER_RESUME_PROMPT.py # Prompts para Gemini
│
├── 📄 requirements.txt       # Dependencias Python
├── 📄 setup_database.sql     # Script de BD
├── 📄 .env.example           # Plantilla de configuración
├── 📄 .gitignore             # Archivos ignorados
└── 📄 README.md              # Este archivo
```

---

## ⚙️ Configuración

### Variables de Entorno (.env)

Creá un archivo `.env` en la raíz del proyecto copiando `.env.example`:

```bash
cp .env.example .env
```

Luego editá el archivo `.env` con tus credenciales:

```env
# Google Gemini API (OBLIGATORIO)
GEMINI_API_KEY=tu_api_key_aqui

# MySQL Database (OBLIGATORIO)
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_NAME=job_tracker

# Indeed Scraper - Credenciales de Google (Opcional)
# El scraper de Indeed usa autenticación de Google
INDEED_EMAIL=tu_email_google@gmail.com
INDEED_PASSWORD=tu_password_google

# LinkedIn Token (Opcional)
LINKEDIN_TOKEN=tu_token_li_at
```

> [!IMPORTANT]
> **Nunca subas el archivo `.env` al repositorio**. Este archivo contiene tus credenciales personales y está incluido en `.gitignore`.

> [!TIP]
> **Verificación en 2 pasos (2FA) para Indeed**: Si tenés 2FA activada en tu cuenta de Google, deberás aprobar el inicio de sesión en tu celular cuando arranque el scraper. Alternativamente, podés crear una [contraseña de aplicación](https://support.google.com/accounts/answer/185833) en tu cuenta de Google.

### Obtener API Key de Gemini

1. Andá a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Iniciá sesión con tu cuenta de Google
3. Hacé clic en "Create API Key"
4. Copiá la key y pegala en tu archivo `.env`

---

## 🔧 Solución de Problemas

### ❌ Error: "MySQL connection failed"
**Solución:**
```bash
# Verificar que MySQL esté corriendo
mysql -u root -p

# Crear la base de datos manualmente
CREATE DATABASE job_tracker;
```

### ❌ LinkedIn no encuentra empleos
**Causas comunes:**
- Token `li_at` expirado (renovar cada ~1 año)
- LinkedIn detectó scraping excesivo (esperar 24h)
- Búsqueda demasiado amplia (ser más específico)

### ❌ Indeed requiere 2FA
**Solución:**
- Desactivar 2FA temporalmente en Indeed
- O usar credenciales de una cuenta sin 2FA

### ❌ Error de Gemini API
**Verificar:**
```bash
# Probar la API key
curl -H "Content-Type: application/json" \
     -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
     "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=TU_API_KEY"
```

### ❌ Archivos CSV no aparecen
**Solución:**
```bash
# Verificar permisos de carpeta
chmod 755 results/

# Verificar logs
tail -f logs/app.log
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Seguí estos pasos:

1. **Fork** el repositorio
2. Creá una **branch** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add: Amazing Feature'`)
4. **Push** a la branch (`git push origin feature/AmazingFeature`)
5. Abrí un **Pull Request**

### Guías de Contribución

- Seguí el estilo de código existente
- Agregá tests para nuevas funcionalidades
- Actualizá la documentación
- Escribí mensajes de commit descriptivos

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👥 Créditos

### Desarrollador

- **Fernando Farfan** - Desarrollo y mantenimiento principal
- GitHub: [@Fernandofarfan](https://github.com/Fernandofarfan)

Proyecto desarrollado desde cero para automatizar la búsqueda de empleo con tecnologías modernas de IA.

### Tecnologías

- **IA**: [Google Gemini Pro](https://ai.google.dev/)
- **Web Scraping**: [Selenium](https://www.selenium.dev/)
- **Framework**: [Flask](https://flask.palletsprojects.com/)
- **UI**: [Bootstrap 5](https://getbootstrap.com/)

---

## 📞 Soporte

¿Tenés preguntas o problemas?

- 📧 **Email**: fernando.farfan16@gmail.com
- 💬 **Issues**: [GitHub Issues](https://github.com/Fernandofarfan/EmpleoIA/issues)
- 📖 **Wiki**: [Documentación Completa](https://github.com/Fernandofarfan/EmpleoIA/wiki)

---

<div align="center">

### ⭐ Si te resultó útil, dejá una estrella!

**Hecho con ❤️ en Argentina**

[⬆ Volver arriba](#-empleoia)

</div>
