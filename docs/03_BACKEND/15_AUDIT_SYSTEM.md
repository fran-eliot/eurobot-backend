# 15_AUDIT_SYSTEM.md

# Audit & Activity Tracking Architecture

## Propósito

Este documento describe la arquitectura completa de:

```text
auditoría,
activity feed,
trazabilidad,
event tracking,
timeline realtime,
monitorización funcional
```

implementada en Aula Robótica Platform.

La plataforma ha evolucionado desde un simple logging CRUD hacia un sistema híbrido de:

```text
Technical Audit System
+
Functional Activity Feed
+
Realtime Operational Tracking
```

---

# Filosofía Arquitectónica

La plataforma separa explícitamente:

```text
auditoría técnica
```

de:

```text
actividad funcional colaborativa
```

Esto permite:

- menor acoplamiento,
- mejor UX,
- mejor semántica,
- trazabilidad enterprise,
- evolución independiente.

---

# Arquitectura General

```text
User Action
    ↓
Service Layer
    ↓
Business Logic
    ↓
Audit Log
    ↓
Activity Feed
    ↓
Realtime Events
    ↓
Dashboard / Project UI
```

---

# Componentes Principales

| Componente | Propósito |
|---|---|
| AuditLog | Trazabilidad técnica |
| ProjectActivityFeed | Timeline funcional |
| audit_service | Registro centralizado |
| activity_feed_service | Feed colaborativo |
| audit_ui | Helpers visuales |
| WebSockets | Realtime propagation |

---

# Audit System

# Objetivo

Registrar:

```text
acciones críticas del sistema
```

para:

- seguridad,
- trazabilidad,
- diagnóstico,
- observabilidad,
- compliance futuro.

---

# Modelo Principal

## AuditLog

Ubicado en:

```text
app/modules/audit/audit_model.py
```

:contentReference[oaicite:0]{index=0}

---

# Estructura

## Campos principales

| Campo | Descripción |
|---|---|
| id_log | ID único |
| action | Acción auditada |
| user_id | Usuario ejecutor |
| resource_type | Tipo de recurso |
| resource_id | ID entidad afectada |
| description | Descripción enriquecida |
| ip_address | IP cliente |
| user_agent | Navegador/dispositivo |
| created_at | Timestamp UTC |

---

# Diseño

## Auditoría desacoplada

El modelo:

```text
NO depende de módulos específicos
```

y puede registrar cualquier entidad.

---

# Beneficios

## Escalabilidad

Permite auditar:

- usuarios,
- proyectos,
- tareas,
- actividades,
- adjuntos,
- autenticación,
- administración.

---

# Audit Actions

## audit_actions.py

Las acciones auditables están centralizadas en:

```text
app/core/constants/audit_actions.py
```

:contentReference[oaicite:1]{index=1}

---

# Ejemplos

## Auth

```python
LOGIN
LOGOUT
```

---

## Users

```python
CREATE_USER
UPDATE_USER
DELETE_USER
ACTIVATE_USER
DEACTIVATE_USER
```

---

## Projects

```python
CREATE_PROJECT
UPDATE_PROJECT
DELETE_PROJECT
```

---

## Tasks

```python
CREATE_TASK
UPDATE_TASK
DELETE_TASK
TASK_STATUS_CHANGE
```

---

# Audit Service Layer

## audit_service.py

Servicio centralizado:

```text
app/modules/audit/audit_service.py
```

:contentReference[oaicite:2]{index=2}

---

# Función Principal

## log_action()

Core reusable audit logger.

Parámetros:

```python
action
user_id
resource_type
resource_id
description
request
```

---

# Metadata HTTP

La auditoría almacena:

```python
request.client.host
request.headers["user-agent"]
```

:contentReference[oaicite:3]{index=3}

---

# Objetivo

Preparar:

```text
security forensics
incident analysis
auditability
```

---

# Auditoría Enriquecida

La plataforma NO almacena únicamente:

```text
"UPDATE_TASK"
```

sino descripciones completas.

---

# Ejemplos Reales

```text
Creó tarea "Diseño Kanban"
```

```text
Cambió estado:
todo → doing
```

```text
Actualizó:
Prioridad: medium → high
```

---

# Filosofía

El audit log debe ser:

```text
human-readable
```

y no únicamente técnico.

---

# Integración con Service Layer

La auditoría está integrada directamente en:

```text
service layer
```

---

# Ejemplos

## task_service.py

La creación de tareas:

- crea entidad,
- registra auditoría,
- genera feed,
- emite realtime,
- crea notificaciones.

:contentReference[oaicite:4]{index=4}

---

# Cambio de estado realtime

```python
change_task_status_with_audit()
```

integra:

- auditoría,
- WebSockets,
- feed,
- notificaciones.

:contentReference[oaicite:5]{index=5}

---

# Beneficios

## Consistencia

Toda acción crítica sigue:

```text
mismo pipeline operacional
```

---

# Activity Feed System

# Filosofía

El Activity Feed NO es auditoría técnica.

Es:

```text
timeline funcional colaborativa
```

---

# Objetivo

Mostrar:

- actividad reciente,
- colaboración,
- evolución proyecto,
- cambios importantes.

---

# Modelo Principal

## ProjectActivityFeed

Ubicado en:

```text
app/modules/activity_feed/activity_feed_model.py
```

:contentReference[oaicite:6]{index=6}

---

# Campos principales

| Campo | Descripción |
|---|---|
| project_id | Proyecto asociado |
| user_id | Usuario actor |
| event_type | Tipo evento |
| message | Mensaje funcional |
| entity_type | Tipo entidad |
| entity_id | Entidad afectada |
| created_at | Timestamp UTC |

---

# Feed Events

## activity_feed_constants.py

Eventos funcionales centralizados.

:contentReference[oaicite:7]{index=7}

---

# Eventos actuales

## Tasks

```python
TASK_CREATED
TASK_UPDATED
TASK_DELETED
TASK_STATUS_CHANGED
```

---

## Activities

```python
ACTIVITY_CREATED
ACTIVITY_UPDATED
ACTIVITY_DELETED
```

---

## Projects

```python
PROJECT_CREATED
PROJECT_UPDATED
PROJECT_DELETED
```

---

## Members

```python
MEMBER_JOINED
MEMBER_REMOVED
```

---

# Feed Service

## create_feed_event()

Servicio principal:

```text
app/modules/activity_feed/activity_feed_service.py
```

:contentReference[oaicite:8]{index=8}

---

# Capacidades

## Persistencia

Guarda evento funcional.

---

## Realtime

Emite automáticamente:

```python
emit_project_event()
emit_dashboard_event()
```

:contentReference[oaicite:9]{index=9}

---

# Resultado

Los feeds son:

```text
persistentes + realtime
```

---

# Arquitectura Realtime

La auditoría moderna está integrada con:

```text
WebSocket architecture
```

---

# Tipos de eventos

## Audit events

```json
{
  "type": "audit"
}
```

---

## Feed events

```json
{
  "type": "feed_event"
}
```

---

## Dashboard feed events

```json
{
  "type": "dashboard_feed_event"
}
```

---

# Objetivos

## Dashboard vivo

Timeline realtime.

---

## Kanban colaborativo

Cambios instantáneos.

---

## UX moderna

Experiencia tipo:

```text
enterprise admin console
```

---

# Audit UI Helpers

## audit_ui.py

Helpers visuales reutilizables.

:contentReference[oaicite:10]{index=10}

---

# Funciones

## get_audit_icon()

Mapea acciones a:

```text
FontAwesome icons
```

---

## get_audit_color()

Mapea acciones a:

```text
Bootstrap/AdminLTE colors
```

---

# Objetivo

Centralizar:

- iconografía,
- semántica visual,
- consistencia UI.

---

# Feed UI Helpers

## activity_feed_utils.py

Sistema equivalente para feeds.

:contentReference[oaicite:11]{index=11}

---

# Capacidades

## Iconografía contextual

```python
TASK_CREATED → fa-plus-circle
```

---

## Colores semánticos

```python
DELETED → bg-danger
UPDATED → bg-primary
```

---

# Dashboard Integration

El dashboard integra:

- métricas,
- audit logs,
- activity feed,
- realtime.

---

# dashboard_service.py

Obtiene:

```python
recent_logs
recent_feed
```

:contentReference[oaicite:12]{index=12}

---

# Arquitectura híbrida

```text
technical monitoring
+
operational collaboration
```

---

# Task Detail Audit Timeline

## task_view_service.py

Las tareas implementan:

```text
grouped audit timelines
```

:contentReference[oaicite:13]{index=13}

---

# Capacidades

## Agrupación temporal

```text
Hoy
Ayer
Fecha concreta
```

---

## Timeline visual

UI enterprise-style.

---

# Filosofía de Auditoría

La auditoría implementa:

```text
event sourcing parcial
```

aunque no full event sourcing.

---

# Características

## Enriquecida

Mensajes legibles.

---

## Contextual

Con entidad y usuario.

---

## Temporal

Timeline completo.

---

## Visual

Helpers UI centralizados.

---

## Realtime

Actualización instantánea.

---

# Diferencia Audit vs Feed

| Audit | Activity Feed |
|---|---|
| Seguridad | Colaboración |
| Técnico | Funcional |
| Compliance | UX |
| Administrativo | Operacional |
| Bajo nivel | Alto nivel |

---

# Beneficios Arquitectónicos

## Desacoplamiento

Menor complejidad semántica.

---

## Escalabilidad

Cada sistema evoluciona independientemente.

---

## UX moderna

Timelines ricos y vivos.

---

## Enterprise readiness

Preparado para:

- observabilidad,
- compliance,
- analytics,
- monitoring.

---

# Integraciones Actuales

## Tasks

✔ Auditoría  
✔ Feed  
✔ Notifications  
✔ Realtime  

---

## Dashboard

✔ Feed realtime  
✔ Audit timeline  

---

## Projects

✔ Eventos funcionales  

---

## Users

✔ Auditoría administrativa  

---

# Limitaciones Actuales

## No existe retention policy

La auditoría crecerá indefinidamente.

---

## No existe async queue

Los eventos son síncronos.

---

## No existe observabilidad avanzada

Faltan:

- métricas,
- tracing,
- alerting.

---

## Feed parcialmente implementado

Algunos módulos aún no generan feed completo.

---

# Futuras Evoluciones

# Auditoría

## Objetivos futuros

- exportación,
- filtros avanzados,
- búsqueda full-text,
- compliance reports,
- retention policies.

---

# Feed

## Objetivos futuros

- comentarios,
- menciones,
- rich activity,
- attachments,
- collaboration analytics.

---

# Realtime

## Evolución futura

- Redis pub/sub,
- horizontal scaling,
- websocket persistence,
- reconnect strategies.

---

# Observabilidad

## Futuro enterprise

Integración posible con:

```text
Prometheus
Grafana
OpenTelemetry
ELK Stack
```

---

# Filosofía Final

La plataforma ya NO implementa únicamente:

```text
logs CRUD básicos
```

sino una arquitectura moderna de:

```text
auditoría técnica,
timeline funcional,
tracking operacional,
realtime collaboration,
event-driven UX.
```

Esto convierte Aula Robótica Platform en una:

```text
enterprise operational platform
```

con capacidades reales de:

- trazabilidad,
- colaboración,
- observabilidad,
- administración avanzada.