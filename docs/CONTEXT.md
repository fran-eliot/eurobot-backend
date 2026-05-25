# Aula Robótica Platform — Updated Context Documentation Bundle

---

# 00_MASTER_CONTEXT.md

## 🧠 Identidad del Proyecto

**Nombre:** Aula Robótica Platform
**Tipo:** Plataforma administrativa modular centrada en IAM, colaboración y gestión operativa
**Dominio:** Universidad / Aula de Robótica / Gestión Académica y Técnica
**Arquitectura:** SSR enterprise-style basada en FastAPI + Jinja2 + WebSockets

---

## 🎯 Objetivo Principal

Construir una plataforma moderna, segura y escalable para:

* gestión de usuarios e identidades
* control de acceso avanzado (RBAC + permisos contextuales)
* gestión de proyectos colaborativos
* gestión de tareas y actividades
* auditoría y trazabilidad
* sincronización realtime
* base futura para ecosistema académico y técnico completo

---

## 🧩 Estado Actual

El proyecto ha evolucionado desde un núcleo IAM hacia una plataforma operativa híbrida.

Actualmente incluye:

### IAM y Seguridad

* JWT + Refresh Tokens
* Cookies HTTPOnly
* RBAC granular
* autorización contextual
* middleware de autenticación
* auditoría centralizada

### Gestión Operativa

* proyectos
* tareas
* actividades
* adjuntos
* timeline de auditoría
* dashboard administrativo

### Frontend SSR Avanzado

* arquitectura reusable de macros Jinja2
* layouts desacoplados
* sistema moderno de toasts
* confirm dialogs reutilizables
* componentes row-based
* timelines dinámicos
* detail layouts avanzados

### Realtime

* WebSockets por proyecto
* timeline realtime
* sincronización Kanban-ready
* presencia de usuarios

---

## 🏗️ Arquitectura General

```text
Cliente Web
   ↓
Jinja2 + AdminLTE + JS modular
   ↓
FastAPI Routers
   ↓
Service Layer
   ↓
SQLAlchemy ORM
   ↓
MariaDB
```

---

## 🔐 Seguridad

El sistema aplica:

* seguridad por diseño
* validación backend obligatoria
* mínimo privilegio
* separación RBAC global / permisos contextuales
* aislamiento realtime
* auditoría completa

---

## ⚙️ Stack Principal

* Python
* FastAPI
* SQLAlchemy
* MariaDB
* Jinja2
* AdminLTE
* Bootstrap
* Chart.js
* WebSockets
* JWT
* bcrypt
* pytest
* GitHub Actions
* SonarCloud

---

## 📊 Estado del Proyecto

### Muy consolidado

* IAM
* seguridad
* SSR architecture
* reusable UI system
* auditoría
* testing backend

### En evolución

* permisos contextuales avanzados
* realtime testing
* Kanban completo
* teams
* CSRF
* API REST versionada

---

## 🚀 Visión

Convertirse en una plataforma universitaria completa para:

* gestión académica
* gestión técnica
* robótica
* investigación
* proyectos colaborativos
* reservas e inventario
* SSO corporativo

---

---

# 02_TECH_STACK.md

# Backend

## Python

Lenguaje principal.

## FastAPI

Uso:

* routers web
* API REST
* WebSockets
* middleware
* dependencias
* render SSR

## SQLAlchemy

ORM principal.

## MariaDB

Persistencia principal.

## Pydantic

Validación y schemas.

---

# Frontend

## Jinja2

Renderizado server-side.

## AdminLTE

Base visual administrativa.

## Bootstrap

Responsive UI.

## JavaScript modular

Organización:

```text
static/js/
├── dashboard/
├── projects/
├── realtime/
├── shared/
└── ui/
```

---

# UI y Visualización

## Chart.js

Dashboards y gráficas.

## Font Awesome

Sistema de iconos.

## Toastify / sistema toast custom

Feedback visual.

## Timeline UI

Auditoría visual dinámica.

---

# Seguridad

## JWT

Autenticación.

## HTTPOnly Cookies

Persistencia segura.

## RBAC

Roles y permisos.

## bcrypt

Hash seguro.

---

# Realtime

## FastAPI WebSockets

Uso:

* timeline realtime
* presencia usuarios
* sincronización de tareas
* auditoría dinámica

---

# Calidad

## pytest

Testing backend.

## pytest-cov

Coverage.

## Ruff

Linting.

## GitHub Actions

CI/CD.

## SonarCloud

Calidad continua.

---

# Gestión de dependencias

## uv

Instalación y locking.

---

---

# 04_DATABASE_SCHEMA.md

# Núcleo IAM

## users

* id_user
* username
* full_name
* active
* created_at

## identities

* id_identity
* email
* password_hash
* provider
* user_id

## roles

* id_role
* name

## permissions

* id_permission
* name

## user_roles

* user_id
* role_id

## role_permissions

* role_id
* permission_id

## audit_logs

* id_log
* user_id
* action
* resource_type
* resource_id
* description
* ip_address
* user_agent
* created_at

---

# Gestión de Proyectos

## projects

* id_project
* name
* description
* status
* start_date
* end_date
* created_by

## project_members

* id
* project_id
* user_id
* role

## tasks

* id_task
* project_id
* name
* description
* status
* priority
* assigned_to
* due_date
* created_by

## activities

* id_activity
* task_id
* user_id
* description
* time_spent
* created_at

## attachments

* id_attachment
* activity_id
* filename
* file_path
* mime_type
* uploaded_by
* uploaded_at

---

# Realtime / Auditoría

## notifications (previsto)

* id_notification
* user_id
* title
* message
* read
* created_at

---

# Relaciones principales

```text
Users
  ↓
ProjectMembers
  ↓
Projects
  ↓
Tasks
  ↓
Activities
  ↓
Attachments
```

---

# Decisiones importantes

* RBAC global separado de roles contextuales
* Tasks pertenecen a Projects
* Equipos son organizativos
* Auditoría desacoplada
* Adjuntos asociados a Activities

---

---

# 07_UI_TEMPLATES.md

# Filosofía Frontend

El frontend sigue una arquitectura SSR enterprise-style basada en:

* Jinja2
* AdminLTE
* macros reutilizables
* separación UI/componentes
* renderizado contextual por permisos

---

# Estructura General

```text
templates/
├── layouts/
├── components/
├── dashboard/
├── users/
├── projects/
├── tasks/
├── activities/
└── audit/
```

---

# Arquitectura de Componentes

## Macros reutilizables

### Buttons

* primary_button
* secondary_button
* delete_button
* icon_button

### Actions

* edit/delete/view actions
* confirm integration

### Layouts

* detail_layout
* form_layout
* section_card
* page_header

### Feedback

* toast system
* validation summary
* alerts desacopladas

---

# Sistema de Confirm Dialogs

El proyecto utiliza:

```html
class="js-confirm-form"
```

con JavaScript centralizado.

Objetivos:

* evitar confirm() nativo
* consistencia UX
* diseño moderno
* integración AdminLTE

---

# Sistema de Toasts

Arquitectura desacoplada:

```text
Backend Flash
   ↓
Session
   ↓
Template Injection
   ↓
Toast Renderer
```

Características:

* success
* error
* warning
* info
* autoclose
* deduplicación

---

# Timeline Realtime

Implementado principalmente en:

* tasks_detail
* audit timeline

Características:

* actualización dinámica
* agrupación por fecha
* iconos por acción
* colores contextuales
* prevención de duplicados

---

# Microcomponentes Row-Based

Patrón:

```text
*_row.html
```

Ejemplos:

* user_row
* project_row
* task_row
* activity_row

Beneficios:

* mantenibilidad
* separación visual
* reutilización extrema

---

# Reglas Clave

## Reutilización obligatoria

👉 Si se repite HTML → crear macro.

## Seguridad

La UI solo oculta acciones.

Toda validación real ocurre en backend.

## Lógica

❌ No lógica compleja en templates.

---

# Arquitectura JavaScript

## shared/

Código transversal.

## realtime/

Sockets y sincronización.

## ui/

Toasts, dialogs y feedback.

## dashboard/

Charts y widgets.

---

# Evolución futura

* partial SPA
* componentes interactivos avanzados
* dashboards realtime
* drag & drop Kanban completo
* notificaciones en vivo

---

---

# 08_CURRENT_TASKS.md

# Estado Actual

El proyecto ya posee una base arquitectónica muy sólida.

Las prioridades han cambiado desde la consolidación inicial.

---

# PRIORIDAD ALTA

## 1. Permisos contextuales avanzados

Pendiente:

* consolidar helpers
* ownership avanzado
* policies reutilizables

---

## 2. CSRF Protection

Implementar:

* tokens CSRF
* integración formularios
* validación middleware

---

## 3. Realtime Hardening

Pendiente:

* reconnect handling
* race condition testing
* websocket resilience

---

## 4. Testing Realtime

Añadir:

* pytest-asyncio
* websocket tests
* broadcast validation

---

# PRIORIDAD MEDIA

## 5. Kanban avanzado

* drag & drop completo
* persistencia optimista
* rollback visual

---

## 6. Teams

Pendiente:

* CRUD completo
* integración proyectos
* permisos contextuales

---

## 7. Notifications System

Pendiente:

* modelo DB
* realtime notifications
* badge unread

---

# PRIORIDAD BAJA

## 8. API REST Versionada

Objetivo:

```text
/api/v1/
```

---

## 9. Dockerización

* docker-compose
* nginx
* production containers

---

# Estado General

## Muy maduros

* IAM
* SSR architecture
* reusable templates
* dashboard
* auditing
* tasks/activities
* attachment system

## En consolidación

* realtime
* contextual permissions
* notifications
* teams

---

# Próximo gran objetivo

👉 Consolidar plataforma colaborativa realtime enterprise-style.

---

---

# 09_KNOWN_ISSUES.md

# Problemas Críticos

## 1. CSRF pendiente

Uso de cookies requiere:

* CSRF tokens
* protección formularios

Estado:
🔴 Alto

---

## 2. Realtime poco testeado

Faltan:

* websocket tests
* concurrencia
* reconexión

Estado:
🔴 Alto

---

# Problemas Importantes

## 3. Race conditions potenciales

Especialmente en:

* realtime timeline
* cambios concurrentes
* Kanban futuro

Estado:
🟠 Alto

---

## 4. Context invalidation

Posibles inconsistencias:

* sidebar dinámico
* permisos cacheados
* realtime updates

Estado:
🟠 Alto

---

## 5. JS modularization parcial

Todavía existe:

* JS inline
* lógica distribuida
* handlers repetidos

Estado:
🟠 Alto

---

## 6. API parcial

La API REST no refleja aún toda la funcionalidad SSR.

Estado:
🟡 Medio

---

## 7. Teams incompleto

Módulo aún parcial.

Estado:
🟡 Medio

---

# Riesgos Técnicos

## WebSockets

Posibles problemas:

* desconexiones
* pérdida de sincronización
* eventos duplicados

---

## Frontend SSR complejo

La arquitectura UI creció mucho.

Riesgo:

* exceso de acoplamiento visual
* deuda JS

---

# Estado Arquitectónico

## IAM

🟢 Muy sólido

## SSR UI

🟢 Muy sólido

## Testing backend

🟢 Muy sólido

## Realtime

🟠 Funcional pero aún inmaduro en testing

---

---

# 10_CHANGELOG.md

# [Unreleased]

## Added

### UI / UX

* sistema moderno de toasts
* confirm dialogs reutilizables
* formularios confirmables desacoplados
* timeline realtime avanzado
* layouts detail avanzados
* microcomponentes row-based

---

### Activities / Attachments

* soporte de adjuntos
* eliminación segura de attachments
* integración UI activities-detail

---

### Dashboard

* charts dinámicos
* integración Chart.js
* estadísticas avanzadas
* mejoras visuales

---

### Realtime

* timeline dinámico
* actualización instantánea auditoría
* prevención de duplicados
* rooms websocket por proyecto

---

## Refactored

### Frontend Architecture

* consolidación reusable macros
* desacoplamiento UI
* centralización feedback visual
* centralización dialogs JS

---

### Backend

* mejora service layer
* helpers reutilizables
* mejor separación router/service

---

## Fixed

* múltiples bugs de toast duplicado
* persistencia incorrecta de flash messages
* confirm dialogs inconsistentes
* macros sin contexto
* problemas de render SSR

---

## Security

* consolidación cookies HTTPOnly
* mejoras validación backend
* aislamiento realtime por proyecto

---

# Estado actual

El proyecto ha dejado de ser únicamente un sistema IAM.

Ahora es una plataforma SSR modular colaborativa con:

* realtime
* auditoría
* reusable UI architecture
* workflows operativos

---

---

# 17_CODING_RULES.md

# Reglas Generales

## Arquitectura

Router → Service → ORM → Template

Nunca romper separación de responsabilidades.

---

# Frontend SSR

## Templates

* reutilizar macros siempre
* evitar HTML duplicado
* usar row-components
* usar layouts reutilizables

---

## Toasts

❌ No usar alert() nativo.

✔ Usar sistema centralizado de toasts.

---

## Confirm dialogs

❌ No usar confirm() inline.

✔ Usar:

```html
class="js-confirm-form"
```

con JS centralizado.

---

## JavaScript

### Organización

```text
shared/
ui/
realtime/
feature-modules/
```

---

### Reglas

* evitar JS inline
* separar handlers reutilizables
* usar listeners centralizados
* evitar duplicación

---

# Seguridad

## Backend-first

Toda validación real ocurre en backend.

Frontend solo controla UX.

---

## Permisos

* usar helpers reutilizables
* no repetir lógica de autorización
* validar ownership

---

# Testing

## Cobertura

Mantener:

```text
>= 85%
```

Objetivo:

```text
90%+
```

---

# Regla de Oro

👉 Si algo se reutiliza:

* crear macro
* crear helper
* crear service
* crear componente

👉 Evitar duplicación siempre.


