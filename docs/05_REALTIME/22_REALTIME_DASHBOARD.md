# 22_REALTIME_DASHBOARD.md

# Realtime Dashboard Architecture

## Objetivo

Este documento describe la arquitectura realtime del dashboard principal de Aula Robótica Platform.

El dashboard funciona como:

```text
Realtime Operational Admin Console
```

capaz de mostrar:

- actividad reciente,
- métricas operativas,
- eventos colaborativos,
- actualizaciones vivas,
- feedback instantáneo.

La arquitectura está construida sobre:

- SSR con Jinja2,
- WebSockets,
- rendering incremental frontend,
- broadcasting desacoplado.

---

# Filosofía del Dashboard

El dashboard NO es simplemente una página de métricas estáticas.

El objetivo es evolucionar hacia:

```text
Live Operations Center
```

para el Aula de Robótica.

---

# Objetivos Arquitectónicos

## 1. Dashboard vivo

El usuario debe percibir:

- actividad constante,
- cambios en tiempo real,
- colaboración multiusuario,
- plataforma activa.

---

## 2. SSR-first

El dashboard se renderiza inicialmente vía:

```text
FastAPI + Jinja2
```

Luego:

```text
WebSockets enriquecen la experiencia
```

---

## 3. Bajo acoplamiento

Separar:

- render inicial,
- métricas,
- realtime,
- feeds,
- notificaciones.

---

## 4. Arquitectura enterprise

Inspiración conceptual:

- GitLab Admin,
- Jira Activity Streams,
- Linear,
- Notion realtime,
- internal admin consoles.

---

# Arquitectura General

```text
Dashboard Service
    ↓
SSR Render (Jinja2)
    ↓
Dashboard WebSocket
    ↓
Realtime Feed Updates
    ↓
Toast Notifications
    ↓
Incremental DOM Updates
```

---

# Componentes Principales

## Backend

### Dashboard Service

Archivo:

```text
app/modules/dashboard/dashboard_service.py
```

Responsable de:

- métricas,
- KPIs,
- queries agregadas,
- dashboards contextuales.

:contentReference[oaicite:0]{index=0}

---

### Dashboard Router

Archivo:

```text
app/modules/dashboard/dashboard_web.py
```

Responsable de:

- render SSR,
- permisos,
- contexto dashboard,
- carga inicial.

:contentReference[oaicite:1]{index=1}

---

### Dashboard WebSocket

Endpoint:

```text
/ws/dashboard
```

Responsable de:

- broadcasting realtime global,
- feed vivo,
- sincronización dashboard.

:contentReference[oaicite:2]{index=2}

---

## Frontend

### dashboard.html

Template SSR principal.

Archivo:

```text
templates/dashboard/dashboard.html
```

:contentReference[oaicite:3]{index=3}

---

### dashboard.js

Cliente realtime.

Archivo:

```text
static/js/dashboard/dashboard.js
```

:contentReference[oaicite:4]{index=4}

---

# Arquitectura SSR + Realtime

## Render Inicial SSR

FastAPI renderiza:

- cards KPI,
- charts,
- activity feed,
- auditoría,
- métricas.

---

## Mejora Realtime

Tras cargar página:

```javascript
connectDashboardWebSocket()
```

:contentReference[oaicite:5]{index=5}

---

## Resultado

La experiencia final es:

```text
SSR estable + realtime incremental
```

---

# Dashboard Contextual

## Filosofía

El dashboard cambia según:

- roles,
- permisos,
- pertenencia a proyectos,
- contexto usuario.

---

# Dashboard Admin

Incluye:

- usuarios,
- roles,
- identidades,
- auditoría global,
- métricas globales,
- actividad global.



---

# Dashboard Contextual

Usuarios no admin reciben:

- proyectos asociados,
- tareas personales,
- actividad contextual,
- feed contextual.

:contentReference[oaicite:7]{index=7}

---

# Dashboard Service

## Core Service

```python
get_dashboard_metrics()
```

:contentReference[oaicite:8]{index=8}

---

# Arquitectura por Roles

## Admin

Usa:

```python
get_admin_dashboard_metrics()
```

---

## Usuario contextual

Usa:

```python
get_contextual_dashboard_metrics()
```

:contentReference[oaicite:9]{index=9}

---

# Métricas Actuales

## Usuarios

```python
total_users
active_users
inactive_users
```

---

## Roles

```python
total_roles
```

---

## Identidades

```python
total_identities
local_identities
external_identities
```

---

## Proyectos

```python
total_projects
active_projects
finished_projects
```

---

## Tareas

```python
total_tasks
pending_tasks
progress_tasks
completed_tasks
completion_rate
```

---

## Actividades

```python
total_activities
total_hours
```

:contentReference[oaicite:10]{index=10}

---

# Queries Agregadas

El dashboard utiliza:

```python
func.count()
func.sum()
case()
coalesce()
```

para minimizar queries innecesarias.

:contentReference[oaicite:11]{index=11}

---

# Dashboard Feed

## Objetivo

Mostrar actividad funcional reciente.

NO es auditoría técnica pura.

---

## Fuente

```python
ProjectActivityFeed
```

:contentReference[oaicite:12]{index=12}

---

## Render SSR

```jinja2
{% for item in recent_feed %}
```

:contentReference[oaicite:13]{index=13}

---

## Actualización Realtime

```javascript
prependDashboardFeedEvent()
```

:contentReference[oaicite:14]{index=14}

---

# Dashboard Realtime

## Conexión

```javascript
new WebSocket("/ws/dashboard")
```

:contentReference[oaicite:15]{index=15}

---

# Eventos Realtime

## Evento principal

```text
dashboard_feed_event
```

:contentReference[oaicite:16]{index=16}

---

## Payload

```json
{
  "type": "dashboard_feed_event",
  "activity": {...}
}
```

---

# Incremental Rendering

## Filosofía

NO se rerenderiza toda la página.

Solo:

- nuevos elementos feed,
- nuevas notificaciones,
- nuevos eventos visuales.

---

# prependDashboardFeedEvent()

Responsable de:

- insertar eventos nuevos,
- evitar duplicados,
- animaciones,
- limitar feed.

:contentReference[oaicite:17]{index=17}

---

# Deduplicación

Evita duplicados mediante:

```javascript
data-feed-id
```

:contentReference[oaicite:18]{index=18}

---

# Feed Limiting

El feed mantiene:

```text
máximo 8 elementos
```

:contentReference[oaicite:19]{index=19}

---

# Animaciones

Los nuevos elementos usan:

```css
activity-item-new
```

para:

- fade-in,
- highlight,
- feedback visual.

:contentReference[oaicite:20]{index=20}

---

# Toast Integration

Cada evento realtime genera:

```javascript
showToast()
```

:contentReference[oaicite:21]{index=21}

---

# Objetivo UX

Crear sensación de:

```text
dashboard vivo
```

---

# Dashboard Charts

## Tecnología

```text
Chart.js
```

:contentReference[oaicite:22]{index=22}

---

# Charts actuales

## Users Chart

```text
doughnut
```

Estado usuarios.

---

## Tasks Chart

```text
doughnut
```

Estado tareas.

:contentReference[oaicite:23]{index=23}

---

# Arquitectura Visual

## Hero Section

Dashboard incluye:

- saludo contextual,
- branding Aula Robótica,
- fecha actual,
- identidad visual.

:contentReference[oaicite:24]{index=24}

---

# KPI Cards

Cards reutilizables para:

- usuarios,
- proyectos,
- tareas,
- productividad,
- actividades,
- horas.

:contentReference[oaicite:25]{index=25}

---

# Renderizado Contextual

Uso intensivo de:

```jinja2
can()
```

:contentReference[oaicite:26]{index=26}

---

# Ejemplo

```jinja2
{% if can("read", "projects") %}
```

---

# Seguridad

## Backend-first

La seguridad real se valida mediante:

```python
require_permission_web()
```

:contentReference[oaicite:27]{index=27}

---

# Realtime Security

El WebSocket dashboard valida:

- JWT,
- usuario autenticado.



---

# Arquitectura UX

## Principios

### 1. Información viva

El dashboard cambia dinámicamente.

---

### 2. Feedback inmediato

Realtime + toast system.

---

### 3. Baja fricción

Sin refresh manual.

---

### 4. Contextualidad

Cada usuario ve:

- sus métricas,
- sus proyectos,
- sus actividades.

---

# Integración con Otros Sistemas

## Audit System

Muestra auditoría reciente.

:contentReference[oaicite:29]{index=29}

---

## Activity Feed

Integra feed funcional.



---

## Toast System

Integrado mediante:

```javascript
showToast()
```

:contentReference[oaicite:31]{index=31}

---

## WebSocket System

Usa:

```text
/ws/dashboard
```

:contentReference[oaicite:32]{index=32}

---

# Estado Actual

## Completamente implementado

Incluye:

- dashboard SSR,
- métricas agregadas,
- dashboard contextual,
- realtime feed,
- charts,
- activity stream,
- toast integration,
- reconnect automático,
- deduplicación feed.

---

# Limitaciones Actuales

## 1. Charts no realtime

Actualmente:

```text
charts SSR estáticos
```

No reciben updates live.

---

## 2. Sin cache distribuida

Las métricas se recalculan.

---

## 3. Feed parcial

El realtime actual se centra en:

- activity feed,
- eventos recientes.

---

## 4. No existe polling fallback

Si WS falla:

```text
no hay sincronización secundaria
```

---

# Evolución Futura

## Corto plazo

- realtime KPI cards,
- realtime charts,
- métricas live,
- indicadores visuales conexión.

---

## Medio plazo

- cache dashboard,
- Redis Pub/Sub,
- dashboards por rol,
- widgets configurables.

---

## Largo plazo

- observabilidad realtime,
- métricas sistema,
- monitoring operativo,
- analytics avanzados,
- dashboards competición,
- dashboards robótica live.

---

# Visión Estratégica

El dashboard evolucionará hacia:

```text
Robotics Operations Center
```

capaz de gestionar:

- proyectos,
- equipos,
- actividad,
- competiciones,
- telemetría,
- operación académica realtime.

---

# Relación con otros documentos

Relacionado con:

- `21_WEBSOCKET_SYSTEM.md`
- `23_REALTIME_NOTIFICATIONS.md`
- `15_AUDIT_SYSTEM.md`
- `18_TOAST_SYSTEM.md`
- `07_FRONTEND_ARCHITECTURE.md`
- `08_UI_ARCHITECTURE.md`
- `20_JS_ARCHITECTURE.md`

---

# Conclusión

El dashboard actual ya supera ampliamente el nivel típico de un panel CRUD académico.

La plataforma ya dispone de:

- SSR contextual,
- realtime feed,
- activity stream live,
- charts modernos,
- dashboard contextual,
- integración audit,
- UX enterprise,
- broadcasting realtime,
- toast notifications,
- arquitectura modular.

La siguiente evolución natural será:

```text
Live operational dashboards fully realtime
```