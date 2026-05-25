# 33_DASHBOARD_MODULE.md

# Módulo Dashboard

## Objetivo

El Dashboard actúa como centro operativo y visual de Aula Robótica Platform.

Actualmente el dashboard combina:

- métricas globales,
- métricas contextuales,
- KPIs,
- activity feed realtime,
- auditoría reciente,
- gráficos dinámicos,
- navegación contextual,
- realtime updates.

No es únicamente una landing administrativa.

El objetivo arquitectónico es evolucionar hacia:

```text
Realtime Enterprise Admin Console
```

---

# Filosofía del módulo

El dashboard representa el estado vivo de la plataforma.

Debe permitir:

- observar actividad,
- detectar cambios,
- visualizar productividad,
- supervisar operaciones,
- navegar rápidamente,
- recibir feedback realtime.

---

# Arquitectura General

```text
Dashboard Router
        ↓
Dashboard Service
        ↓
Metrics Aggregation
        ↓
Activity Feed
        ↓
Audit Integration
        ↓
Realtime WebSockets
        ↓
SSR Rendering
        ↓
Charts + Live Feed
```

---

# Componentes Principales

## Backend

```text
app/modules/dashboard/
├── dashboard_service.py
└── dashboard_web.py
```

---

## Frontend SSR

```text
templates/dashboard/
└── dashboard.html
```

:contentReference[oaicite:0]{index=0}

---

## Realtime JS

```text
static/js/dashboard/dashboard.js
```

:contentReference[oaicite:1]{index=1}

---

# Arquitectura del Dashboard

# Dashboard híbrido

El dashboard combina:

## SSR

Render inicial rápido y seguro.

## Realtime

Actualización parcial vía WebSockets.

---

# Beneficios

- UX fluida,
- bajo consumo,
- SSR enterprise,
- realtime progresivo.

---

# Dashboard Router

Archivo:

```text
dashboard_web.py
```

:contentReference[oaicite:2]{index=2}

---

# Ruta Principal

```text
GET /dashboard
```

---

# Seguridad

La ruta requiere:

```python
require_permission_web(
    Resources.DASHBOARD,
    Actions.READ
)
```

:contentReference[oaicite:3]{index=3}

---

# Context Injection

El router inyecta:

```python
request.scope["db"]
```

para helpers globales de templates. :contentReference[oaicite:4]{index=4}

---

# Pipeline Principal

```text
GET /dashboard
    ↓
require_permission_web()
    ↓
get_dashboard_metrics()
    ↓
detectar roles
    ↓
resolver admin/contextual
    ↓
render SSR
```

:contentReference[oaicite:5]{index=5}

---

# Dashboard Service

Archivo:

```text
dashboard_service.py
```

:contentReference[oaicite:6]{index=6}

---

# Responsabilidad Principal

Construir métricas agregadas desacopladas.

---

# Filosofía

El router NO contiene lógica de negocio compleja.

Toda agregación vive en:

```text
dashboard_service.py
```

---

# Arquitectura de Métricas

## Admin Dashboard

Muestra:

- usuarios,
- roles,
- identidades,
- proyectos,
- tareas,
- actividades,
- auditoría global,
- feed global.

---

## Dashboard Contextual

Usuarios no admin reciben:

- solo proyectos accesibles,
- solo tareas visibles,
- solo actividades visibles,
- feed contextual,
- sin auditoría global.

:contentReference[oaicite:7]{index=7}

---

# Resolución de Roles

## Función

```python
get_user_role_names()
```

:contentReference[oaicite:8]{index=8}

---

# Roles soportados

Actualmente:

```text
admin
profesor
estudiante
uah_user
```

---

# Métricas Principales

# Usuarios

```text
total_users
active_users
inactive_users
```

:contentReference[oaicite:9]{index=9}

---

# Roles

```text
total_roles
```

---

# Identidades

```text
total_identities
local_identities
external_identities
```

---

# Proyectos

```text
total_projects
active_projects
finished_projects
```

---

# Tareas

```text
total_tasks
pending_tasks
progress_tasks
completed_tasks
completion_rate
```

---

# Actividades

```text
total_activities
total_hours
```

---

# Métricas Derivadas

# Completion Rate

Calculado mediante:

```python
calculate_completion_rate()
```

:contentReference[oaicite:10]{index=10}

---

# Fórmula

:contentReference[oaicite:11]{index=11}

---

# Empty Dashboard Strategy

## Función

```python
empty_dashboard_metrics()
```

:contentReference[oaicite:12]{index=12}

---

# Objetivo

Evitar:

- errores template,
- null handling complejo,
- rendering inconsistente.

---

# Dashboard Contextual

## Filosofía

El dashboard se adapta automáticamente al usuario.

---

# Admin

Vista global del sistema.

---

# Estudiante

Vista personal/contextual.

---

# Profesor / Coordinador

Vista operacional de proyectos accesibles.

---

# Filtrado Contextual

## Projects

```python
ProjectMember.project_id
```

:contentReference[oaicite:13]{index=13}

---

# Tasks

## Estudiante

Solo tareas asignadas:

```python
Task.assigned_to == user_id
```

:contentReference[oaicite:14]{index=14}

---

# Activities

## Estudiante

Solo actividades propias.

:contentReference[oaicite:15]{index=15}

---

# Activity Feed

# Feed integrado

El dashboard consume:

```python
ProjectActivityFeed
```

:contentReference[oaicite:16]{index=16}

---

# Feed Admin

Feed global.

---

# Feed Contextual

Feed limitado a proyectos accesibles.

---

# Auditoría Integrada

## Solo admin

El dashboard muestra:

```python
AuditLog
```



---

# Filosofía

Separar:

## Feed funcional

```text
actividad operativa
```

de:

## Auditoría técnica

```text
seguridad y trazabilidad
```

---

# Frontend SSR

Archivo:

```text
dashboard.html
```

:contentReference[oaicite:18]{index=18}

---

# Arquitectura UI

El dashboard usa:

- hero section,
- KPI cards,
- charts,
- audit table,
- realtime feed,
- cards reutilizables.

---

# Hero Section

Incluye:

- bienvenida contextual,
- rol,
- fecha,
- branding.

:contentReference[oaicite:19]{index=19}

---

# KPI Cards

## Métricas visuales

Cada KPI:

- enlace contextual,
- iconografía,
- contador,
- metadata secundaria.

---

# Ejemplos

## Usuarios

```text
Usuarios activos
```

---

## Tareas

```text
Completadas
```

---

## Productividad

```text
completion_rate
```

:contentReference[oaicite:20]{index=20}

---

# Contextual Rendering

El template usa:

```jinja2
is_admin
can(...)
```

para renderizar componentes condicionalmente. :contentReference[oaicite:21]{index=21}

---

# Charts

# Chart.js Integration

El dashboard usa:

```html
Chart.js
```

:contentReference[oaicite:22]{index=22}

---

# Users Chart

## Admin only

Gráfico doughnut:

```text
Activos / Inactivos
```

---

# Tasks Chart

Gráfico doughnut:

```text
Por hacer
En progreso
Completadas
```

---

# Filosofía Visual

Gráficos simples:

- rápidos,
- claros,
- dashboard-oriented.

---

# Activity Feed Realtime

# Feed Live

La card:

```text
Actividad reciente
```

se actualiza en realtime. :contentReference[oaicite:23]{index=23}

---

# Feed SSR inicial

El render inicial carga:

```python
recent_feed
```



---

# Feed Realtime JS

Archivo:

```text
dashboard.js
```

:contentReference[oaicite:25]{index=25}

---

# WebSocket Dashboard

Conexión:

```text
/ws/dashboard
```

:contentReference[oaicite:26]{index=26}

---

# Eventos soportados

## dashboard_feed_event

Actualiza:

- activity feed,
- toast realtime.

---

# Pipeline Realtime

```text
Backend Event
    ↓
WebSocket Broadcast
    ↓
dashboard.js
    ↓
prependDashboardFeedEvent()
    ↓
showToast()
```

---

# prependDashboardFeedEvent()

Responsable de:

- insertar item,
- evitar duplicados,
- eliminar empty state,
- limitar feed,
- animaciones.

:contentReference[oaicite:27]{index=27}

---

# Anti-duplicados

El sistema usa:

```javascript
data-feed-id
```

para evitar render doble. :contentReference[oaicite:28]{index=28}

---

# Feed Size Control

## limitDashboardFeedItems()

Limita:

```text
máximo 8 eventos
```

:contentReference[oaicite:29]{index=29}

---

# Toast Integration

Los eventos muestran:

```javascript
showToast()
```

:contentReference[oaicite:30]{index=30}

---

# stripHtml()

El JS limpia HTML antes de mostrar toast. :contentReference[oaicite:31]{index=31}

---

# Reconnect automático

Si cae conexión:

```javascript
setTimeout(connectDashboardWebSocket, 2500)
```

:contentReference[oaicite:32]{index=32}

---

# Integración con Otros Módulos

# Tasks

Alimenta:

- métricas,
- charts,
- completion rate,
- activity feed.

---

# Activities

Alimenta:

- total hours,
- activity count,
- realtime feed.

---

# Notifications

Los eventos dashboard generan toasts integrados.

---

# Audit

Admin dashboard consume:

```text
AuditLog
```

---

# Projects

Dashboard contextual depende de:

```text
ProjectMember
```

---

# Seguridad

# Backend-first

Toda visibilidad real se resuelve en backend.

---

# Contextual Queries

El dashboard filtra:

- proyectos,
- tareas,
- actividades.

:contentReference[oaicite:33]{index=33}

---

# Frontend Authorization

El template SSR usa:

```jinja2
can()
```

para ocultar módulos no autorizados. :contentReference[oaicite:34]{index=34}

---

# Estado Actual

## Implementado

- dashboard SSR,
- dashboard contextual,
- KPIs,
- charts,
- realtime feed,
- WebSockets,
- reconnect,
- toast integration,
- audit integration,
- feed integration,
- responsive cards,
- contextual rendering.

---

# Limitaciones actuales

## 1. dashboard.js monolítico

Actualmente mezcla:

- websocket,
- feed rendering,
- toasts,
- formatting.

---

## 2. Sin polling fallback

Solo WebSocket.

---

## 3. Sin cache de métricas

Cada carga recalcula queries.

---

## 4. Sin métricas históricas

No existe persistencia analytics.

---

## 5. Sin widgets configurables

El layout es fijo.

---

## 6. Sin observabilidad

No hay métricas técnicas:

- latency,
- errors,
- websocket health.

---

# Mejoras Futuras

## Corto plazo

- modularizar dashboard.js,
- loaders,
- skeletons,
- indicators realtime.

---

## Medio plazo

- métricas históricas,
- widgets configurables,
- analytics,
- charts avanzados,
- filtros temporales.

---

## Largo plazo

- observabilidad,
- dashboards operativos,
- monitoring,
- multi-dashboard,
- realtime analytics engine,
- BI integration.

---

# Valor Arquitectónico

El Dashboard es uno de los módulos más importantes porque conecta:

```text
Realtime
+
Métricas
+
Activity Feed
+
Auditoría
+
Navegación
+
Operación
```

---

# Conclusión

El Dashboard actual ya supera ampliamente el concepto de panel administrativo académico.

Actualmente representa:

```text
Operational Realtime Console
```

con:

- métricas contextuales,
- activity feed vivo,
- charts,
- realtime updates,
- SSR enterprise,
- navegación contextual,
- integración completa con el ecosistema de módulos.