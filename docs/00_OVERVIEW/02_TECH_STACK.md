# 02_TECH_STACK.md

# Stack Tecnológico

# 🐍 Backend

## Python 3.13

Lenguaje principal del proyecto.

Se utiliza como base para:

- backend web
- lógica de negocio
- realtime
- autorización
- renderizado SSR
- automatización
- testing

---

## FastAPI

Framework principal de backend.

La plataforma utiliza FastAPI como núcleo arquitectónico para:

- SSR routes
- REST APIs
- WebSockets
- dependency injection
- middleware
- authentication
- realtime communication

---

## SQLAlchemy

ORM principal del sistema.

Uso actual:

- modelos relacionales
- relationships
- eager loading
- query optimization
- ownership/context queries
- transactional workflows

---

## MariaDB

Base de datos relacional principal.

Actualmente utilizada para:

- IAM
- RBAC
- proyectos
- tareas
- actividades
- auditoría
- notificaciones
- adjuntos

---

## Pydantic

Validación y serialización de datos.

Uso:

- schemas
- DTOs
- validación de entrada
- respuestas API

---

# 🔐 Seguridad

## JWT Authentication

Sistema principal de autenticación.

Implementado mediante:

- access tokens
- refresh tokens
- JWT payload permissions
- expiración controlada

---

## HTTPOnly Cookies

Los tokens se almacenan mediante cookies seguras.

Ventajas:

- protección frente a XSS
- SSR integration
- persistencia segura

---

## SessionMiddleware

Utilizado para:

- flash messages
- toast notifications
- estado temporal SSR
- mensajes transitorios UI

Actualmente integrado mediante:

```python
from starlette.middleware.sessions import SessionMiddleware
```

---

# 🔐 RBAC + Contextual Authorization
La plataforma utiliza autorización híbrida:

### Global RBAC
- roles
- permissions
- policies

### Contextual Authorization
Validaciones dinámicas basadas en:
- ownership
- project coordinators
- resource permissions
- entity relationships

### bcrypt
- Hash seguro de contraseñas.

# 🌐 Frontend SSR

### Jinja2
Motor principal de renderizado server-side.
**Uso:**
- templates
- macros reutilizables
- partial rendering
- contextual UI
- permission-aware rendering

### Bootstrap 4/5
Sistema base responsive.
**Uso:**
- grid system
- forms
- layout
- utilities
- responsive UI

### AdminLTE
Base visual administrativa enterprise-style. Actualmente proporciona:
- layout administrativo
- sidebars
- cards
- dashboard structure
- widgets base

### Font Awesome
Sistema principal de iconografía. Uso intensivo en:
- navegación
- dashboards
- acciones
- timelines
- auditoría
- botones contextuales

# ⚡ Arquitectura JavaScript
La plataforma utiliza una arquitectura JS modular organizada por dominios funcionales.

### Modular JS Architecture
Estructura basada en:
```text
static/js/
├── core/
├── dashboard/
├── kanban/
├── projects/
├── tasks/
├── activities/
└── notifications/
```

### Core JS
Incluye funcionalidades reutilizables:
- toast system
- confirm dialogs
- flash handlers
- websocket clients
- reusable utilities

### Toast Notification System
Sistema centralizado de notificaciones UI.
Características:
- SSR compatible
- autoclose
- categories
- reusable rendering
- session flash integration

### Reusable Confirm Dialog System
Reemplazo progresivo de confirm() nativos.
Basado en:
- data-confirm
- reusable modal dialogs
- centralized handlers

## 📡 Realtime Architecture

### FastAPI WebSockets
La plataforma incorpora realtime mediante WebSockets.
Uso actual:
- dashboard sync
- notifications
- timelines
- realtime updates

### WebSocket Rooms
La arquitectura ya soporta segmentación lógica tipo “rooms”.
Ejemplos:
- dashboard channels
- project channels
- user-specific notifications

Preparado para:
- collaborative editing
- realtime Kanban
- user presence

## 📊 Visualización de Datos

### Chart.js
Utilizado en dashboards y métricas.
Uso actual:
- activity charts
- user statistics
- project metrics
- realtime visual indicators

## 🎨 Arquitectura CSS
La plataforma utiliza una arquitectura CSS modular.

### Foundation Layer
- base.css
- layout.css
- utilities.css

Responsabilidades:
- reset
- spacing
- typography
- layout primitives

### Design System Layer
- components.css
- forms.css
- tables.css
- buttons.css

Incluye:
- reusable cards
- forms
- tables
- badges
- buttons
- alerts
- toasts

### Feature-oriented CSS
CSS organizado por dominio funcional.
Ejemplos:
- dashboard.css
- projects.css
- tasks.css
- activities.css
- kanban.css
- notifications.css

## 🧩 Arquitectura Backend

### Core Layer
Infraestructura transversal reutilizable.
`app/core/`

Incluye:
- security
- middleware
- websocket
- authorization
- constants
- template context
- flash system
- utilities

### Modular Domain Architecture
La plataforma sigue arquitectura modular por dominios.
`modules/`

Dominios actuales:
- auth
- users
- roles
- identities
- projects
- tasks
- activities
- audit
- notifications
- activity_feed
- auth_saml

## 🧪 Testing Stack
- pytest (Framework principal de testing)
- pytest-cov (Cobertura de tests)
- Ruff (Linting y calidad de código)

### Testing Goals
Objetivos actuales:
- services
- permissions
- authorization
- realtime
- websocket workflows

## ⚙️ Tooling y Dev Environment

### uv
Gestión moderna de entorno y dependencias Python.
Uso actual:
- dependency management
- virtual environments
- execution workflows

Ejemplo:
```bash
uv run uvicorn app.main:app --reload
```

### GitHub
Control de versiones principal.

### GitHub Actions
CI/CD pipeline.
Actualmente utilizado para:
- linting
- testing
- quality checks
- validation workflows

### SonarCloud
Análisis estático y calidad de código.
Uso:
- maintainability
- code smells
- coverage analysis
- technical debt tracking

## 📚 APIs y Documentación
### Swagger / OpenAPI
Documentación automática FastAPI.
Disponible para APIs REST del sistema.

## 🚀 Infraestructura Futura
### Docker
Previsto para:
- despliegue
- entornos reproducibles
- desarrollo aislado

### Alembic
Previsto para:
- migraciones SQLAlchemy
- versionado DB

## 🏁 Resumen Técnico
La plataforma utiliza una arquitectura moderna SSR-first centrada en:
- seguridad
- modularidad
- realtime
- maintainability
- reusable UI
- enterprise workflows

combinando FastAPI, SSR rendering y realtime communication bajo una arquitectura progresivamente escalable.