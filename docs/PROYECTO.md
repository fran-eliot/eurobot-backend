# Aula Robótica Platform — Context Update (May 2026)

## Estado General del Proyecto

La plataforma Aula Robótica ha evolucionado desde un sistema IAM/JWT básico hacia una aplicación web enterprise-style basada en FastAPI + SQLAlchemy + Jinja2 con una arquitectura modular, sistema de permisos avanzado y una UI moderna y reutilizable.

Actualmente el proyecto dispone de:

* Autenticación JWT mediante cookies
* Middleware de autenticación y autorización
* Sistema RBAC (roles + permisos)
* Layouts reutilizables con Jinja
* Menú dinámico según permisos
* Breadcrumbs inteligentes
* Dashboard con métricas y WebSockets
* Activity Feed
* Sistema de auditoría
* Sistema de notificaciones
* Sistema de flash messages + toasts modernos
* Confirm dialogs reutilizables
* Gestión de proyectos, tareas y actividades
* Sistema de adjuntos para actividades

---

# Arquitectura Principal

## Backend

### Stack

* FastAPI
* SQLAlchemy ORM
* MySQL
* Jinja2
* JWT Auth
* WebSockets
* SessionMiddleware (Starlette)

### Organización Modular

La aplicación sigue una estructura modular:

* core/
* modules/
* web/
* templates/
* static/
* utils/

Cada módulo contiene:

* model
* schemas
* service
* router
* repository (cuando aplica)
* templates
* JS/CSS específicos

---

# Sistema de UI Reutilizable

## Macros Jinja

El proyecto usa una arquitectura basada en componentes reutilizables.

### Componentes importantes

* buttons.html
* badges.html
* tabs.html
* detail_layout.html
* audit_table.html
* permission_matrix.html
* actions.html

## Layouts

Se ha consolidado un sistema de detail layouts reutilizables:

* panel izquierdo (perfil/resumen)
* panel derecho (tabs)
* cards modernas
* hero sections

---

# Sistema de Toasts y Flash Messages

## Implementación Final

Se implementó un sistema de flash messages persistente compatible con redirects.

### Backend

Archivo:

* app/utils/flash.py

Funciones:

* add_flash()
* get_flash()
* flash_success()
* flash_error()
* flash_warning()
* flash_info()

### Características

* Persistencia mediante sesión
* Compatible con RedirectResponse
* Consumo único de mensajes
* Cache por request mediante request.state
* Evita duplicados y reapariciones

### Solución importante

El contexto global se construye varias veces por request.

Por ello get_flash() ahora:

* consume mediante session.pop()
* cachea en request.state._cached_flash_messages

Esto resolvió:

* toasts duplicados
* acumulación de mensajes
* mensajes reapareciendo entre páginas

---

# Sistema de Confirm Dialogs

## Estado Actual

Se eliminaron los confirm() nativos del navegador.

Ahora el proyecto usa:

* dialogs.js
* modales modernos reutilizables
* formularios con clase js-confirm-form
* atributos data-confirm-*

## btn_delete()

El macro btn_delete fue modernizado.

Ahora acepta:

* confirm_title
* confirm_text
* confirm_button

Ejemplo:

```jinja
{{ btn_delete(
    "/projects/" ~ project.id_project ~ "/delete",
    confirm_title="¿Eliminar proyecto?",
    confirm_text="Se eliminarán también sus tareas y actividades."
) }}
```

---

# Sistema de Adjuntos para Actividades

## Modelo

ActivityAttachment

### Relaciones

En Activity:

```python
attachments = relationship(
    "ActivityAttachment",
    back_populates="activity",
    cascade="all, delete-orphan",
    passive_deletes=True,
)
```

En User:

```python
activity_attachments = relationship(
    "ActivityAttachment",
    back_populates="uploader",
)
```

## Campos principales

* activity_id
* uploaded_by
* original_filename
* stored_filename
* file_path
* mime_type
* size_bytes
* description
* created_at

## Funcionalidades implementadas

* subida de archivos
* borrado
* descarga
* descripción opcional
* almacenamiento físico
* toasts automáticos
* recarga correcta tras redirect

---

# Contexto Global de Templates

Archivo:

* app/web/context.py

## Funciones principales

### get_template_context()

Proporciona:

* usuario actual
* roles
* permisos
* helpers de autorización
* menú dinámico
* breadcrumbs
* flash messages
* notificaciones
* helpers visuales de auditoría
* helpers visuales de activity feed

### Helpers disponibles en templates

* has_role()
* has_perm()
* can()
* is_owner()
* is_project_coordinator()

---

# Sistema de Notificaciones

## Características

* notificaciones recientes globales
* contador de no leídas
* WebSocket notifications
* integración en navbar/layout

## Context helpers

* recent_notifications
* unread_notifications_count

---

# Dashboard

## Funcionalidades

* estadísticas globales
* métricas de usuarios
* métricas de proyectos
* métricas de tareas
* métricas de actividades
* feed reciente
* auditoría reciente
* gráficos Chart.js
* WebSocket dashboard updates

## Tecnologías UI

* Bootstrap
* FontAwesome
* Chart.js
* JS modular

---

# Seguridad y Permisos

## Sistema RBAC

Permisos estructurados como:

```text
module:action
```

Ejemplos:

* users:read
* users:create
* projects:update
* activities:delete

## Helper principal

```python
can(action, resource, target=None)
```

Usado extensivamente en templates.

---

# Estado de Madurez del Proyecto

Actualmente el proyecto ya presenta características de aplicación enterprise:

* arquitectura modular
* sistema RBAC avanzado
* UI reutilizable
* sistema de auditoría
* activity feed
* WebSockets
* notificaciones
* confirm dialogs modernos
* toasts centralizados
* layouts profesionales
* macros reutilizables
* breadcrumbs dinámicos
* contexto global consistente

El nivel actual supera ampliamente el típico CRUD FastAPI/Jinja.

---

# Próximas Líneas Posibles

## Backend

* permisos más granulares
* soft delete
* versionado
* API pública
* rate limiting
* tests automáticos
* repositorios desacoplados

## Frontend/UI

* drag & drop uploads
* previews de adjuntos
* dark mode
* live updates parciales
* tables avanzadas
* filtros persistentes
* componentes HTMX o Alpine.js

## Infraestructura

* Docker
* CI/CD
* despliegue cloud
* logging estructurado
* monitorización
* backups automáticos

---

# Estado Actual

El sistema de UI y UX ya tiene una base muy sólida y consistente.

Las mejoras recientes sobre:

* toasts
* confirm dialogs
* context caching
* sistema de adjuntos

han consolidado una arquitectura frontend/backend mucho más robusta y mantenible.
