# 24_REALTIME_KANBAN.md

# Realtime Kanban Architecture

## Objetivo

Este documento describe la arquitectura realtime del sistema Kanban de Aula Robótica Platform.

El sistema permite:

- mover tareas en tiempo real,
- colaboración multiusuario,
- sincronización instantánea,
- actualización visual inmediata,
- auditoría integrada,
- activity feed live.

La arquitectura combina:

- SSR,
- WebSockets,
- drag & drop frontend,
- broadcasting por proyecto,
- eventos desacoplados.

---

# Filosofía del Sistema

El Kanban NO es simplemente una lista de tareas.

El objetivo es construir:

```text
Collaborative Realtime Workflow System
```

para coordinar:

- equipos,
- proyectos,
- tareas,
- flujo operativo.

---

# Objetivos Arquitectónicos

## 1. Colaboración realtime

Los usuarios deben visualizar cambios:

```text
instantáneamente
```

---

## 2. Arquitectura desacoplada

Separar:

- UI,
- drag & drop,
- persistencia,
- realtime,
- auditoría,
- feed funcional.

---

## 3. UX moderna

Inspiración conceptual:

- Jira,
- Linear,
- GitHub Projects,
- Trello,
- Notion.

---

## 4. Bajo acoplamiento

El sistema evita:

- lógica JS incrustada,
- rendering acoplado,
- polling continuo.

---

# Arquitectura General

```text
Drag & Drop
    ↓
POST /tasks/{id}/status
    ↓
Task Service
    ↓
Persistencia SQL
    ↓
Audit Log
    ↓
Activity Feed
    ↓
WebSocket Broadcast
    ↓
Realtime UI Update
```

---

# Componentes Principales

## Backend

### Task Service

Archivo:

```text
app/modules/tasks/task_service.py
```

:contentReference[oaicite:0]{index=0}

---

### Tasks Router

Archivo:

```text
app/modules/tasks/tasks_web.py
```

:contentReference[oaicite:1]{index=1}

---

### Task View Service

Archivo:

```text
app/modules/tasks/task_view_service.py
```

:contentReference[oaicite:2]{index=2}

---

## Frontend

### project_detail.html

Vista principal del Kanban.

---

### project_detail.js

Cliente drag & drop realtime.

---

### websocket.js

Infraestructura WS compartida.

---

# Filosofía SSR + Realtime

## Render inicial SSR

FastAPI + Jinja2 renderizan:

- columnas,
- tareas,
- badges,
- usuarios,
- estados.

---

## Mejora realtime

WebSockets enriquecen la experiencia.

---

# Arquitectura Kanban

## Estados actuales

```text
todo
doing
done
```



---

# Modelo de Estados

## todo

Pendiente.

---

## doing

En progreso.

---

## done

Finalizada.

---

# Arquitectura Visual

## Columnas

Cada estado representa:

```text
workflow lane
```

---

# Cards

Cada tarea se renderiza como:

```text
kanban-task
```

---

# Metadata UI

Las tareas incluyen:

- prioridad,
- responsable,
- estado,
- acciones,
- auditoría contextual.

---

# Drag & Drop

## Filosofía

El usuario modifica workflow:

```text
directamente desde UI
```

---

# Arquitectura Frontend

## Eventos

```javascript
dragstart
dragover
drop
```

---

# Flujo Drag & Drop

## 1. Usuario arrastra tarea

Card Kanban.

---

## 2. Detectar columna destino

```text
todo
doing
done
```

---

## 3. POST async

```text
/tasks/{id}/status
```

:contentReference[oaicite:4]{index=4}

---

## 4. Persistencia backend

```python
change_task_status_with_audit()
```

:contentReference[oaicite:5]{index=5}

---

## 5. Broadcasting realtime

```python
emit_project_event()
```

:contentReference[oaicite:6]{index=6}

---

## 6. Actualización clientes

Todos los usuarios conectados reciben evento.

---

# Endpoint Kanban

## Ruta principal

```python
POST /tasks/{task_id}/status
```

:contentReference[oaicite:7]{index=7}

---

# Validaciones

## 1. Task existente

```python
if not task:
```

---

## 2. Acceso contextual

```python
ensure_can_view_task()
```

---

## 3. Permisos

```python
require_permission_web()
```

:contentReference[oaicite:8]{index=8}

---

# change_task_status_with_audit()

## Core principal

Servicio centralizado.

:contentReference[oaicite:9]{index=9}

---

# Responsabilidades

## 1. Validar estado

```python
TaskStatusEnum
```

---

## 2. Persistencia

Actualizar task.

---

## 3. Auditoría

```python
log_action()
```

---

## 4. Realtime

```python
emit_project_event()
```

---

## 5. Activity Feed

```python
create_feed_event()
```

---

## 6. Notifications

```python
create_notification()
```

:contentReference[oaicite:10]{index=10}

---

# Arquitectura Event-Driven

El cambio Kanban dispara:

- auditoría,
- feed funcional,
- realtime,
- notificaciones.

---

# Payload Realtime

## Evento emitido

```json
{
  "type": "audit",
  "action": "UPDATE_TASK",
  "description": "...",
  "user": "...",
  "created_at": "..."
}
```

:contentReference[oaicite:11]{index=11}

---

# Rooms por Proyecto

## Arquitectura

Cada proyecto funciona como:

```text
room aislada
```

---

# Objetivo

Solo reciben eventos:

```text
usuarios del proyecto
```

---

# WebSocket Integration

## Emisión

```python
emit_project_event(project_id, payload)
```

:contentReference[oaicite:12]{index=12}

---

# Resultado

Realtime contextual.

---

# Activity Feed Integration

## Filosofía

Kanban alimenta:

```text
feed funcional del proyecto
```

---

# Evento generado

```python
FeedEvent.TASK_STATUS_CHANGED
```

:contentReference[oaicite:13]{index=13}

---

# Mensaje generado

```python
"{usuario} movió '{task}' a {estado}"
```

:contentReference[oaicite:14]{index=14}

---

# Auditoría Integrada

## Objetivo

Trazabilidad completa.

---

# Audit Log

Se registra:

```python
UPDATE_TASK
```

:contentReference[oaicite:15]{index=15}

---

# Información Auditada

- usuario,
- estado previo,
- nuevo estado,
- timestamp,
- contexto.

---

# Notifications Integration

## Casos

Si existe responsable:

```python
assigned_to
```

se genera notificación realtime.

:contentReference[oaicite:16]{index=16}

---

# Ejemplo

```text
"La tarea cambió a doing"
```

---

# Filosofía UX

El usuario recibe:

- feedback visual,
- toast,
- actualización instantánea,
- sincronización viva.

---

# Seguridad

## Seguridad backend-first

Toda validación ocurre en backend.

---

# Validaciones

## Roles

```python
require_permission_web()
```

---

## Contexto proyecto

```python
can_user_action()
```

---

## Ownership contextual

```python
ensure_can_view_task()
```



---

# Frontend Authorization

El frontend SSR oculta:

- acciones,
- edición,
- drag capability,
- controles contextuales.

---

# Arquitectura UI

## Realtime incremental

La página:

```text
NO recarga completamente
```

---

# Actualización parcial

Solo cambia:

- columna,
- card,
- contadores,
- feed,
- timeline.

---

# Arquitectura Modular

## Backend desacoplado

Separación entre:

- router,
- services,
- realtime,
- feed,
- audit.

---

## Frontend desacoplado

Separación entre:

- drag & drop,
- websocket,
- rendering,
- realtime updates.

---

# Integración con Dashboard

Los cambios Kanban impactan:

- métricas,
- activity feed,
- dashboard realtime.

---

# Integración con Notifications

Cambios relevantes generan:

- toast,
- notifications,
- badge updates.

---

# Integración con Audit Timeline

El detalle de tarea muestra:

```python
grouped_audit
```

:contentReference[oaicite:18]{index=18}

---

# Arquitectura Timeline

Agrupación por:

- Hoy,
- Ayer,
- fechas históricas.

:contentReference[oaicite:19]{index=19}

---

# Estado Actual

## Implementado

Incluye:

- drag & drop,
- realtime updates,
- project rooms,
- activity feed,
- audit integration,
- contextual security,
- notifications,
- SSR integration,
- task detail timeline,
- workflow visual.

---

# Limitaciones Actuales

## 1. Sin optimistic UI avanzada

El cambio espera confirmación backend.

---

## 2. Sin locks colaborativos

Dos usuarios pueden mover simultáneamente.

---

## 3. Sin presencia realtime

No existe:

```text
"usuario editando"
```

---

## 4. Sin ordenación compleja

Actualmente:

```text
sin ordering persistente avanzado
```

---

# Evolución Futura

## Corto plazo

- realtime counters,
- smooth animations,
- reconnect resiliente,
- visual sync indicators.

---

## Medio plazo

- ordering persistente,
- swimlanes,
- filtros realtime,
- etiquetas dinámicas,
- subtareas.

---

## Largo plazo

- collaborative editing,
- presence system,
- distributed realtime,
- Redis Pub/Sub,
- workflow engine,
- advanced automation.

---

# Visión Estratégica

El Kanban evolucionará hacia:

```text
Realtime Collaborative Robotics Workflow Platform
```

para coordinar:

- equipos,
- proyectos,
- competiciones,
- workflows educativos,
- operaciones técnicas.

---

# Relación con otros documentos

Relacionado con:

- `21_WEBSOCKET_SYSTEM.md`
- `22_REALTIME_DASHBOARD.md`
- `23_REALTIME_NOTIFICATIONS.md`
- `15_AUDIT_SYSTEM.md`
- `08_UI_ARCHITECTURE.md`
- `20_JS_ARCHITECTURE.md`
- `13_PROJECTS_MODULE.md`

---

# Conclusión

El sistema Kanban actual ya supera ampliamente un CRUD académico convencional.

La plataforma dispone actualmente de:

- workflow realtime,
- colaboración multiusuario,
- project rooms,
- drag & drop,
- broadcasting contextual,
- auditoría integrada,
- notifications realtime,
- activity feed,
- SSR + realtime híbrido,
- arquitectura desacoplada.

La siguiente evolución natural será:

```text
fully collaborative operational workflow system
```