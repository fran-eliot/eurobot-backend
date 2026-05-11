# Arquitectura del Sistema

## Visión General

Aula Robótica Platform sigue una arquitectura modular multicapa orientada a:

- mantenibilidad
- separación de responsabilidades
- seguridad por diseño
- reutilización
- escalabilidad progresiva

La aplicación adopta una estrategia híbrida basada en:

- renderizado server-side
- lógica modular desacoplada
- autorización centralizada
- sincronización realtime mediante WebSockets

---

# Arquitectura General

```text
Cliente Web
   │
   ▼
Presentation Layer
(Jinja2 + AdminLTE + JS)

   │
   ▼
Application Layer
(FastAPI Routers)

   │
   ▼
Domain / Service Layer
(Business Logic)

   │
   ▼
Persistence Layer
(SQLAlchemy ORM)

   │
   ▼
MariaDB
```

---

# Capas del Sistema

---

# 1. Presentation Layer (Capa de Presentación)

Responsable de la interfaz administrativa renderizada en servidor.

## Tecnologías

- Jinja2
- AdminLTE
- Bootstrap
- JavaScript modular ligero

## Responsabilidades

- Renderizado HTML
- Componentes reutilizables
- Formularios
- Tablas
- Dashboards
- Navegación contextual
- Menús dinámicos
- Feedback visual
- Timeline realtime
- Kanban interactivo

---

# Arquitectura Frontend

El frontend sigue una estrategia híbrida SSR (Server-Side Rendering).

## Organización CSS

La arquitectura CSS está dividida por capas funcionales.

### Foundation

Infraestructura visual global:

- `base.css`
- `layout.css`
- `utilities.css`

### Design System

Componentes reutilizables:

- `components.css`
- `forms.css`
- `tables.css`
- `permissions.css`

### Feature-oriented CSS

Estilos específicos de dominio:

- `projects.css`
- `tasks.css`
- `kanban.css`
- `dashboard.css`
- `users.css`
- `activities.css`

---

## Arquitectura JavaScript

JavaScript ligero organizado por módulos funcionales.

### Funcionalidades actuales

- Drag & Drop Kanban
- WebSockets realtime
- Timeline dinámico
- Presencia de usuarios
- Feedback visual
- Formularios interactivos

### Organización

```text
static/js/
├── projects/
│   └── project_detail.js
│
├── realtime/
│
└── shared/
```

---

# 2. Application Layer (Capa de Aplicación)

Responsable de exponer funcionalidades mediante FastAPI.

## Incluye

- Routers web
- Endpoints REST
- WebSockets
- Dependencias
- Validaciones
- Redirecciones
- Flash messages
- Policies de acceso

---

# Módulos actuales

## Core

Infraestructura compartida:

- auth
- audit
- permissions
- websocket realtime
- authorization
- middleware

---

## Gestión de usuarios

- users
- roles
- identities

---

## Gestión académica

- students
- activities

---

## Gestión de proyectos

- projects
- project_members
- tasks

---

## Integraciones

- auth_saml

---

# 3. Domain / Service Layer (Capa de Dominio / Servicios)

Contiene lógica de negocio desacoplada del transporte HTTP.

Los services encapsulan:

- validaciones funcionales
- reglas de negocio
- auditoría
- permisos contextuales
- operaciones complejas

---

## Ejemplos

- Creación de usuarios
- Asignación de roles
- Gestión de miembros de proyecto
- Cambio de estado Kanban
- Emisión de eventos realtime
- Auditoría centralizada
- Resolución de permisos efectivos

---

# Arquitectura de Servicios

La lógica de negocio sigue una separación clara:

```text
Router
  ↓
Service
  ↓
ORM / DB
```

Los routers:

- no contienen lógica compleja
- delegan reglas al service layer
- aplican dependencias y autorización

---

# 4. Persistence Layer (Capa de Persistencia)

Responsable del acceso a datos.

## Tecnologías

- SQLAlchemy ORM
- MariaDB

## Componentes

- Models
- Relaciones ORM
- Queries
- Session management
- Transactions

---

# Organización ORM

## Relaciones principales

- usuarios ↔ roles
- proyectos ↔ miembros
- proyectos ↔ tareas
- tareas ↔ usuarios
- auditoría ↔ recursos

---

# 5. Security Layer (Capa de Seguridad)

La seguridad es transversal a todas las capas.

## Componentes

- JWT
- HTTPOnly Cookies
- RBAC
- Policies
- Permission guards
- Middleware auth
- Ownership checks
- Roles contextuales

---

# Arquitectura de autorización

El sistema implementa una estrategia híbrida.

---

## RBAC Global

Permisos clásicos por recurso:

```text
users:create
tasks:update
projects:read
roles:delete
```

---

## RBAC Contextual por Proyecto

Cada proyecto puede contener roles internos:

- coordinator
- member

Esto permite:

- permisos dinámicos
- ownership contextual
- colaboración multiusuario
- autorización granular

---

# Helpers principales

## `can_user_action()`

Motor centralizado de autorización.

Compatible con:

- JWT payload
- ORM users
- roles globales
- permisos efectivos
- permisos contextuales

---

# 6. Realtime Layer (WebSockets)

El sistema implementa sincronización realtime mediante WebSockets organizados por proyecto ("rooms").

---

# Casos de uso actuales

## Kanban

Sincronización de estados:

- todo
- doing
- done

---

## Timeline de auditoría

Inserción dinámica de eventos:

- create
- update
- delete
- status change

---

## Presencia de usuarios

Visualización de usuarios conectados.

---

# Estrategia técnica

## Características

- FastAPI WebSockets
- Eventos JSON tipados
- Rooms por proyecto
- Broadcast controlado
- Reconexion automática frontend

---

## Emisión de eventos

Los eventos realtime se desacoplan mediante:

```python
emit_project_event()
```

Internamente utiliza:

```python
asyncio.create_task()
```

para evitar bloqueo de requests HTTP.

---

# Seguridad Realtime

## Validaciones

- JWT válido
- Usuario activo
- Pertenencia al proyecto
- Aislamiento por room

---

# Eventos actuales

## task_updated

Sincroniza cambios Kanban.

---

## audit

Actualiza timeline realtime.

---

## users_online

Actualiza presencia de usuarios.

---

# Flujo típico de petición

```text
Usuario
   ↓
Router
   ↓
Dependency Auth
   ↓
Permission Guard
   ↓
Service Layer
   ↓
ORM
   ↓
MariaDB
```

Resultado:

```text
Template Render
o
Evento Realtime
```

---

# Estructura Modular

```text
app/
├── core/
│   ├── authorization/
│   ├── constants/
│   ├── middleware/
│   ├── security/
│   ├── websockets/
│   └── utils/
│
├── modules/
│   ├── auth/
│   ├── audit/
│   ├── dashboard/
│   ├── users/
│   ├── roles/
│   ├── identities/
│   ├── projects/
│   ├── tasks/
│   ├── activities/
│   ├── students/
│   └── auth_saml/
│
├── db/
│   ├── base.py
│   └── session.py
│
├── templates/
├── static/
└── main.py
```

---

# Principios Arquitectónicos

## Separación de responsabilidades

Cada capa tiene responsabilidades claramente definidas.

---

## Seguridad por diseño

Toda acción sensible pasa por validación backend.

---

## Reutilización

Uso extensivo de:

- helpers
- macros
- services
- componentes UI

---

## Escalabilidad

Preparado para:

- nuevos módulos
- SSO
- API pública
- frontend desacoplado

---

## Mantenibilidad

- estructura modular
- frontend desacoplado
- CSS organizado por capas
- JS modular ligero

---

# Evolución futura prevista

## Backend

- API versionada
- Alembic migrations
- tests automatizados
- CI/CD
- Dockerización

---

## Frontend

- componentes JS reutilizables
- dashboards avanzados
- gráficos realtime

---

## Seguridad

- OAuth2
- SAML SSO
- 2FA
- revocación de sesiones

---

## Escalabilidad

- caché
- colas de eventos
- microservicios futuros (si escala)