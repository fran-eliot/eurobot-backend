# 03_ARCHITECTURE.md

# Arquitectura General del Sistema

# 📌 Visión General

Aula Robótica Platform sigue una arquitectura modular multicapa orientada a:

- mantenibilidad
- seguridad por diseño
- SSR enterprise architecture
- reutilización
- realtime collaboration
- escalabilidad progresiva

La plataforma combina:

- renderizado server-side
- backend modular
- autorización contextual
- realtime synchronization
- reusable UI systems

---

# 🏗️ Arquitectura General

```text
Cliente Web
    │
    ▼
SSR Presentation Layer
(Jinja2 + Bootstrap + AdminLTE + JS)

    │
    ▼
Application Layer
(FastAPI Routers + Dependencies)

    │
    ▼
Domain / Service Layer
(Business Logic + Authorization)

    │
    ▼
Persistence Layer
(SQLAlchemy ORM)

    │
    ▼
MariaDB
''' 

---

# 🧩 Capas Principales

### 1. Presentation Layer
Responsable de:
- renderizado SSR
- layouts
- reusable UI
- dashboards
- feedback visual
- realtime UI updates

Tecnologías:
- Jinja2
- Bootstrap
- AdminLTE
- JavaScript modular

### 2. Application Layer
Implementada mediante FastAPI.
Responsabilidades:
- routers
- endpoints
- dependencies
- middleware
- flash messages
- websocket endpoints
- request orchestration

### 3. Domain / Service Layer
Contiene la lógica de negocio desacoplada.
Incluye:
- validaciones
- reglas funcionales
- autorización contextual
- auditoría
- emisión de eventos realtime

### 4. Persistence Layer
Responsable del acceso a datos.
Implementado mediante:
- SQLAlchemy ORM
- relaciones ORM
- session management
- eager loading
- transactional workflows

### 5. Realtime Layer
Implementa sincronización realtime mediante WebSockets.
Casos actuales:
- dashboard sync
- notifications
- timelines
- kanban updates
- user presence

# 🔐 Arquitectura de Seguridad
La seguridad es transversal a toda la plataforma.
El sistema utiliza:
- JWT
- HTTPOnly cookies
- SessionMiddleware
- RBAC
- contextual authorization
- ownership validation

# 🧠 Arquitectura Modular
La plataforma está organizada por dominios funcionales.

```text
modules/
├── auth/
├── users/
├── roles/
├── identities/
├── projects/
├── tasks/
├── activities/
├── notifications/
├── audit/
├── dashboard/
└── auth_saml/
```
## 🎨 Arquitectura UI
La UI sigue principios de:
- reusable components
- reusable rows
- contextual rendering
- centralized dialogs
- centralized toast notifications

## ⚡ Arquitectura Realtime
El sistema realtime utiliza:
- websocket rooms
- event emitters
- async broadcasts
- reconnect workflows

## 📂 Gestión de Adjuntos
La plataforma incorpora attachment workflows integrados en actividades.
Incluye:
- upload seguro
- ownership
- metadata persistente
- filesystem storage
- SSR integration

## 🔔 Sistema de Notificaciones
El sistema de notifications soporta:
- persistencia
- realtime updates
- unread counters
- SSR rendering
- websocket synchronization

## 🏁 Principios Arquitectónicos

### Seguridad backend-first
Toda autorización se valida en backend.

### SSR-first
El sistema prioriza renderizado server-side.

### Reutilización
Uso intensivo de:
- macros
- helpers
- services
- reusable UI
- reusable dialogs

### Escalabilidad progresiva
Preparado para:
- SSO/SAML
- APIs públicas
- dashboards avanzados
- realtime collaboration

## 🚀 Estado Arquitectónico Actual
Actualmente la plataforma ya presenta características típicas de:
- enterprise admin platforms
- collaborative operational systems
- internal management platforms

con una arquitectura madura, modular y altamente extensible.