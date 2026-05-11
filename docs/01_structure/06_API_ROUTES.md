# 06_API_ROUTES.md

## 🧠 Propósito

Este documento describe las rutas HTTP expuestas por la aplicación:

* API REST
* Rutas web (render Jinja2)
* Endpoints de autenticación
* Integraciones (SAML)

Sirve como referencia para:

* Desarrollo backend
* Integración frontend
* Auditoría de permisos
* Evolución del sistema

---

## 🔐 AUTENTICACIÓN (API)

### Login API

* `POST /api/auth/login`
* Autenticación mediante email + password
* Genera:

  * Access Token
  * Refresh Token (cookies HTTPOnly)

---

## 👤 USERS (API)

* `GET /api/users`
* `POST /api/users`
* `GET /api/users/{user_id}`
* `DELETE /api/users/{user_id}`

---

# 🌐 AUTENTICACIÓN WEB

* `GET /login` → formulario login
* `POST /login` → autenticación
* `GET /refresh` → renovar sesión
* `POST /logout` → cerrar sesión

---

# 🧾 SAML AUTHENTICATION

## Web

* `GET /auth/saml/login`
* `GET /auth/saml/acs`
* `GET /auth/saml/metadata`
* `POST /auth/saml/acs`

## API/Interno

* `GET /auth/saml/login`
* `GET /auth/saml/acs`
* `GET /auth/saml/metadata`
* `POST /auth/saml/acs`

---

# 📊 DASHBOARD

* `GET /dashboard`

---

# 👥 USERS WEB

* `GET /users`
* `GET /users/form`
* `POST /users/form`
* `GET /users/{user_id}/edit`
* `POST /users/{user_id}/edit`
* `GET /users/{user_id}`
* `POST /users/{user_id}/roles`
* `POST /users/{user_id}/delete`
* `POST /users/{user_id}/deactivate`
* `POST /users/{user_id}/activate`

---

# 🔑 IDENTITIES WEB

* `GET /identities`
* `GET /identities/{identity_id}`
* `POST /identities/{identity_id}`
* `GET /identities/form`
* `POST /identities/form`
* `GET /identities/{identity_id}/edit`
* `POST /identities/{identity_id}/edit`
* `POST /identities/{identity_id}/delete`

---

# 🛡️ ROLES WEB

* `GET /roles`
* `GET /roles/{role_id}`
* `GET /roles/{role_id}/edit`
* `POST /roles/{role_id}/edit`
* `GET /roles/form`
* `POST /roles/form`
* `POST /roles/{role_id}/delete`

---

# 📦 PROJECTS WEB

* `GET /projects`
* `GET /projects/form`
* `POST /projects/form`
* `GET /projects/{project_id}`
* `GET /projects/{project_id}/edit`
* `POST /projects/{project_id}/edit`
* `POST /projects/{project_id}/delete`

---

# 🧩 TASKS WEB

* `GET /tasks`
* `GET /tasks/form`
* `POST /tasks/form`
* `GET /tasks/{task_id}`
* `GET /tasks/{task_id}/edit`
* `POST /tasks/{task_id}/edit`
* `POST /tasks/{task_id}/delete`

---

# 🧪 ACTIVITIES WEB

* `GET /activities`
* `GET /activities/form`
* `POST /activities/form`
* `GET /activities/{activity_id}`
* `GET /activities/{activity_id}/edit`
* `POST /activities/{activity_id}/edit`
* `POST /activities/{activity_id}/delete`

---

# 🧠 ESTRUCTURA DE RUTAS

## Convención Web

```text
GET    /resource            → listado
GET    /resource/form       → crear
POST   /resource/form       → guardar nuevo
GET    /resource/{id}       → detalle
GET    /resource/{id}/edit  → editar
POST   /resource/{id}/edit  → guardar edición
POST   /resource/{id}/delete → eliminar
```

---

## Convención API

```text
GET    /api/resource
POST   /api/resource
GET    /api/resource/{id}
PUT    /api/resource/{id}
DELETE /api/resource/{id}
```

---

# 🔐 SEGURIDAD

Todas las rutas protegidas requieren:

* JWT válido en cookies
* Middleware de autenticación
* Validación RBAC

---

# ⚠️ OBSERVACIONES IMPORTANTES

* Existen rutas duplicadas entre API y Web → comportamiento esperado
* SAML está implementado parcialmente
* No hay aún rutas para:

  * project_members
  * project_teams
* No hay endpoints Kanban

---

# 🚧 GAP ACTUAL

Faltan endpoints para:

## Proyecto

* `/projects/{id}/members`
* `/projects/{id}/teams`

## Tasks (mejoras)

* cambio de estado
* asignación dinámica

## Kanban

* `/projects/{id}/kanban`

---

# 🔮 EVOLUCIÓN PREVISTA

* API completa REST paralela a Web
* Versionado (`/api/v1`)
* Endpoints para roles contextuales
* Integración frontend SPA futura

---

# 📌 RESUMEN

El sistema actualmente expone:

* API básica de autenticación y usuarios
* Sistema completo de rutas web administrativas
* Base funcional para proyectos, tareas y actividades

Pendiente:

* formalización completa de API REST
* endpoints de roles contextuales
* endpoints de Kanban

---
