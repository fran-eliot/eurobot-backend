# 12_API_ROUTES.md

# 🌐 API & Web Routes

# 🧠 Propósito

Este documento describe la arquitectura actual de rutas y endpoints expuestos por Aula Robótica Platform.

Incluye:

- API REST
- rutas SSR/Jinja2
- autenticación JWT
- integración SAML
- realtime endpoints
- attachments
- notifications
- endpoints contextuales

---

# 🏗️ Filosofía Arquitectónica

La plataforma implementa una arquitectura híbrida:

```text id="3u2b5k"
SSR (Jinja2)
+
REST API
+
Realtime WebSockets
```
---

# Objetivos
* SSR enterprise-first
* UX moderna
* backend desacoplado
* soporte realtime
* futura SPA compatibility

# 🔐 AUTHENTICATION API
## Login API
`POST /api/auth/login`  
Autenticación principal.

### Funcionalidades
* email/password
* generación JWT
* cookies HTTPOnly
* carga permisos
* RBAC

### Respuesta
**Tokens generados**
* access_token
* refresh_token

---

# 👤 USERS API
* **GET /api/users**: Listado usuarios.
* **POST /api/users**: Crear usuario.
* **GET /api/users/{user_id}**: Detalle usuario.
* **DELETE /api/users/{user_id}**: Eliminar usuario.

# 🌐 AUTHENTICATION WEB
## SSR Authentication
* **GET /login**: Formulario login SSR.
* **POST /login**: Autenticación SSR.
  * **Incluye**:
    * JWT cookies
    * sesión
    * flash messages
    * redirects
* **GET /refresh**: Renovación sesión.
* **POST /logout**: Cerrar sesión.

# 🏢 SAML AUTHENTICATION
## SAML Web
* **GET /auth/saml/login**: Inicio flujo SAML.
* **GET /auth/saml/acs**: Assertion Consumer Service.
* **GET /auth/saml/metadata**: Metadata XML.
* **POST /auth/saml/acs**: Procesamiento respuesta IdP.

### Estado actual
SAML parcialmente implementado.
**Preparado para**:
* Azure AD
* Keycloak
* Okta
* Identity Providers corporativos

# 📊 DASHBOARD
## Dashboard SSR
* **GET /dashboard**: Dashboard administrativo principal.
  * **Funcionalidades**:
    * métricas
    * charts
    * audit timeline
    * activity feed
    * notifications
    * realtime updates

## Realtime Dashboard
* **WS /ws/dashboard**: Canal realtime dashboard.
  * **Eventos soportados**:
    * dashboard_metrics
    * audit_feed
    * activity_feed

# 👥 USERS WEB
## Gestión Usuarios SSR
* **GET /users**: Listado usuarios.
* **GET /users/form**: Formulario creación.
* **POST /users/form**: Crear usuario.
* **GET /users/{user_id}**: Detalle usuario.
* **GET /users/{user_id}/edit**: Formulario edición.
* **POST /users/{user_id}/edit**: Guardar edición.
* **POST /users/{user_id}/roles**: Asignar roles.
* **POST /users/{user_id}/delete**: Eliminar usuario.
* **POST /users/{user_id}/deactivate**: Desactivar usuario.
* **POST /users/{user_id}/activate**: Activar usuario.

# 🔑 IDENTITIES WEB
## Gestión Identidades
* **GET /identities**: Listado identities.
* **GET /identities/form**: Crear identity.
* **POST /identities/form**: Guardar identity.
* **GET /identities/{identity_id}**: Detalle identity.
* **GET /identities/{identity_id}/edit**: Editar identity.
* **POST /identities/{identity_id}/edit**: Guardar edición.
* **POST /identities/{identity_id}/delete**: Eliminar identity.

# 🛡️ ROLES WEB
## Gestión RBAC
* **GET /roles**: Listado roles.
* **GET /roles/form**: Crear rol.
* **POST /roles/form**: Guardar rol.
* **GET /roles/{role_id}**: Detalle rol.
* **GET /roles/{role_id}/edit**: Editar rol.
* **POST /roles/{role_id}/edit**: Guardar edición.
* **POST /roles/{role_id}/delete**: Eliminar rol.

# 📦 PROJECTS WEB
## Gestión Proyectos
* **GET /projects**: Listado proyectos.
* **GET /projects/form**: Crear proyecto.
* **POST /projects/form**: Guardar proyecto.
* **GET /projects/{project_id}**: Detalle proyecto.
* **GET /projects/{project_id}/edit**: Editar proyecto.
* **POST /projects/{project_id}/edit**: Guardar edición.
* **POST /projects/{project_id}/delete**: Eliminar proyecto.

## 👥 Project Membership
### Membership Management
* **POST /projects/{project_id}/members**: Agregar miembro.
* **POST /projects/{project_id}/members/remove**: Eliminar miembro.
* **POST /projects/{project_id}/coordinator**: Asignar coordinador.

**Funcionalidades:**
* autorización contextual
* project roles
* ownership
* coordinación proyectos

# 🧩 TASKS WEB
## Gestión Tareas
* **GET /tasks**: Listado tareas.
* **GET /tasks/form**: Crear tarea.
* **POST /tasks/form**: Guardar tarea.
* **GET /tasks/{task_id}**: Detalle tarea.
* **GET /tasks/{task_id}/edit**: Editar tarea.
* **POST /tasks/{task_id}/edit**: Guardar edición.
* **POST /tasks/{task_id}/delete**: Eliminar tarea.

### Task State Management
* **POST /tasks/{task_id}/status**: Cambio estado realtime.

**Estados soportados:**
* todo
* doing
* done

# 🧪 ACTIVITIES WEB
## Gestión Actividades
* **GET /activities**: Listado actividades.
* **GET /activities/form**: Crear actividad.
* **POST /activities/form**: Guardar actividad.
* **GET /activities/{activity_id}**: Detalle actividad.
* **GET /activities/{activity_id}/edit**: Editar actividad.
* **POST /activities/{activity_id}/edit**: Guardar edición.
* **POST /activities/{activity_id}/delete**: Eliminar actividad.

### Activity Status
* **POST /activities/{activity_id}/status**: Cambio estado actividad.

**Estados soportados:**
* Pendiente
* En progreso
* Completada

# 📎 ACTIVITY ATTACHMENTS
## Sistema Adjuntos
* **POST /activity-attachments/upload**: Subir adjunto.
* **GET /activity-attachments/{attachment_id}/download**: Descargar archivo.
* **POST /activity-attachments/{attachment_id}/delete**: Eliminar adjunto.

**Funcionalidades:**
* uploads seguros
* metadata persistente
* ownership
* validación MIME
* filesystem storage

# 🔔 NOTIFICATIONS
## Notifications API
* **GET /notifications**: Listado notificaciones.
* **POST /notifications/{notification_id}/read**: Marcar leída.
* **POST /notifications/read-all**: Marcar todas leídas.
* **GET /notifications/unread-count**: Contador unread.

## Notifications Realtime
* **WS /ws/notifications**: Canal realtime notificaciones.

**Eventos soportados:**
* new_notification
* notification_read
* unread_counter

# 📡 REALTIME WEBSOCKETS
## Arquitectura WebSocket
La plataforma utiliza WebSockets aislados por contexto.

### Endpoints actuales
* **WS /ws/dashboard**: Dashboard realtime.
* **WS /ws/notifications**: Notifications realtime.

### Arquitectura rooms
* Project Room
* User Room
* Dashboard Room

### Funcionalidades realtime
* dashboards live
* feeds dinámicos
* métricas
* notifications
* auditoría live

# 🧾 AUDIT & FEED
## Audit Timeline
Integrado directamente en dashboard y vistas SSR.

### Eventos auditados
* LOGIN
* CREATE_PROJECT
* UPDATE_TASK
* DELETE_ACTIVITY
* UPLOAD_ATTACHMENT

# 🧠 Convenciones Arquitectónicas
## Convención SSR
* **GET /resource**
* **GET /resource/form**
* **POST /resource/form**
* **GET /resource/{id}**
* **GET /resource/{id}/edit**
* **POST /resource/{id}/edit**
* **POST /resource/{id}/delete**

## Convención REST
* GET
* POST
* PUT/PATCH
* DELETE

# 🔐 Seguridad
Todas las rutas protegidas requieren:
* JWT válido
* cookies HTTPOnly
* middleware auth
* RBAC
* autorización contextual

## Seguridad WebSocket
Todos los sockets validan:
* JWT
* usuario activo
* acceso contextual
* aislamiento rooms

# 🚀 Estado Actual Arquitectónico
## Actualmente implementado
### Backend
* SSR enterprise
* JWT cookies
* RBAC
* attachments
* notifications
* realtime
* dashboards live

### Frontend
* AdminLTE
* reusable UI
* dialogs modernos
* toast system
* contextual rendering

### Realtime
* websocket isolation
* notifications
* dashboard streaming

# 🔮 Evolución Prevista
### API
* `/api/v1`
* OpenAPI formalizado
* versionado

### Seguridad
* CSRF
* refresh rotation
* rate limiting
* 2FA

### Realtime
* project collaboration
* presence
* collaborative editing

### Frontend
* posible SPA híbrida
* HTMX/Turbo exploration
* realtime UI expansion

# 📌 Resumen
La plataforma ya dispone de una arquitectura moderna basada en:  
**SSR + JWT + Realtime + RBAC + Contextual Authorization**

Con capacidades reales de:
* administración enterprise
* trazabilidad
* realtime collaboration
* seguridad multicapa
* escalabilidad modular

