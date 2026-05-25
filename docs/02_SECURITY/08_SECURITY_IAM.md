## 08_SECURITY_IAM.md

# 🔐 Seguridad e IAM

# Visión General

La seguridad constituye uno de los pilares arquitectónicos principales de Aula Robótica Platform.

La plataforma implementa una arquitectura híbrida basada en:

- JWT
- RBAC
- autorización contextual
- SSR seguro
- cookies HTTPOnly
- auditoría centralizada
- aislamiento realtime
- validación multicapa

El objetivo es construir una plataforma:

- segura por diseño
- escalable
- observable
- reutilizable
- preparada para entornos enterprise

---

# 🧱 Arquitectura General de Seguridad

```text 
Usuario
   ↓
JWT Validation
   ↓
Auth Middleware
   ↓
Permission Dependencies
   ↓
Policies Contextuales
   ↓
Service Layer Validation
   ↓
Persistence Layer
```
---

# 🔑 Autenticación
La autenticación actual utiliza:

* email/password
* JWT
* cookies HTTPOnly
* SSR integration

## Flujo de Login

```text
Usuario
    ↓
POST /login
    ↓
Validación Identity
    ↓
Generación JWT
    ↓
Set-Cookie HTTPOnly
    ↓
Redirect SSR
```
---

# Validaciones realizadas
### Usuario activo
Verificación de estado habilitado.

### Identity válida
Comprobación de identidad asociada.

### Password hash
Validación mediante:
* bcrypt

### Roles y permisos
Carga automática de permisos efectivos.

# 🎫 JWT Architecture
La plataforma utiliza JWT stateless.

### Access Token
Contiene:
```json
{
  "sub": "user_id",
  "username": "usuario",
  "roles": [],
  "permissions": [],
  "type": "access",
  "iat": 123456789,
  "exp": 123456789
}
```
### Refresh Token
Preparado para:
* persistencia segura
* renovación futura
* refresh rotation
* revocación avanzada

# 🍪 Integración SSR + JWT Cookies
La plataforma **NO** utiliza localStorage.
Los tokens se almacenan mediante:
* HTTPOnly cookies

## Ventajas
### Mitigación XSS
El frontend no tiene acceso directo a tokens.

### SSR nativo
Integración limpia con:
* FastAPI
* Jinja2
* renderizado server-side

### Seguridad centralizada
La sesión se resuelve completamente en backend.

## SessionMiddleware
La plataforma incorpora:
* Starlette SessionMiddleware

**Usado para:**
* flash messages
* contexto SSR
* toasts persistentes
* UX server-side

# 🛡️ Arquitectura de Autorización

La autorización combina múltiples capas:

- RBAC global
- ownership
- permisos contextuales
- validaciones por proyecto
- helpers reutilizables
- autorización SSR
- aislamiento realtime

La arquitectura sigue un modelo híbrido enterprise-oriented preparado para crecimiento modular y entornos multiusuario complejos.

---

# 🔐 Modelo RBAC

La plataforma implementa un sistema RBAC (*Role-Based Access Control*) combinado con permisos granulares desacoplados.

## Estructura General

```text
Usuario
   ↓
Roles Globales
   ↓
Permisos Efectivos
   ↓
Policies Contextuales
   ↓
Autorización Final
```

## Ventajas del modelo

- Escalable
- Flexible
- Seguro
- Fácil de extender
- Bajo acoplamiento
- Preparado para organizaciones complejas
- Compatible con autorización contextual

---

# 🧩 Permisos Granulares

Los permisos son atómicos e independientes del rol.

## Ejemplos

### Users

- users:read
- users:create
- users:update
- users:delete

### Projects

- projects:read
- projects:create
- projects:update
- projects:delete

### Tasks

- tasks:read
- tasks:create
- tasks:update
- tasks:delete

### Activities

- activities:read
- activities:create
- activities:update
- activities:delete

---

# 👤 Roles Globales

## Roles actuales

- admin
- profesor
- estudiante

## Roles previstos

- coordinador
- gestor
- supervisor
- auditor
- operador técnico

---

# 📌 Roles Contextuales

Los roles contextuales están completamente desacoplados del RBAC global.

## Roles de proyecto

### coordinator

Puede:

- gestionar tareas
- coordinar miembros
- administrar flujo operativo
- supervisar actividad

### member

Puede:

- participar en proyectos
- ejecutar tareas
- registrar actividad
- subir adjuntos

---

# 🧠 Motor Centralizado de Autorización

Toda autorización contextual se centraliza mediante helpers reutilizables.

## Core Helpers

### can_user_action()

Resuelve:

- roles globales
- permisos efectivos
- ownership
- contexto proyecto
- permisos derivados

### require_permission_web()

Dependency reutilizable FastAPI.

---

# 🔍 Policies reutilizables

Ejemplos:

- is_project_coordinator()
- user_in_project()
- can_manage_tasks()
- can_edit_activity()
- can_upload_attachment()

---

# 🎨 Seguridad UI (Frontend Authorization)

El frontend SSR implementa autorización visual contextual.

## Funcionalidades

- ocultación contextual
- rendering condicional
- navegación protegida
- componentes dinámicos
- menús adaptativos
- acciones contextuales

## Helpers UI disponibles

- has_role()
- has_perm()
- can()
- is_owner()
- is_project_coordinator()

## Ejemplo SSR

```html
{% if has_perm("projects:update") %}
```

> **Importante**
>
> Toda seguridad REAL reside siempre en backend.
>
> El frontend únicamente mejora UX y reduce ruido visual.

---

# 🧩 Validación Contextual Avanzada
La plataforma aplica validaciones multicapa.

### Capa Middleware
* JWT
* cookies
* sesión

### Capa Dependency
* permisos
* roles
* acceso contextual

### Capa Service
* ownership
* negocio
* consistencia

### Capa Persistence
* integridad relacional
* constraints

# 📡 Seguridad Realtime
La plataforma reutiliza JWT también en WebSockets.

## Flujo WebSocket
```text
JWT Cookie
    ↓
WS Connection
    ↓
JWT Validation
    ↓
User Resolution
    ↓
Room Authorization
    ↓
Realtime Events
```

## Validaciones WebSocket
* **JWT válido**: Verificación completa del token.[cite: 1]
* **Usuario activo**: Validación de estado.[cite: 1]
* **Acceso contextual**: Verificación por proyecto/sala.[cite: 1]
* **Room isolation**: Aislamiento total entre canales.[cite: 1]

## Rooms Architecture
```text
Project A
  └── WS Room A
Project B  
  └── WS Room B
```

Los usuarios únicamente reciben:
* eventos autorizados
* datos permitidos
* feeds contextualizados

## Eventos protegidos
### Dashboard
* dashboard_updates
* metrics

### Feed
* activity_feed
* audit_feed

### Tasks
* task_updated
* task_status_changed

### Notifications
* new_notification
* unread_counter

# 🔔 Seguridad Notifications
Las notificaciones son:
* persistentes
* contextualizadas
* aisladas por usuario

## Validaciones
Cada notificación valida:
* ownership
* permisos
* acceso contextual

# 📜 Auditoría Centralizada
El módulo audit registra:
* acciones críticas
* cambios operativos
* accesos
* eventos sensibles

## Información registrada
### Usuario
* user_id
* username

### Técnico
* IP
* User-Agent
* timestamp

### Funcional
* entidad afectada
* acción
* descripción
* metadata contextual

---

## Eventos auditados
### Seguridad
* LOGIN
* LOGOUT

### Usuarios
* CREATE_USER
* UPDATE_USER
* DELETE_USER

### Proyectos
* CREATE_PROJECT
* UPDATE_PROJECT
* DELETE_PROJECT

### Tasks
* CREATE_TASK
* UPDATE_TASK
* TASK_STATUS_CHANGE

# 📈 Auditoría Realtime
La auditoría ya soporta:
* timelines realtime
* streaming visual
* dashboards live
* actualización incremental

# 🔒 Riesgos Mitigados
### XSS
Mitigado evitando localStorage.

### Acceso no autorizado
Mitigado mediante RBAC + policies.

### Escalada de privilegios
Mitigado con autorización centralizada.

### Cross-project leakage
Mitigado mediante room isolation.

### Manipulación frontend
Mitigado validando siempre backend.

# 🚀 Mejoras Futuras
### Seguridad avanzada
* CSRF protection
* refresh rotation
* session revocation
* rate limiting
* 2FA

### Enterprise IAM
* OAuth2
* OpenID Connect
* SAML SSO
* LDAP integration

### Observabilidad
* SIEM integration
* external logs
* security metrics
* alerting

# 🧠 Principios Arquitectónicos
### Seguridad por diseño
La seguridad se integra desde la base.

### Defensa en profundidad
Múltiples capas independientes.

### Autorización centralizada
Toda validación pasa por helpers reutilizables.

### SSR First Security
El backend controla completamente sesión y permisos.

### Escalabilidad Enterprise
Preparado para:
* organizaciones académicas
* multiusuario
* crecimiento modular
* realtime enterprise