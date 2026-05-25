# 29_TASKS_MODULE.md

# Módulo de Tareas

## Objetivo

El módulo de tareas gestiona el trabajo operativo dentro de los proyectos de Aula Robótica Platform.

No es únicamente un CRUD de tareas. Actualmente actúa como núcleo de coordinación funcional entre:

- proyectos,
- miembros,
- responsables,
- actividades,
- Kanban,
- auditoría,
- activity feed,
- notificaciones,
- realtime.

---

# Responsabilidad del módulo

El módulo permite:

- crear tareas dentro de proyectos,
- asignar tareas a usuarios,
- editar datos funcionales,
- cambiar estados Kanban,
- eliminar tareas,
- consultar tareas con filtros,
- visualizar detalle de tarea,
- consultar actividades asociadas,
- consultar auditoría de tarea,
- emitir eventos realtime,
- generar notificaciones.

---

# Arquitectura General

```text
Tasks Web Router
        ↓
Task Service
        ↓
Task Model
        ↓
Audit Service
        ↓
Activity Feed
        ↓
Notifications
        ↓
WebSockets
        ↓
SSR / Realtime UI
```

---

# Componentes Principales

## Backend

```text
app/modules/tasks/
├── task_model.py
├── task_service.py
├── task_view_service.py
└── tasks_web.py
```

---

## Frontend SSR

```text
templates/tasks/
├── tasks_list.html
├── tasks_detail.html
└── tasks_form.html
```

---

## Componentes UI

```text
templates/components/task_row.html
templates/components/data_table.html
templates/components/section_card.html
```

---

## Realtime relacionado

```text
templates/projects/projects_detail.html
static/js/projects/project_detail.js
```

---

# Modelo de Tarea

La entidad `Task` representa una unidad de trabajo dentro de un proyecto.

## Campos principales

```text
id_task
project_id
name
description
status
priority
assigned_to
created_by
due_date
created_at
```

---

# Estados de tarea

El módulo usa un workflow Kanban simple:

```text
todo
doing
done
```

---

# Prioridades

Las tareas pueden clasificarse como:

```text
low
medium
high
```

---

# Relaciones

## Task → Project

Cada tarea pertenece obligatoriamente a un proyecto.

```text
Task N ─── 1 Project
```

---

## Task → Assignee

Una tarea puede estar asignada a un usuario.

```text
Task N ─── 0..1 User
```

---

## Task → Activities

Una tarea puede tener múltiples actividades asociadas.

```text
Task 1 ─── N Activity
```

Las actividades se eliminan como huérfanas cuando se elimina la tarea.

---

# Router Web

Archivo:

```text
tasks_web.py
```

El router expone las rutas SSR principales del módulo. :contentReference[oaicite:0]{index=0}

---

# Rutas Principales

## Listado

```text
GET /tasks/
```

Permite:

- búsqueda,
- filtrado por estado,
- filtrado por proyecto,
- paginación,
- contadores por estado.

---

## Formulario de creación

```text
GET /tasks/form
```

---

## Crear tarea

```text
POST /tasks/form
```

---

## Formulario de edición

```text
GET /tasks/{task_id}/edit
```

---

## Actualizar tarea

```text
POST /tasks/{task_id}/edit
```

---

## Detalle

```text
GET /tasks/{task_id}
```

---

## Eliminar

```text
POST /tasks/{task_id}/delete
```

---

## Cambio de estado Kanban

```text
POST /tasks/{task_id}/status
```

El endpoint de cambio de estado devuelve JSON:

```json
{
  "ok": true
}
```

y se usa desde el Kanban realtime. :contentReference[oaicite:1]{index=1}

---

# Seguridad del módulo

El módulo usa seguridad backend-first.

## Guards principales

```python
require_permission_web(Resources.TASKS, Actions.READ)
require_permission_web(Resources.TASKS, Actions.CREATE)
require_permission_web(Resources.TASKS, Actions.UPDATE)
require_permission_web(Resources.TASKS, Actions.DELETE)
```

:contentReference[oaicite:2]{index=2}

---

# Autorización contextual

Además del permiso global, el módulo aplica autorización contextual mediante:

```python
can_user_action()
ensure_can_view_task()
```



---

# Filtrado contextual en listado

El listado adapta los resultados según rol:

## Admin

Ve todas las tareas.

## Estudiante

Ve solo tareas asignadas a sí mismo.

## Profesor / Coordinador

Ve tareas de proyectos donde participa.

Este filtrado se aplica directamente en la query del listado. :contentReference[oaicite:4]{index=4}

---

# Validación de asignación

Al crear o actualizar una tarea, si se asigna un usuario, el sistema valida que pertenezca al proyecto.

```text
El usuario asignado debe ser miembro del proyecto.
```

Esto evita asignaciones inconsistentes. :contentReference[oaicite:5]{index=5}

---

# Service Layer

Archivo:

```text
task_service.py
```

Contiene la lógica de negocio principal del módulo. :contentReference[oaicite:6]{index=6}

---

# Funciones principales

## create_task()

Crea una tarea básica validando proyecto y permisos.

---

## update_task_status()

Actualiza estado de tarea de forma simple.

---

## create_task_with_audit()

Crea tarea e integra:

- auditoría,
- WebSocket,
- activity feed,
- notificación al responsable.

:contentReference[oaicite:7]{index=7}

---

## change_task_status_with_audit()

Gestiona el cambio de estado Kanban.

Incluye:

- validación de estado,
- persistencia,
- auditoría,
- evento realtime,
- activity feed,
- notificación al responsable.

:contentReference[oaicite:8]{index=8}

---

## update_task_with_audit()

Actualiza campos auditables de tarea.

Campos auditados:

```text
name
description
project_id
assigned_to
status
priority
```

:contentReference[oaicite:9]{index=9}

---

## delete_task_with_audit()

Elimina tarea e integra:

- auditoría,
- WebSocket,
- activity feed.

:contentReference[oaicite:10]{index=10}

---

# Pipeline Operacional

## Crear tarea

```text
POST /tasks/form
    ↓
validar proyecto
    ↓
validar permisos
    ↓
validar assigned_to ∈ project_members
    ↓
create_task_with_audit()
    ↓
AuditLog CREATE_TASK
    ↓
emit_project_event()
    ↓
FeedEvent.TASK_CREATED
    ↓
Notification TASK_ASSIGNED
    ↓
redirect detalle
```

---

## Cambiar estado

```text
POST /tasks/{id}/status
    ↓
require_permission_web(tasks:update)
    ↓
ensure_can_view_task()
    ↓
change_task_status_with_audit()
    ↓
TaskStatusEnum validation
    ↓
AuditLog UPDATE_TASK
    ↓
emit_project_event()
    ↓
FeedEvent.TASK_STATUS_CHANGED
    ↓
Notification TASK_STATUS_CHANGED
    ↓
JSON { ok: true }
```

---

## Editar tarea

```text
POST /tasks/{id}/edit
    ↓
validar existencia
    ↓
ensure_can_view_task()
    ↓
can_user_action(update, tasks, task)
    ↓
validar assigned_to
    ↓
update_task_with_audit()
    ↓
AuditLog UPDATE_TASK
    ↓
FeedEvent.TASK_UPDATED
    ↓
Notification TASK_ASSIGNED si cambia responsable
    ↓
redirect detalle
```

---

# Task Detail View Service

Archivo:

```text
task_view_service.py
```

Construye la vista detallada de tarea. :contentReference[oaicite:11]{index=11}

---

# Responsabilidades

## Carga eficiente

Carga:

- tarea,
- proyecto,
- usuario asignado.

---

## Validación contextual

Valida lectura mediante:

```python
can_user_action(Actions.READ, Resources.TASKS, current_user, task)
```

---

## Usuarios disponibles

Obtiene usuarios disponibles para reasignación si el usuario puede gestionar la tarea.

---

## Auditoría agrupada

Agrupa logs por día:

```text
Hoy
Ayer
dd/mm/yyyy
```

:contentReference[oaicite:12]{index=12}

---

## Permisos preparados para UI

Devuelve:

```python
can_edit
can_delete
```

para render contextual.

---

# Vista de Listado

Archivo:

```text
tasks_list.html
```

La vista de listado usa componentes reutilizables:

- `page_header`,
- `section_card`,
- `filters_bar`,
- `input`,
- `select`,
- `data_table`,
- `task_row`.

:contentReference[oaicite:13]{index=13}

---

# Capacidades del listado

## Filtros

- texto,
- estado,
- proyecto.

---

## Estadísticas

Cards:

- total tareas,
- por hacer,
- en progreso,
- completadas.

---

## Tabla reusable

Render mediante:

```jinja2
data_table(..., row_renderer=task_row)
```

:contentReference[oaicite:14]{index=14}

---

# Row Component

Archivo:

```text
task_row.html
```

Renderiza cada tarea de forma reusable. :contentReference[oaicite:15]{index=15}

---

# Capacidades

- enlace a detalle,
- enlace a proyecto,
- badge de estado,
- badge de prioridad,
- acciones contextuales,
- confirm dialog para borrado.

---

# Seguridad visual

Usa:

```jinja2
can("read", "tasks", task)
can("update", "tasks", task)
can("delete", "tasks", task)
```

:contentReference[oaicite:16]{index=16}

---

# Vista de Detalle

Archivo:

```text
tasks_detail.html
```

Muestra:

- información de tarea,
- proyecto,
- estado,
- prioridad,
- responsable,
- actividades,
- horas registradas,
- descripción,
- timeline de auditoría.

:contentReference[oaicite:17]{index=17}

---

# Actividades asociadas

La vista detalle integra el módulo de actividades mostrando:

- ID,
- nombre,
- usuario,
- estado,
- horas,
- acciones.

El render de actividades usa:

```jinja2
activity_row(activity)
```

:contentReference[oaicite:18]{index=18}

---

# Timeline de Auditoría

El detalle incluye timeline visual agrupado por fecha.

Utiliza helpers globales:

```jinja2
get_audit_icon()
get_audit_color()
```

:contentReference[oaicite:19]{index=19}

---

# Integración Kanban

El módulo de tareas está integrado en `projects_detail.html`.

---

# Kanban por proyecto

La vista de proyecto renderiza tres columnas:

```text
Por hacer
En progreso
Completado
```

Cada columna agrupa tareas por estado. :contentReference[oaicite:20]{index=20}

---

# Interacción Kanban

Cada tarea puede moverse mediante:

- drag & drop,
- botones contextuales:
  - Empezar,
  - Finalizar.

:contentReference[oaicite:21]{index=21}

---

# Autorización visual Kanban

Solo las tareas editables son arrastrables:

```jinja2
{% if can("update", "tasks", task) %}draggable="true"{% endif %}
```

:contentReference[oaicite:22]{index=22}

---

# JS Realtime

Archivo:

```text
project_detail.js
```

Gestiona:

- drag & drop,
- botones de cambio de estado,
- optimistic UI,
- rollback,
- WebSocket de proyecto,
- online users,
- audit timeline realtime,
- activity feed realtime,
- contadores Kanban,
- empty states.

:contentReference[oaicite:23]{index=23}

---

# Cambio de estado frontend

El JS ejecuta:

```text
fetch POST /tasks/{taskId}/status
```

con:

```text
new_status=...
```

:contentReference[oaicite:24]{index=24}

---

# Optimistic UI

El cambio visual se aplica antes de recibir respuesta backend.

Si falla:

- se hace rollback,
- se refrescan contadores,
- se marca error visual.

:contentReference[oaicite:25]{index=25}

---

# Realtime WebSocket

El módulo escucha eventos:

```text
users_online
task_updated
audit
feed_event
```

:contentReference[oaicite:26]{index=26}

---

# Integración Audit

Cada acción relevante genera auditoría:

- crear tarea,
- editar tarea,
- borrar tarea,
- cambiar estado.

---

# Integración Activity Feed

Eventos generados:

```text
TASK_CREATED
TASK_UPDATED
TASK_DELETED
TASK_STATUS_CHANGED
```

:contentReference[oaicite:27]{index=27}

---

# Integración Notifications

Eventos generados:

```text
TASK_ASSIGNED
TASK_STATUS_CHANGED
```

cuando existe usuario responsable distinto del actor. :contentReference[oaicite:28]{index=28}

---

# Integración Dashboard

Los eventos de tareas alimentan:

- activity feed global,
- dashboard realtime,
- métricas futuras.

---

# Integración con Projects

Tasks depende fuertemente de Projects:

- toda tarea pertenece a un proyecto,
- la autorización se contextualiza por proyecto,
- los miembros del proyecto determinan asignaciones válidas,
- el Kanban vive dentro del detalle de proyecto.

---

# Integración con Activities

Las actividades cuelgan de tareas.

El módulo Tasks actúa como contenedor operativo de:

```text
trabajo planificado
```

mientras Activities registra:

```text
trabajo realizado
```

---

# Estado Actual

## Implementado

- CRUD SSR de tareas,
- listado con filtros,
- contadores por estado,
- row reusable,
- detalle con actividades,
- timeline de auditoría,
- validación contextual,
- asignación a miembros,
- Kanban por proyecto,
- drag & drop,
- optimistic UI,
- WebSocket realtime,
- feed funcional,
- notificaciones.

---

# Limitaciones actuales

## 1. Orden Kanban no persistente

Actualmente se cambia estado, pero no se guarda posición dentro de columna.

---

## 2. Alert residual

En `project_detail.js` aún existe un `alert()` en error de cambio de estado.

Debe sustituirse por `showToast()` o `showError()`. :contentReference[oaicite:29]{index=29}

---

## 3. Project detail JS demasiado grande

`project_detail.js` concentra Kanban, feed, audit timeline y WebSocket.

Debería dividirse en módulos:

- `kanban.js`,
- `project_feed.js`,
- `audit_timeline.js`,
- `websocket.js`.

---

## 4. No hay subtareas

Pendiente si el dominio crece.

---

## 5. No hay etiquetas

Las tareas no tienen tags/categorías.

---

# Mejoras Futuras

## Corto plazo

- sustituir alert por toast,
- extraer JS Kanban,
- añadir indicadores de conexión,
- mejorar estados visuales de error.

---

## Medio plazo

- orden persistente en Kanban,
- filtros realtime,
- etiquetas,
- subtareas,
- comentarios en tareas.

---

## Largo plazo

- workflows configurables,
- automatizaciones,
- SLA / deadlines,
- analítica de productividad,
- asignaciones inteligentes.

---

# Valor Arquitectónico

El módulo Tasks es uno de los módulos más importantes del sistema porque conecta:

```text
Planificación
+
Ejecución
+
Colaboración
+
Realtime
+
Auditoría
+
Notificaciones
```

---

# Conclusión

El módulo de tareas ya no funciona como CRUD aislado.

Actualmente representa un sistema operativo colaborativo dentro de Aula Robótica Platform:

```text
Project Workflow Core
```

Permite coordinar trabajo, asignar responsables, seguir estados, registrar actividad, emitir eventos y mantener sincronizadas las vistas de proyecto en tiempo real.