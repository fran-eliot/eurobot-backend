# 🤖 Aula Robótica Platform

![Python](https://img.shields.io/badge/python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-success)
![Coverage](https://img.shields.io/badge/coverage-75%25-brightgreen)
![Tests](https://github.com/fran-eliot/aula-robotica-platform/actions/workflows/tests.yml/badge.svg)

Plataforma web modular desarrollada para la gestión colaborativa del **Aula de Robótica de la Escuela Politécnica Superior de la Universidad de Alcalá (UAH)**.

El proyecto integra:

* gestión de usuarios e identidades,
* autenticación y autorización avanzada,
* control de acceso RBAC contextual,
* gestión colaborativa de proyectos,
* tareas Kanban realtime,
* auditoría,
* notificaciones,
* dashboard administrativo,
* arquitectura preparada para SAML/SSO institucional.

Desarrollado como **Proyecto Final del CFGS DAM (Desarrollo de Aplicaciones Multiplataforma)** con enfoque profesional en:

* arquitectura backend,
* seguridad,
* testing,
* realtime,
* calidad software,
* mantenibilidad,
* escalabilidad.

---

# 📚 Tabla de contenidos

* Visión general
* Características principales
* Arquitectura del sistema
* Stack tecnológico
* Funcionalidades
* Sistema IAM y seguridad
* Realtime y WebSockets
* Calidad software
* Testing y cobertura
* Estructura del proyecto
* Modelo de datos
* Instalación y ejecución
* Docker y despliegue
* API y documentación
* Roadmap futuro
* Documentación adicional
* Autor

---

# 🚀 Visión general

Aula Robótica Platform no es únicamente un CRUD administrativo.

El sistema ha sido diseñado como una plataforma extensible para soportar:

* operaciones internas del Aula de Robótica,
* coordinación de proyectos,
* trabajo colaborativo,
* gestión académica,
* seguimiento de actividades,
* competiciones como Eurobot Spain,
* integración futura con sistemas institucionales.

La aplicación sigue una arquitectura modular orientada a separar claramente:

* presentación,
* lógica de negocio,
* persistencia,
* seguridad,
* realtime.

---

# ✨ Características principales

## 🔐 Seguridad e IAM

* Autenticación JWT
* Cookies HTTPOnly
* RBAC contextual
* Roles globales y contextuales
* Sistema granular de permisos
* Middleware de autenticación
* Protección SSR y API
* Auditoría completa
* Arquitectura preparada para SAML/SSO

## 📊 Dashboard administrativo

* Métricas globales
* Feed de actividad
* Logs recientes
* Estadísticas de proyectos
* Estado de tareas
* Métricas contextuales por usuario

## 👥 Gestión de usuarios

* CRUD completo
* Activación/desactivación
* Roles y permisos efectivos
* Visualización contextual
* Auditoría integrada

## 🔑 Gestión de identidades

* Identidades desacopladas del usuario
* Soporte multi-provider
* Arquitectura preparada para OAuth/SAML
* Asociación flexible usuario-identidad

## 📁 Gestión de proyectos

* Creación y edición
* Miembros y coordinadores
* Gestión colaborativa
* Feed de actividad
* Métricas por proyecto

## ✅ Gestión de tareas

* Kanban realtime
* Prioridades
* Estados
* Asignaciones
* Auditoría de cambios
* Actualización sincronizada mediante WebSockets

## 🔔 Notificaciones

* Sistema realtime
* Notificaciones contextuales
* Marcado de lectura
* Integración con tareas y proyectos

## 🧾 Auditoría

Registro centralizado de:

* login/logout,
* acciones CRUD,
* cambios críticos,
* operaciones de seguridad,
* actividad del sistema.

---

# 🏗️ Arquitectura del sistema

El proyecto utiliza una arquitectura modular multicapa.

```text
┌──────────────────────────────┐
│        Frontend SSR          │
│ Jinja2 + AdminLTE + Bootstrap│
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         FastAPI Routers      │
│ SSR + API REST + WebSockets  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        Service Layer         │
│ Business Logic / IAM / RBAC  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     SQLAlchemy ORM Layer     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         MariaDB DB           │
└──────────────────────────────┘
```

## Arquitectura híbrida

La aplicación combina:

* SSR tradicional mediante Jinja2,
* API REST,
* comunicación realtime mediante WebSockets.

Esto permite:

* rapidez de desarrollo,
* buena experiencia de usuario,
* simplicidad operativa,
* realtime sin SPA compleja.

---

# 🧱 Stack tecnológico

## Backend

* Python 3.13
* FastAPI
* SQLAlchemy ORM
* MariaDB
* Uvicorn

## Frontend

* Jinja2
* AdminLTE
* Bootstrap
* Chart.js
* SweetAlert2

## Seguridad

* JWT
* Cookies HTTPOnly
* bcrypt
* RBAC contextual
* Middleware de autenticación

## Realtime

* WebSockets
* Broadcast de eventos
* Sincronización Kanban

## Calidad software

* Pytest
* Ruff
* SonarQube Cloud
* GitHub Actions
* Coverage

## Infraestructura

* Docker
* uv
* GitHub
* CI/CD

---

# ⚙️ Funcionalidades

# 1. Sistema IAM

El sistema implementa un modelo IAM completo basado en:

* usuarios,
* identidades,
* roles,
* permisos,
* ownership,
* contexto de proyecto.

## Roles principales

* Administrador
* Profesor
* Coordinador
* Estudiante

## Control de acceso

El acceso se valida tanto:

* en backend,
* como en frontend SSR.

Esto incluye:

* menús dinámicos,
* botones condicionales,
* validación de acciones,
* ownership,
* permisos efectivos.

---

# 2. Dashboard

El dashboard muestra información diferente según el usuario.

## Administradores

* usuarios,
* roles,
* identidades,
* actividad reciente,
* auditoría,
* estadísticas globales.

## Usuarios contextuales

* proyectos asignados,
* tareas,
* progreso,
* feed de actividad,
* notificaciones.

---

# 3. Gestión de proyectos

Cada proyecto puede incluir:

* miembros,
* coordinadores,
* tareas,
* actividades,
* notificaciones,
* feed de actividad.

## Características

* roles contextuales,
* colaboración,
* seguimiento,
* realtime.

---

# 4. Sistema Kanban

El sistema Kanban soporta:

* drag & drop,
* realtime,
* sincronización automática,
* persistencia inmediata.

## Estados

* To Do
* Doing
* Done

## Flujo realtime

```text
Cliente A
   │
   ▼
Drag & Drop
   │
   ▼
Backend valida permisos
   │
   ▼
DB Update
   │
   ▼
Broadcast WebSocket
   │
   ▼
Clientes sincronizados
```

---

# 🔐 Sistema de seguridad

## Autenticación

La autenticación utiliza:

* JWT Access Token,
* Refresh Token,
* Cookies HTTPOnly.

## Ventajas

* protección frente a XSS,
* integración sencilla SSR,
* separación frontend/backend.

---

## RBAC contextual

La autorización combina:

* roles globales,
* roles contextuales,
* permisos granulares.

```text
Usuario
   │
   ▼
Rol Global
   │
   ▼
Proyecto
   │
   ▼
Rol Contextual
   │
   ▼
Permisos efectivos
```

---

## Auditoría

Todas las acciones relevantes quedan registradas:

* usuario,
* acción,
* recurso,
* IP,
* timestamp,
* user-agent.

---

# ⚡ Realtime y WebSockets

La plataforma incorpora comunicación realtime para:

* Kanban,
* notificaciones,
* sincronización de actividad.

## Características

* salas por proyecto,
* broadcast selectivo,
* sincronización automática,
* arquitectura desacoplada.

---

# 🧪 Calidad software

El proyecto incorpora una estrategia real de calidad software.

## Herramientas

| Herramienta     | Uso              |
| --------------- | ---------------- |
| Ruff            | Linting          |
| Pytest          | Testing          |
| Coverage        | Cobertura        |
| SonarQube Cloud | Calidad estática |
| GitHub Actions  | CI/CD            |

---

# 🧪 Testing y cobertura

Actualmente el proyecto dispone de:

* más de 240 tests automatizados,
* cobertura superior al 75%,
* testing de servicios críticos,
* integración automática CI/CD.

## Tests cubiertos

* services,
* autenticación,
* permisos,
* dashboard,
* proyectos,
* tareas,
* notificaciones,
* activity feed.

## Ejecutar tests

```bash
uv run pytest
```

## Coverage

```bash
uv run pytest --cov=app --cov-report=html
```

---

# 📁 Estructura del proyecto

```text
app/
├── core/
│   ├── security/
│   ├── middleware/
│   ├── permissions/
│   └── utils/
│
├── db/
│   └── session/
│
├── modules/
│   ├── auth/
│   ├── users/
│   ├── roles/
│   ├── identities/
│   ├── projects/
│   ├── tasks/
│   ├── notifications/
│   ├── dashboard/
│   ├── websocket/
│   └── audit/
│
├── static/
├── templates/
└── main.py
```

---

# 🧩 Modelo de datos

## Entidades principales

* Users
* Identities
* Roles
* Permissions
* Projects
* Tasks
* Activities
* Notifications
* AuditLogs

## Relaciones principales

```text
User 1 ─── N Identities
User N ─── N Roles
Project 1 ─── N Tasks
Project N ─── N Members
User 1 ─── N AuditLogs
```

---

# 🚀 Instalación y ejecución

## Clonar repositorio

```bash
git clone https://github.com/fran-eliot/aula-robotica-platform
cd aula-robotica-platform
```

## Instalar dependencias

```bash
uv sync
```

## Configurar variables de entorno

Crear:

```text
.env
```

## Ejecutar aplicación

```bash
uv run uvicorn app.main:app --reload
```

Aplicación disponible en:

```text
http://127.0.0.1:8000
```

---

# 🐳 Docker y despliegue

El proyecto está preparado para despliegue mediante Docker.

## Objetivos del despliegue

* portabilidad,
* reproducibilidad,
* aislamiento,
* facilidad de instalación.

---

# 📘 API y documentación

## Swagger UI

```text
/api/docs
```

## ReDoc

```text
/api/redoc
```

La documentación OpenAPI incluye:

* endpoints,
* modelos,
* autenticación,
* respuestas,
* validaciones.

---

# 🛣️ Roadmap futuro

## Integraciones

* SAML/SSO UAH
* OAuth2
* proveedores externos

## Plataforma

* SPA complementaria
* métricas avanzadas
* analytics
* mobile support
* realtime avanzado

## Infraestructura

* despliegue cloud,
* Docker Compose,
* Kubernetes,
* escalado horizontal.

---

# 📚 Documentación adicional

El proyecto incluye documentación técnica extensa en:

```text
docs/
```

Incluyendo:

* arquitectura,
* seguridad,
* módulos,
* decisiones arquitectónicas,
* despliegue,
* testing,
* evolución del proyecto,
* integración SAML.

---

# 👨‍💻 Autor

## Francisco “Fran” Ramírez Martín

Backend Developer · Full Stack · Data & AI Enthusiast

### Formación

* CFGS DAM
* Ingeniería Informática (UNED)
* Bootcamp Full Stack
* Bootcamp Data Analytics

### Tecnologías principales

* Python
* FastAPI
* Java
* Spring Boot
* SQL
* Angular
* Docker
* AWS

### Contacto

🔗 LinkedIn

[https://linkedin.com/in/franeliot](https://linkedin.com/in/franeliot)

💻 GitHub

[https://github.com/fran-eliot](https://github.com/fran-eliot)
