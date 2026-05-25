# 34_ACTIVITY_FEED_MODULE.md

# Módulo Activity Feed

# Objetivo

El módulo Activity Feed proporciona trazabilidad funcional y colaboración realtime dentro de Aula Robótica Platform.

Actualmente permite:

- registrar eventos funcionales,
- mostrar actividad reciente,
- alimentar dashboards,
- alimentar feeds de proyecto,
- emitir eventos realtime,
- generar timelines colaborativos,
- sincronizar actividad entre usuarios.

---

# Filosofía del módulo

El Activity Feed NO es auditoría técnica.

Representa:

```text
actividad funcional y operativa
```

orientada a:

- colaboración,
- visibilidad,
- UX,
- contexto de proyecto.

---

# Diferencia con Auditoría

# Audit System

Orientado a:

```text
seguridad
compliance
trazabilidad técnica
```

---

# Activity Feed

Orientado a:

```text
colaboración
actividad funcional
timeline operativo
realtime UX
```

---

# Filosofía Arquitectónica

Separar ambos sistemas permite:

- menor acoplamiento,
- mejor UX,
- distinta retención,
- distinta semántica,
- distinta visualización.

---

# Arquitectura General

```text
Task / Project / Activity Event
        ↓
create_feed_event()
        ↓
ProjectActivityFeed
        ↓
Realtime Emitters
        ↓
Dashboard Feed
        ↓
Project Feed
        ↓
Live Timeline UI
```

---

# Componentes Principales

## Backend

```text
app/modules/activity_feed/
├── activity_feed_constants.py
├── activity_feed_model.py
└── activity_feed_service.py
```

---

# Frontend Integrado

El feed se consume principalmente desde:

```text
dashboard.html
projects_detail.html
```



---

# Modelo Principal

Archivo:

```text
activity_feed_model.py
```

:contentReference[oaicite:1]{index=1}

---

# Entidad Principal

```python
ProjectActivityFeed
```

---

# Objetivo del Modelo

Representar eventos funcionales asociados a proyectos.

---

# Campos principales

```text
id_feed
project_id
user_id
event_type
message
entity_type
entity_id
created_at
```

:contentReference[oaicite:2]{index=2}

---

# Arquitectura del Modelo

# Relación Project

```text
Feed N ─── 1 Project
```

---

# Relación User

```text
Feed N ─── 1 User
```

---

# Entity Reference Pattern

El modelo usa:

```text
entity_type
entity_id
```

en lugar de múltiples foreign keys rígidas.

:contentReference[oaicite:3]{index=3}

---

# Beneficios

- desacoplamiento,
- flexibilidad,
- extensibilidad,
- soporte multi-entidad.

---

# Event Types

Archivo:

```text
activity_feed_constants.py
```

:contentReference[oaicite:4]{index=4}

---

# Clase Principal

```python
FeedEvent
```

---

# Eventos soportados

# Tasks

```text
TASK_CREATED
TASK_UPDATED
TASK_DELETED
TASK_STATUS_CHANGED
```

---

# Activities

```text
ACTIVITY_CREATED
ACTIVITY_UPDATED
ACTIVITY_DELETED
```

---

# Projects

```text
PROJECT_CREATED
PROJECT_UPDATED
PROJECT_DELETED
```

---

# Members

```text
MEMBER_JOINED
MEMBER_REMOVED
```

:contentReference[oaicite:5]{index=5}

---

# Filosofía de Eventos

Los eventos representan:

```text
acciones relevantes para colaboración
```

NO todos los cambios internos del sistema.

---

# Service Layer

Archivo:

```text
activity_feed_service.py
```

:contentReference[oaicite:6]{index=6}

---

# Función Principal

## create_feed_event()

Core del sistema de feed.

---

# Responsabilidades

## Persistencia DB

Crear entrada de feed.

---

## Broadcast realtime

Emitir evento:

- dashboard,
- proyecto.

---

## Payload normalization

Estructurar datos para frontend.

---

# Pipeline Completo

```text
Task/Project/Activity action
    ↓
create_feed_event()
    ↓
ProjectActivityFeed()
    ↓
db.add()
    ↓
db.flush()
    ↓
emit_project_event()
    ↓
emit_dashboard_event()
```

:contentReference[oaicite:7]{index=7}

---

# Persistencia

El evento se persiste mediante:

```python
db.add(feed_entry)
db.flush()
```

:contentReference[oaicite:8]{index=8}

---

# Payload Realtime

# Project Event

```python
emit_project_event()
```

---

# Dashboard Event

```python
emit_dashboard_event()
```

:contentReference[oaicite:9]{index=9}

---

# Payload emitido

```json
{
  "type": "feed_event",
  "activity": {
    "feed_id": ...,
    "event_type": ...,
    "message": ...,
    "user_id": ...,
    "created_at": ...
  }
}
```

:contentReference[oaicite:10]{index=10}

---

# Filosofía Realtime

El feed funciona como:

```text
live operational timeline
```

---

# Dashboard Integration

El dashboard consume:

```python
recent_feed
```

:contentReference[oaicite:11]{index=11}

---

# Dashboard Feed UI

El dashboard renderiza:

```text
Actividad reciente
```

como timeline vivo.

:contentReference[oaicite:12]{index=12}

---

# Dashboard Realtime

El dashboard escucha:

```text
dashboard_feed_event
```

vía WebSockets. :contentReference[oaicite:13]{index=13}

---

# Project Feed Integration

El detalle de proyecto integra:

```jinja2
project_feed(feed_events)
```

:contentReference[oaicite:14]{index=14}

---

# Filosofía

Cada proyecto posee su timeline contextual.

---

# Feed Contextual

El feed del proyecto muestra:

- actividad relevante,
- cambios recientes,
- colaboración viva,
- evolución del proyecto.

---

# Eventos que alimentan el feed

# Tasks

## Creación

```text
TASK_CREATED
```

---

## Cambio de estado

```text
TASK_STATUS_CHANGED
```

---

## Actualización

```text
TASK_UPDATED
```

---

## Eliminación

```text
TASK_DELETED
```

---

# Activities

## Registro trabajo

```text
ACTIVITY_CREATED
```

---

## Actualización

```text
ACTIVITY_UPDATED
```

---

## Eliminación

```text
ACTIVITY_DELETED
```

---

# Projects

## Cambios estructurales

```text
PROJECT_CREATED
PROJECT_UPDATED
```

---

# Membership

## Colaboración

```text
MEMBER_JOINED
MEMBER_REMOVED
```

---

# Arquitectura Visual

# Timeline Pattern

El feed usa patrón:

```text
timeline / activity stream
```

---

# Feed Items

Cada item contiene:

- mensaje,
- usuario implícito,
- fecha,
- entidad relacionada.

---

# Feed UX

La UI prioriza:

- lectura rápida,
- contexto,
- realtime,
- colaboración.

---

# Dashboard Feed

El dashboard muestra:

```text
últimos 8 eventos
```



---

# Feed Realtime

Los nuevos eventos:

- aparecen instantáneamente,
- animan entrada,
- eliminan empty state,
- mantienen límite visual.

:contentReference[oaicite:16]{index=16}

---

# Anti-Duplicados

El frontend usa:

```javascript
data-feed-id
```

:contentReference[oaicite:17]{index=17}

---

# Arquitectura Desacoplada

El módulo NO depende directamente de:

- dashboard,
- projects UI,
- notifications.

Solo emite eventos estructurados.

---

# Beneficios

- reutilización,
- escalabilidad,
- múltiples consumidores realtime.

---

# Integración con WebSockets

El módulo usa:

```python
emit_project_event()
emit_dashboard_event()
```

:contentReference[oaicite:18]{index=18}

---

# Rooms soportadas

# Dashboard Room

Feed global.

---

# Project Room

Feed contextual por proyecto.

---

# Integración con Notifications

Actualmente son sistemas separados.

---

# Notifications

Orientadas a:

```text
usuario específico
```

---

# Activity Feed

Orientado a:

```text
timeline colectivo
```

---

# Integración con Audit

Ambos sistemas pueden coexistir visualmente.

---

# Audit

```text
seguridad
```

---

# Feed

```text
actividad funcional
```

---

# Seguridad

# Contextual Visibility

Los usuarios solo reciben:

- feeds de proyectos accesibles,
- dashboard contextual.

---

# Backend-first

Toda visibilidad se filtra desde queries backend.

---

# Estado Actual

## Implementado

- modelo desacoplado,
- eventos tipados,
- service layer,
- realtime,
- dashboard integration,
- project integration,
- timeline visual,
- feed contextual,
- anti-duplicados,
- broadcast global,
- broadcast por proyecto.

---

# Limitaciones actuales

## 1. Sin paginación

El feed es limitado/manual.

---

## 2. Sin filtros

No existen filtros:

- tipo,
- usuario,
- entidad.

---

## 3. Sin iconografía tipada realtime

El payload no incluye metadata visual avanzada.

---

## 4. Sin agrupación

Eventos repetidos no se consolidan.

---

## 5. Sin persistencia analytics

No existen métricas históricas del feed.

---

## 6. Sin feed multi-proyecto

No existe timeline agregado personalizado.

---

# Mejoras Futuras

## Corto plazo

- iconografía contextual,
- filtros,
- metadata visual,
- timestamps relativos.

---

## Medio plazo

- agrupación,
- infinite scroll,
- búsqueda,
- feed híbrido audit+activity.

---

## Largo plazo

- analytics,
- event sourcing parcial,
- observabilidad operacional,
- timeline distribuido,
- feed intelligence,
- ML activity insights.

---

# Valor Arquitectónico

El Activity Feed es una de las piezas que más acerca el proyecto a una plataforma moderna tipo:

```text
Realtime Collaborative Operations Platform
```

---

# Conclusión

El sistema actual ya representa una arquitectura sorprendentemente madura.

Actualmente aporta:

- timelines vivos,
- realtime,
- colaboración contextual,
- desacoplamiento,
- feeds por proyecto,
- feed global,
- integración dashboard,
- integración WebSocket,
- trazabilidad funcional.

El siguiente gran salto evolutivo será:

```text
event-driven operational intelligence
```