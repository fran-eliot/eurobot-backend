# 30_ACTIVITIES_MODULE.md

# Módulo de Actividades

## Objetivo

El módulo de actividades gestiona el registro del trabajo realizado sobre las tareas de Aula Robótica Platform.

Mientras el módulo de tareas representa el trabajo planificado, el módulo de actividades representa el trabajo ejecutado:

```text
Task = qué hay que hacer
Activity = qué se ha hecho
```

Actualmente el módulo permite:

- registrar actividades sobre tareas,
- asociar actividad a usuario,
- registrar horas invertidas,
- controlar estado de actividad,
- adjuntar evidencias,
- consultar actividades con filtros,
- mostrar detalle enriquecido,
- alimentar activity feed,
- emitir feedback visual mediante toasts.

---

# Estado Arquitectónico

Actualmente NO existe `activity_service.py`.

La lógica principal del módulo vive en:

```text
activities_web.py
```

Esto significa que el módulo funciona correctamente, pero todavía conserva parte de lógica de negocio dentro del router.

---

# Arquitectura Actual

```text
Activities Web Router
        ↓
Activity Model
        ↓
Task / Project Context
        ↓
Activity Feed
        ↓
Attachment System
        ↓
SSR UI
```

---

# Componentes Principales

## Backend

```text
app/modules/activities/
├── activity_model.py
└── activities_web.py
```

---

## Frontend SSR

```text
templates/activities/
├── activities_list.html
├── activities_detail.html
└── activities_form.html
```

---

## Componentes UI

```text
templates/components/activity_row.html
templates/components/data_table.html
templates/components/section_card.html
templates/components/filters_bar.html
```

---

## Módulos Integrados

```text
tasks
projects
users
activity_feed
activity_attachments
flash/toasts
authorization
```

---

# Modelo de Actividad

La entidad `Activity` representa una acción, avance o evidencia de trabajo asociada a una tarea.

## Campos principales

```text
id_activity
name
description
status
task_id
user_id
time_spent
created_at
```

---

# Estados de Actividad

Actualmente los estados se almacenan como string.

## Valores usados en UI

```text
Pendiente
En progreso
Completada
```

Estos valores se utilizan en filtros, badges y contadores del listado. 

---

# Relaciones

## Activity → Task

Cada actividad pertenece a una tarea.

```text
Activity N ─── 1 Task
```

---

## Activity → User

Cada actividad pertenece a un usuario responsable o ejecutor.

```text
Activity N ─── 1 User
```

---

## Activity → Attachments

Una actividad puede tener múltiples adjuntos.

```text
Activity 1 ─── N ActivityAttachment
```

La vista detalle integra directamente la subida, listado, descarga y borrado de adjuntos. :contentReference[oaicite:1]{index=1}

---

# Router Web

Archivo:

```text
activities_web.py
```

Gestiona el flujo SSR completo del módulo. :contentReference[oaicite:2]{index=2}

---

# Rutas Principales

## Listado

```text
GET /activities/
```

Permite:

- búsqueda por nombre,
- filtrado por estado,
- filtrado por tarea,
- paginación,
- contadores por estado,
- filtrado contextual por rol/proyecto.

---

## Formulario de creación

```text
GET /activities/form
```

Admite precarga por tarea:

```text
/activities/form?task_id=...
```

---

## Crear actividad

```text
POST /activities/form
```

---

## Detalle

```text
GET /activities/{activity_id}
```

---

## Formulario de edición

```text
GET /activities/{activity_id}/edit
```

---

## Actualizar actividad

```text
POST /activities/{activity_id}/edit
```

---

## Eliminar actividad

```text
POST /activities/{activity_id}/delete
```

---

# Seguridad del módulo

El módulo usa seguridad backend-first mediante:

```python
require_permission_web(Resources.ACTIVITIES, Actions.READ)
require_permission_web(Resources.ACTIVITIES, Actions.CREATE)
require_permission_web(Resources.ACTIVITIES, Actions.UPDATE)
require_permission_web(Resources.ACTIVITIES, Actions.DELETE)
```

:contentReference[oaicite:3]{index=3}

---

# Autorización Contextual

Además del permiso global, se utiliza:

```python
ensure_can_view_activity()
```

para validar acceso contextual a la actividad. :contentReference[oaicite:4]{index=4}

---

# Filtrado Contextual

El listado se adapta según rol.

## Admin

Puede ver todas las actividades.

## Estudiante

Solo ve sus propias actividades:

```text
Activity.user_id == current_user.id_usuario
```

## Profesor / Coordinador

Ve actividades de proyectos donde participa.

El router obtiene los `project_id` desde `ProjectMember` y filtra actividades por tareas pertenecientes a esos proyectos. :contentReference[oaicite:5]{index=5}

---

# Flujo de Creación

```text
POST /activities/form
    ↓
validar tarea
    ↓
crear fake_activity para autorización contextual
    ↓
ensure_can_view_activity()
    ↓
si estudiante: user_id = current_user.id_usuario
    ↓
crear Activity
    ↓
db.flush()
    ↓
create_feed_event(ACTIVITY_CREATED)
    ↓
db.commit()
    ↓
flash_success()
    ↓
redirect detalle
```

:contentReference[oaicite:6]{index=6}

---

# Flujo de Actualización

```text
POST /activities/{id}/edit
    ↓
cargar actividad con task/project/user
    ↓
ensure_can_view_activity()
    ↓
validar nueva tarea
    ↓
validar acceso contextual a nueva tarea
    ↓
actualizar campos
    ↓
si cambia nombre o estado:
        create_feed_event(ACTIVITY_UPDATED)
    ↓
db.commit()
    ↓
flash_success()
    ↓
redirect detalle
```

:contentReference[oaicite:7]{index=7}

---

# Flujo de Eliminación

```text
POST /activities/{id}/delete
    ↓
cargar actividad con task/project/user
    ↓
ensure_can_view_activity()
    ↓
create_feed_event(ACTIVITY_DELETED)
    ↓
db.delete(activity)
    ↓
db.commit()
    ↓
flash_success()
    ↓
redirect listado
```

:contentReference[oaicite:8]{index=8}

---

# Activity Feed Integration

El módulo genera eventos funcionales:

```text
ACTIVITY_CREATED
ACTIVITY_UPDATED
ACTIVITY_DELETED
```

Estos eventos alimentan:

- feed de proyecto,
- dashboard,
- realtime activity stream.

:contentReference[oaicite:9]{index=9}

---

# Flash / Toast Integration

El módulo usa:

```python
flash_success()
```

para feedback SSR tras:

- crear actividad,
- actualizar actividad,
- eliminar actividad.

:contentReference[oaicite:10]{index=10}

---

# Vista de Listado

Archivo:

```text
activities_list.html
```

Usa arquitectura reusable:

- `page_header`,
- `section_card`,
- `filters_bar`,
- `input`,
- `select`,
- `data_table`,
- `activity_row`.

:contentReference[oaicite:11]{index=11}

---

# Capacidades del Listado

## Filtros

```text
search
status
task_id
```

---

## Estadísticas

Cards:

```text
total actividades
pendientes
en progreso
completadas
```

---

## Tabla reusable

La tabla se renderiza mediante:

```jinja2
data_table(..., row_renderer=activity_row)
```

:contentReference[oaicite:12]{index=12}

---

# Row Component

Archivo:

```text
activity_row.html
```

Renderiza cada actividad de forma homogénea. :contentReference[oaicite:13]{index=13}

---

# Capacidades

- ID,
- nombre enlazado,
- tarea asociada,
- usuario,
- estado con badge,
- horas,
- acciones contextuales.

---

# Seguridad Visual

El componente usa:

```jinja2
can("read", "activities", activity)
can("update", "activities", activity)
can("delete", "activities", activity)
```

:contentReference[oaicite:14]{index=14}

---

# Confirm Dialog

El borrado usa el sistema reusable:

```text
js-confirm-form
```

con atributos:

```text
data-confirm-title
data-confirm-text
data-confirm-button
```

:contentReference[oaicite:15]{index=15}

---

# Vista de Detalle

Archivo:

```text
activities_detail.html
```

La vista detalle ya tiene diseño avanzado y muestra:

- cabecera de actividad,
- estado,
- horas invertidas,
- usuario,
- tarea asociada,
- proyecto,
- descripción,
- adjuntos,
- subida de archivos,
- acciones contextuales.

:contentReference[oaicite:16]{index=16}

---

# Detail Layout

La vista detalle utiliza cards de información:

```text
activity-info-card
```

y una estructura visual moderna orientada a:

```text
enterprise admin detail view
```

:contentReference[oaicite:17]{index=17}

---

# Integración con Tareas

La actividad enlaza directamente con su tarea asociada.

Desde el detalle se puede:

- ver tarea,
- crear nueva actividad en la misma tarea.

:contentReference[oaicite:18]{index=18}

---

# Integración con Proyectos

La actividad obtiene proyecto a través de:

```text
activity.task.project
```

Esto permite navegación hacia el proyecto relacionado. :contentReference[oaicite:19]{index=19}

---

# Integración con Adjuntos

El detalle de actividad incluye un submódulo completo de adjuntos.

## Funciones visibles

- subir archivo,
- añadir descripción,
- listar adjuntos,
- mostrar icono según MIME,
- mostrar uploader,
- mostrar tamaño,
- mostrar fecha,
- descargar,
- eliminar.

:contentReference[oaicite:20]{index=20}

---

# Upload de Adjuntos

La subida se realiza mediante:

```text
POST /activity-attachments/upload
```

con:

```text
multipart/form-data
```

Campos:

```text
activity_id
file
description
```

:contentReference[oaicite:21]{index=21}

---

# Borrado de Adjuntos

El borrado de adjunto usa confirmación visual basada en:

```javascript
confirmAction()
```

:contentReference[oaicite:22]{index=22}

---

# MIME-aware UI

La vista detalle selecciona iconografía según `mime_type`:

```text
pdf
image
word
excel/spreadsheet
zip/compressed
text
default file
```

:contentReference[oaicite:23]{index=23}

---

# Integración con CSS

El módulo carga:

```html
/static/css/activities.css
```

en listado y detalle. 

---

# Diferencia con Tasks

## Tasks

Representan planificación:

```text
qué hay que hacer
```

## Activities

Representan ejecución:

```text
qué se ha hecho
cuánto tiempo se ha dedicado
qué evidencias existen
```

---

# Estado Actual

## Implementado

- CRUD SSR completo,
- listado con filtros,
- contadores,
- detalle moderno,
- integración con tareas,
- integración con proyectos,
- integración con usuarios,
- integración con adjuntos,
- activity feed,
- flash/toasts,
- dialogs,
- autorización contextual.

---

# Limitaciones actuales

## 1. No existe service layer propia

La lógica vive en `activities_web.py`.

Recomendación:

```text
crear activity_service.py
```

---

## 2. Estados como string

Los estados usan strings directos.

Recomendación:

```text
ActivityStatusEnum
```

---

## 3. Sin auditoría técnica completa

Actualmente sí se alimenta activity feed, pero no se observa integración explícita con `AuditLog` para create/update/delete de actividades.

---

## 4. Sin notificaciones propias

El módulo no parece generar notificaciones directas en creación/edición/borrado.

---

## 5. Validación de horas mejorable

`time_spent` debería protegerse con:

```text
time_spent >= 0
```

---

# Mejoras Futuras

## Corto plazo

- extraer `activity_service.py`,
- añadir `ActivityStatusEnum`,
- añadir auditoría técnica,
- sustituir JS inline de adjuntos por patrón reusable.

---

## Medio plazo

- notificaciones por actividad relevante,
- filtros por proyecto,
- timeline de actividades,
- dashboard de horas,
- validación avanzada de tiempo.

---

## Largo plazo

- tipos de actividad,
- comentarios,
- evidencias estructuradas,
- métricas por usuario/proyecto,
- integración con competiciones,
- analítica de productividad.

---

# Valor Arquitectónico

El módulo Activities es clave porque convierte la plataforma en un sistema de seguimiento real.

Permite pasar de:

```text
gestión de tareas
```

a:

```text
trazabilidad de trabajo realizado
```

---

# Conclusión

El módulo de actividades ya está bastante maduro en UI y funcionalidad.

Actualmente aporta:

- seguimiento operativo,
- control de horas,
- evidencias mediante adjuntos,
- conexión con tareas,
- conexión con proyectos,
- activity feed,
- autorización contextual,
- UX avanzada SSR.

La principal mejora arquitectónica pendiente es extraer la lógica del router hacia una `activity_service.py` dedicada.