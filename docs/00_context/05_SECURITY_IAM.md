# Seguridad e IAM

## Visión General

La seguridad constituye uno de los pilares principales de Aula Robótica Platform.

El sistema implementa una estrategia híbrida basada en:

- JWT
- RBAC
- permisos granulares
- roles contextuales
- auditoría
- aislamiento realtime

Todo ello bajo un enfoque de:

- seguridad por diseño
- mínimo privilegio
- autorización centralizada
- trazabilidad completa

---

# Arquitectura de Seguridad

```text
Usuario
   ↓
JWT Validation
   ↓
Middleware Auth
   ↓
Permission Guards
   ↓
Policies / Ownership
   ↓
Service Layer
```

---

# Autenticación

El sistema utiliza autenticación basada en:

- credenciales
- JWT
- cookies HTTPOnly

---

# Login actual

## Credenciales soportadas

- email
- password

---

# Verificaciones realizadas

## Usuario activo

Validación de estado del usuario.

---

## Password hash

Hash seguro mediante:

- bcrypt

---

## Identidad válida

Comprobación de identidad asociada.

---

# JWT (JSON Web Tokens)

El sistema utiliza JWT para autenticación stateless.

---

# Access Token

Contiene:

```json
{
  "sub": "user_id",
  "username": "usuario",
  "roles": [],
  "permissions": [],
  "exp": "timestamp"
}
```

---

# Refresh Token

Preparado para:

- renovación de sesión
- persistencia segura
- rotación futura

---

# Transporte de Tokens

Los tokens se almacenan mediante cookies seguras.

## Estrategia actual

- HTTPOnly
- SameSite
- Secure (entornos HTTPS)

---

# Ventajas

## Mitigación XSS

No se utiliza localStorage.

---

## Integración SSR

Compatibilidad natural con Jinja2 y renderizado server-side.

---

## Seguridad centralizada

Menor exposición frontend.

---

# Autorización

El sistema implementa una arquitectura híbrida de autorización.

---

# RBAC Global

Permisos clásicos asociados a recursos.

---

## Ejemplos

### Users

- users:read
- users:create
- users:update
- users:delete

---

### Roles

- roles:read
- roles:create
- roles:update
- roles:delete

---

### Projects

- projects:read
- projects:create
- projects:update
- projects:delete

---

### Tasks

- tasks:read
- tasks:create
- tasks:update
- tasks:delete

---

### Otros

- dashboard:read
- audit:read
- students:read

---

# Roles Globales

## Roles actuales

- admin
- profesor
- estudiante

---

# Roles Contextuales

Además del RBAC global, el sistema implementa roles internos por proyecto.

---

## Roles actuales

### coordinator

Gestión operativa del proyecto:

- tareas
- miembros
- seguimiento

---

### member

Participación colaborativa:

- visualización
- ejecución de tareas

---

# Arquitectura de autorización contextual

La autorización contextual permite permisos dinámicos según:

- proyecto
- ownership
- pertenencia
- rol interno

---

# Motor centralizado de autorización

## `can_user_action()`

Responsable de resolver:

- roles globales
- permisos efectivos
- ownership
- roles contextuales
- permisos por proyecto

---

# Dependencias de seguridad

## FastAPI Dependencies

Uso extensivo de:

```python
require_permission_web()
```

---

## Policies reutilizables

Ejemplos:

- `is_project_coordinator()`
- `can_manage_tasks()`
- `user_in_project()`

---

# Seguridad Backend

Toda seguridad real reside en backend.

---

# Capas de protección

## Middleware JWT

Validación automática de sesión.

---

## Permission Guards

Control de acceso por recurso.

---

## Ownership checks

Restricciones por propietario/contexto.

---

## Policies contextuales

Validación dinámica según proyecto.

---

## Validación Service Layer

Reglas críticas revalidadas en lógica de negocio.

---

# Seguridad Frontend

El frontend implementa únicamente restricciones visuales.

---

## Incluye

- ocultación de botones
- ocultación de menús
- navegación contextual
- acciones condicionadas

---

> El frontend nunca sustituye validaciones backend.

---

# Seguridad Realtime (WebSockets)

El sistema reutiliza la misma estrategia de autenticación JWT para WebSockets.

---

# Validaciones realizadas

## JWT válido

Validación de access token.

---

## Usuario activo

Comprobación de estado.

---

## Acceso al proyecto

Verificación contextual.

---

## Aislamiento por room

Cada proyecto mantiene su propio canal realtime.

---

# Eventos protegidos

- task_updated
- audit
- users_online

---

# Estrategia de rooms

```text
Proyecto A
 └── room websocket A

Proyecto B
 └── room websocket B
```

Los usuarios solo reciben eventos de proyectos autorizados.

---

# Auditoría

El sistema implementa auditoría centralizada mediante el módulo `audit`.

---

# Objetivos

- trazabilidad
- observabilidad
- seguimiento de acciones
- análisis de seguridad

---

# Eventos auditados

## Seguridad

- LOGIN
- LOGOUT

---

## Usuarios

- CREATE_USER
- UPDATE_USER
- DELETE_USER
- ACTIVATE_USER
- DEACTIVATE_USER

---

## Proyectos

- CREATE_PROJECT
- UPDATE_PROJECT
- DELETE_PROJECT

---

## Tasks

- CREATE_TASK
- UPDATE_TASK
- DELETE_TASK
- TASK_STATUS_CHANGE

---

# Información registrada

## Contexto usuario

- user_id
- username

---

## Contexto técnico

- IP
- User-Agent
- timestamp

---

## Contexto funcional

- recurso afectado
- descripción
- tipo de acción

---

# Timeline Realtime

La auditoría puede visualizarse mediante timeline dinámico:

- agrupación por fecha
- actualización realtime
- feedback visual
- integración AdminLTE

---

# Riesgos mitigados

## XSS

Mitigado evitando localStorage.

---

## Acceso no autorizado

Mitigado mediante RBAC y policies.

---

## Elevación de privilegios

Mitigado con autorización centralizada.

---

## Acceso cross-project

Mitigado mediante aislamiento realtime.

---

## Trazabilidad insuficiente

Mitigado mediante auditoría centralizada.

---

# Mejoras futuras previstas

## Seguridad avanzada

- CSRF tokens
- Rate limiting
- Session revocation
- Refresh rotation
- 2FA

---

## Integración corporativa

- OAuth2
- OpenID Connect
- SAML SSO

---

## Observabilidad

- SIEM
- logs externos
- alertas de seguridad
- métricas de acceso

---

# Principios aplicados

## Seguridad por diseño

La seguridad se integra desde la arquitectura base.

---

## Mínimo privilegio

Los usuarios solo reciben permisos necesarios.

---

## Defensa en profundidad

Múltiples capas de validación.

---

## Autorización centralizada

Toda validación pasa por helpers y policies reutilizables.

---

## Escalabilidad

Preparado para crecimiento organizacional y académico.