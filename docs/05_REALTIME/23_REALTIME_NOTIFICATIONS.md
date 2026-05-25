# 23_REALTIME_NOTIFICATIONS.md

# Realtime Notifications System

## Objetivo

Este documento describe la arquitectura realtime del sistema de notificaciones de Aula Robótica Platform.

El sistema permite:

- notificaciones instantáneas,
- feedback en tiempo real,
- comunicación contextual,
- UX moderna tipo enterprise,
- sincronización multiusuario.

La arquitectura combina:

- persistencia SQL,
- WebSockets,
- SSR,
- render incremental frontend,
- toast notifications.

---

# Filosofía del Sistema

Las notificaciones NO son simples mensajes flash temporales.

El objetivo es construir:

```text
Realtime User Communication Layer
```

capaz de:

- informar eventos relevantes,
- mantener sincronización contextual,
- mejorar colaboración,
- reducir fricción operativa.

---

# Objetivos Arquitectónicos

## 1. Realtime real

El usuario debe recibir eventos:

```text
sin refresh
```

---

## 2. Persistencia completa

Las notificaciones se almacenan.

No son efímeras.

---

## 3. UX enterprise

Inspiración:

- GitHub Notifications,
- Jira,
- Slack,
- Linear,
- Discord admin systems.

---

## 4. Bajo acoplamiento

Separar:

- persistencia,
- realtime,
- rendering,
- UI,
- broadcasting.

---

# Arquitectura General

```text
Backend Event
    ↓
Notification Service
    ↓
Persistencia SQL
    ↓
emit_user_event()
    ↓
WebSocket user room
    ↓
notifications.js
    ↓
Toast + Dropdown Update
```

---

# Componentes Principales

## Backend

### Notification Model

Archivo:

```text
app/modules/notifications/notification_model.py
```

Define persistencia SQL.

:contentReference[oaicite:0]{index=0}

---

### Notification Service

Archivo:

```text
app/modules/notifications/notification_service.py
```

Responsable de:

- crear notificaciones,
- emitir eventos realtime,
- lectura,
- contadores,
- sincronización.

:contentReference[oaicite:1]{index=1}

---

### Notifications Router

Archivo:

```text
app/modules/notifications/notifications_web.py
```

Responsable de:

- página de notificaciones,
- marcar leídas,
- navegación,
- endpoints SSR.

:contentReference[oaicite:2]{index=2}

---

## Frontend

### notifications.js

Cliente realtime.

Archivo:

```text
static/js/notifications/notifications.js
```

:contentReference[oaicite:3]{index=3}

---

### notifications_list.html

Vista SSR de notificaciones.

Archivo:

```text
templates/notifications/notifications_list.html
```

:contentReference[oaicite:4]{index=4}

---

# Notification Model

## Tabla

```text
notifications
```

:contentReference[oaicite:5]{index=5}

---

# Campos Principales

## Identidad

```python
id_notification
user_id
```

---

## Contenido

```python
type
title
message
```

---

## Contexto

```python
entity_type
entity_id
url
```

---

## Estado

```python
is_read
created_at
read_at
```

:contentReference[oaicite:6]{index=6}

---

# Filosofía de Persistencia

Las notificaciones:

- sobreviven refresh,
- sobreviven reconnect,
- permiten historial,
- permiten navegación contextual.

---

# Arquitectura Realtime

## Flujo Principal

```text
Evento backend
    ↓
create_notification()
    ↓
Persistencia DB
    ↓
emit_user_event()
    ↓
WebSocket usuario
    ↓
Frontend update
```

---

# create_notification()

Core principal:

```python
create_notification()
```

:contentReference[oaicite:7]{index=7}

---

# Responsabilidades

## 1. Persistencia

Inserta notificación SQL.

---

## 2. Estado inicial

```python
is_read=False
```

---

## 3. Timestamp

```python
created_at=datetime.now(UTC)
```

---

## 4. Emisión realtime

```python
emit_user_event()
```

:contentReference[oaicite:8]{index=8}

---

# Payload Realtime

## Formato

```json
{
  "type": "notification",
  "notification": {
    "id_notification": 1,
    "title": "...",
    "message": "...",
    "url": "...",
    "created_at": "..."
  }
}
```

:contentReference[oaicite:9]{index=9}

---

# WebSocket Notifications

## Endpoint

```text
/ws/notifications
```

:contentReference[oaicite:10]{index=10}

---

# Arquitectura de Usuario

Cada usuario posee:

```text
canal realtime privado
```

---

# Objetivo

Aislamiento total de eventos.

---

# notifications.js

## Inicialización

```javascript
connectNotificationsWebSocket()
```

:contentReference[oaicite:11]{index=11}

---

# Conexión WS

```javascript
new WebSocket("/ws/notifications")
```

:contentReference[oaicite:12]{index=12}

---

# Reconnect automático

## Estrategia

```javascript
setTimeout(connectNotificationsWebSocket, 3000)
```

:contentReference[oaicite:13]{index=13}

---

# Keepalive

## Implementación

```javascript
socket.send("ping")
```

cada:

```text
30 segundos
```

:contentReference[oaicite:14]{index=14}

---

# Objetivo

Evitar:

- idle disconnects,
- timeouts proxy,
- cierres silenciosos.

---

# Recepción de Eventos

## Handler principal

```javascript
socket.onmessage
```

:contentReference[oaicite:15]{index=15}

---

# Evento soportado

```text
notification
```

---

# Comportamiento Frontend

Al recibir evento:

## 1. prependNotification()

Actualiza dropdown.

---

## 2. incrementNotificationCount()

Actualiza badge.

---

## 3. showToast()

Feedback inmediato.

:contentReference[oaicite:16]{index=16}

---

# Dropdown Realtime

## Objetivo

Mostrar nuevas notificaciones instantáneamente.

---

# prependNotification()

Responsable de:

- insertar item,
- eliminar empty state,
- actualizar DOM,
- marcar unread.

:contentReference[oaicite:17]{index=17}

---

# Rendering Incremental

La UI:

```text
NO rerenderiza toda la página
```

Solo inserta:

```text
nuevo elemento
```

---

# Notification Counter

## Badge dinámico

```javascript
incrementNotificationCount()
```

:contentReference[oaicite:18]{index=18}

---

# Comportamiento

- incremento automático,
- render badge,
- sincronización visual.

---

# Toast Integration

Cada notificación genera:

```javascript
showToast()
```

:contentReference[oaicite:19]{index=19}

---

# Objetivo UX

El usuario recibe:

```text
feedback inmediato contextual
```

---

# Notifications Page

## Vista completa

Archivo:

```text
notifications_list.html
```

:contentReference[oaicite:20]{index=20}

---

# Funcionalidades

## Historial

Listado persistente.

---

## Estado visual

- leídas,
- no leídas.

---

## Navegación contextual

Links automáticos.

---

## Mark all as read

Operación masiva.

:contentReference[oaicite:21]{index=21}

---

# Render SSR

La página utiliza:

```text
SSR + Jinja2
```

---

# Notification Types

## Tipos actuales

```text
TASK_ASSIGNED
TASK_STATUS_CHANGED
PROJECT_MEMBER_ADDED
PROJECT_UPDATED
```

:contentReference[oaicite:22]{index=22}

---

# Arquitectura Extensible

El sistema soporta:

```text
tipos arbitrarios
```

---

# Navegación Contextual

## open_notification()

Endpoint:

```python
/notifications/{id}/open
```

:contentReference[oaicite:23]{index=23}

---

# Comportamiento

## 1. Marca leída

```python
mark_notification_as_read()
```

---

## 2. Redirige

```python
notification.url
```

:contentReference[oaicite:24]{index=24}

---

# Filosofía UX

La notificación funciona como:

```text
actionable event
```

---

# Lectura de Notificaciones

## Individual

```python
mark_notification_as_read()
```

---

## Global

```python
mark_all_notifications_as_read()
```



---

# Estado Visual

## Unread

```css
notification-unread
notification-page-unread
```



---

# Indicadores UX

## Dot indicator

```text
notification-page-dot
```

---

## Badge "Nueva"

Render condicional SSR.

:contentReference[oaicite:27]{index=27}

---

# Seguridad

## Aislamiento usuario

Cada notificación pertenece a:

```python
user_id
```

:contentReference[oaicite:28]{index=28}

---

# Validación Backend

Todas las operaciones validan:

```python
current_user.id_usuario
```

:contentReference[oaicite:29]{index=29}

---

# Arquitectura Realtime Segura

El backend emite eventos:

```text
solo al usuario destinatario
```

---

# Integración con Context Injection

El sistema se integra globalmente mediante:

```python
recent_notifications
unread_notifications_count
```

---

# Resultado

El navbar dispone siempre de:

- dropdown actualizado,
- contador vivo,
- acceso inmediato.

---

# Integración con Otros Sistemas

## Toast System

Integración directa.

:contentReference[oaicite:30]{index=30}

---

## WebSocket System

Usa infraestructura común.



---

## Audit System

Eventos críticos pueden generar:

- audit log,
- notification.

---

## Activity Feed

Sistemas separados pero complementarios.

---

# Diferencia conceptual

## Notifications

Orientadas a:

```text
usuario concreto
```

---

## Activity Feed

Orientado a:

```text
actividad colaborativa global
```

---

# Estado Actual

## Implementado

Incluye:

- persistencia SQL,
- realtime WS,
- reconnect,
- keepalive,
- toast integration,
- dropdown realtime,
- unread counters,
- mark as read,
- navegación contextual,
- notifications page,
- rendering SSR.

---

# Limitaciones Actuales

## 1. No existe batching

Cada evento se emite individualmente.

---

## 2. Sin prioridades

No hay:

- critical,
- warning,
- info,
- success.

---

## 3. Sin agrupación

No se agrupan eventos similares.

---

## 4. Sin preferencias usuario

No existe configuración:

- muting,
- canales,
- frecuencia.

---

# Evolución Futura

## Corto plazo

- tipos visuales,
- iconografía dinámica,
- sound notifications,
- unread sync realtime.

---

## Medio plazo

- agrupación inteligente,
- prioridades,
- filtros,
- archivado.

---

## Largo plazo

- push notifications,
- email integration,
- mobile sync,
- distributed realtime,
- Redis Pub/Sub,
- event bus.

---

# Visión Estratégica

El sistema evolucionará hacia:

```text
Unified Event Communication Platform
```

para:

- operación académica,
- colaboración,
- coordinación proyectos,
- competición robótica,
- workflows realtime.

---

# Relación con otros documentos

Relacionado con:

- `21_WEBSOCKET_SYSTEM.md`
- `22_REALTIME_DASHBOARD.md`
- `18_TOAST_SYSTEM.md`
- `15_AUDIT_SYSTEM.md`
- `20_JS_ARCHITECTURE.md`
- `08_UI_ARCHITECTURE.md`

---

# Conclusión

El sistema de notificaciones actual ya supera ampliamente el comportamiento típico de un CRUD académico.

La plataforma dispone actualmente de:

- realtime user events,
- persistencia completa,
- WebSockets privados,
- toast integration,
- dropdown live updates,
- reconnect automático,
- navegación contextual,
- unread counters,
- UX enterprise,
- arquitectura desacoplada.

La siguiente evolución natural será:

```text
full event-driven realtime platform
```