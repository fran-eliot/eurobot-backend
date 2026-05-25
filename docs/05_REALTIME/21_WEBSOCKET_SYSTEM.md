# 21_WEBSOCKET_SYSTEM.md

# Sistema WebSocket

## Objetivo

Este documento describe la arquitectura realtime basada en WebSockets de Aula Robótica Platform.

El sistema permite:

- colaboración realtime,
- actualización viva de dashboards,
- sincronización Kanban,
- presencia de usuarios online,
- activity feeds live,
- auditoría realtime,
- notificaciones instantáneas.

La arquitectura está diseñada como una capa desacoplada sobre SSR/Jinja2.

---

# Filosofía Arquitectónica

La plataforma sigue una arquitectura:

```text
SSR-first + Realtime Enhancement
```

Esto significa:

- FastAPI renderiza HTML SSR,
- Jinja2 genera vistas iniciales,
- WebSockets sincronizan eventos posteriores,
- no existe polling tradicional,
- el frontend permanece sincronizado en tiempo real.

---

# Objetivos del Sistema

## UX moderna

Experiencia similar a:

- admin consoles enterprise,
- herramientas colaborativas,
- dashboards operativos realtime.

---

## Sincronización multiusuario

Mantener vistas sincronizadas entre:

- profesores,
- administradores,
- coordinadores,
- estudiantes.

---

## Desacoplamiento

Separar:

- lógica CRUD,
- render SSR,
- realtime,
- notificaciones.

---

## Escalabilidad

Preparar arquitectura para:

- múltiples salas,
- múltiples usuarios,
- realtime distribuido,
- Redis Pub/Sub futuro.

---

# Arquitectura General

```text
Browser
   ↓
WebSocket Connection
   ↓
FastAPI WebSocket Router
   ↓
ConnectionManager
   ↓
Rooms / User Channels / Dashboard Channels
   ↓
Broadcast System
```

---

# Estructura Actual

```text
app/core/websockets/
├── manager.py
├── router.py
├── utils.py
└── ws_auth.py
```

---

# Componentes Principales

## 1. ConnectionManager

Archivo:

```text
app/core/websockets/manager.py
```

Responsable de:

- gestionar conexiones activas,
- gestionar rooms,
- gestionar usuarios online,
- broadcasting,
- conexiones dashboard,
- conexiones individuales.

:contentReference[oaicite:0]{index=0}

---

## 2. Router WebSocket

Archivo:

```text
app/core/websockets/router.py
```

Define endpoints realtime:

```text
/ws/projects/{project_id}
/ws/dashboard
/ws/notifications
```

:contentReference[oaicite:1]{index=1}

---

## 3. Utilidades de emisión

Archivo:

```text
app/core/websockets/utils.py
```

Define helpers desacoplados:

```python
emit_project_event()
emit_dashboard_event()
emit_user_event()
```

:contentReference[oaicite:2]{index=2}

---

## 4. Autenticación WS

Archivo:

```text
app/core/websockets/ws_auth.py
```

Valida JWT desde cookies HTTPOnly.

:contentReference[oaicite:3]{index=3}

---

# Arquitectura de Canales

Actualmente existen tres tipos principales de canal.

---

# 1. Project Rooms

Endpoint:

```text
/ws/projects/{project_id}
```

Responsable de:

- Kanban realtime,
- usuarios online,
- auditoría realtime,
- activity feed realtime.

---

## Concepto de Room

Cada proyecto funciona como una sala independiente:

```python
self.rooms[project_id]
```

:contentReference[oaicite:4]{index=4}

---

## Aislamiento

Los eventos de un proyecto NO se envían a otros proyectos.

Esto reduce:

- ruido,
- consumo,
- fugas de información,
- acoplamiento.

---

## Validación de acceso

Antes de aceptar conexión:

```python
user_in_project(user, project)
```

:contentReference[oaicite:5]{index=5}

---

## Eventos actuales

```text
users_online
task_updated
audit
feed_event
```

:contentReference[oaicite:6]{index=6}

---

# 2. Dashboard Channel

Endpoint:

```text
/ws/dashboard
```

Responsable de:

- dashboard realtime,
- activity feed global,
- métricas dinámicas.

---

## Características

Canal compartido global.

Conexiones almacenadas en:

```python
self.dashboard_connections
```

:contentReference[oaicite:7]{index=7}

---

## Eventos actuales

```text
dashboard_feed_event
```

:contentReference[oaicite:8]{index=8}

---

# 3. User Notification Channels

Endpoint:

```text
/ws/notifications
```

Responsable de:

- notificaciones personales,
- dropdown navbar,
- contador unread,
- toast notifications.

---

## Arquitectura

Cada usuario tiene su propio canal:

```python
self.user_connections[user_id]
```

:contentReference[oaicite:9]{index=9}

---

## Eventos actuales

```text
notification
```

:contentReference[oaicite:10]{index=10}

---

# ConnectionManager

## Estructuras internas

### Rooms

```python
self.rooms = {}
```

Mapa:

```text
project_id -> websocket connections
```

---

### Usuarios online

```python
self.users = {}
```

Mapa:

```text
project_id -> online users
```

---

### Dashboard connections

```python
self.dashboard_connections = []
```

---

### User connections

```python
self.user_connections = {}
```

Mapa:

```text
user_id -> websocket connections
```

:contentReference[oaicite:11]{index=11}

---

# Flujo de Conexión

## 1. Cliente abre WebSocket

Ejemplo:

```javascript
new WebSocket("/ws/projects/1")
```

:contentReference[oaicite:12]{index=12}

---

## 2. FastAPI recibe conexión

Router WS:

```python
@router.websocket("/projects/{project_id}")
```

:contentReference[oaicite:13]{index=13}

---

## 3. Validación JWT

```python
get_current_user_ws()
```

Lee:

```python
websocket.cookies.get("access_token")
```

:contentReference[oaicite:14]{index=14}

---

## 4. Validación de acceso contextual

```python
user_in_project(user, project)
```

---

## 5. Registro de conexión

```python
manager.connect()
```

:contentReference[oaicite:15]{index=15}

---

## 6. Broadcasting

Los eventos se emiten automáticamente a la room correspondiente.

---

# Broadcasting Architecture

## Project Broadcast

```python
broadcast_to_project(project_id, payload)
```

:contentReference[oaicite:16]{index=16}

---

## Dashboard Broadcast

```python
broadcast_dashboard(payload)
```

:contentReference[oaicite:17]{index=17}

---

## User Broadcast

```python
broadcast_to_user(user_id, payload)
```

:contentReference[oaicite:18]{index=18}

---

# Emisión Desacoplada

## Filosofía

Los servicios NO deberían conocer detalles internos del manager.

Se utilizan helpers:

```python
emit_project_event()
emit_dashboard_event()
emit_user_event()
```

:contentReference[oaicite:19]{index=19}

---

# Arquitectura Async

## create_task()

La emisión se realiza sin bloquear request principal:

```python
loop.create_task(...)
```

:contentReference[oaicite:20]{index=20}

---

## Beneficios

- menor latencia,
- mejor UX,
- desacoplamiento realtime,
- requests más rápidas.

---

# Gestión de Usuarios Online

## Arquitectura

Cuando un usuario entra:

```python
self.users[project_id][user.id_usuario]
```

:contentReference[oaicite:21]{index=21}

---

## Broadcast automático

Cada conexión/desconexión ejecuta:

```python
broadcast_users(project_id)
```

:contentReference[oaicite:22]{index=22}

---

## Evento emitido

```json
{
  "type": "users_online",
  "users": [...]
}
```

---

# Seguridad

## JWT Cookies

Los WebSockets usan:

```text
HTTPOnly JWT cookies
```

No usan tokens en querystring.

---

## Validación SSR integrada

La autenticación reutiliza:

```python
validate_access_token()
```

:contentReference[oaicite:23]{index=23}

---

## Cierre seguro

Conexiones inválidas:

```python
await websocket.close(code=1008)
```

:contentReference[oaicite:24]{index=24}

---

# Gestión de Desconexiones

## WebSocketDisconnect

Cada endpoint captura:

```python
except WebSocketDisconnect:
```

:contentReference[oaicite:25]{index=25}

---

## Limpieza automática

Se eliminan:

- sockets muertos,
- usuarios desconectados,
- rooms vacías.

:contentReference[oaicite:26]{index=26}

---

# Frontend Realtime

## Dashboard

Archivo:

```text
static/js/dashboard/dashboard.js
```

Características:

- reconexión automática,
- feed live,
- toasts realtime,
- deduplicación.

:contentReference[oaicite:27]{index=27}

---

## Notifications

Archivo:

```text
static/js/core/notifications.js
```

Características:

- keepalive,
- reconexión,
- dropdown dinámico,
- contador unread,
- toast realtime.

:contentReference[oaicite:28]{index=28}

---

## Project Detail

Archivo:

```text
static/js/projects/project_detail.js
```

Características:

- Kanban realtime,
- auditoría realtime,
- feed realtime,
- online users,
- optimistic UI.

:contentReference[oaicite:29]{index=29}

---

# Keepalive

Notifications WS implementa:

```javascript
socket.send("ping")
```

cada:

```text
30 segundos
```

:contentReference[oaicite:30]{index=30}

---

# Reconnection Strategy

Todos los canales implementan:

```javascript
setTimeout(connect..., X)
```

para reconexión automática.



---

# Arquitectura de Eventos

## Estructura general

```json
{
  "type": "...",
  "payload": ...
}
```

---

## Ejemplos

### Task update

```json
{
  "type": "task_updated",
  "task_id": 12,
  "status": "doing"
}
```

---

### Notification

```json
{
  "type": "notification",
  "notification": {...}
}
```

---

### Feed event

```json
{
  "type": "feed_event",
  "activity": {...}
}
```

---

# Beneficios Arquitectónicos

## 1. UX moderna

Interfaz viva y colaborativa.

---

## 2. SSR compatible

No requiere SPA.

---

## 3. Bajo acoplamiento

Realtime desacoplado del CRUD.

---

## 4. Escalabilidad conceptual

Preparado para:

- Redis,
- Pub/Sub,
- workers,
- horizontal scaling.

---

## 5. Aislamiento contextual

Rooms por proyecto.

---

## 6. Enterprise feel

La plataforma se comporta como:

```text
Enterprise Realtime Admin Platform
```

---

# Limitaciones Actuales

## 1. Estado en memoria

Las conexiones viven en memoria del proceso.

Problema:

```text
multi-worker deployment
```

---

## 2. No hay Redis Pub/Sub

Actualmente:

```text
single-process realtime
```

---

## 3. Reconexión básica

No existe:

- exponential backoff,
- jitter,
- estado visual conexión.

---

## 4. No existe heartbeat server-side

Solo cliente → servidor.

---

## 5. Sin message persistence

Los eventos realtime no se almacenan.

---

# Roadmap Futuro

## Corto plazo

- extraer websocket.js reusable,
- heartbeat bidireccional,
- estado visual conexión.

---

## Medio plazo

- Redis Pub/Sub,
- event bus,
- reconnect strategy avanzada,
- rate limiting WS.

---

## Largo plazo

- horizontal scaling,
- distributed realtime,
- observabilidad realtime,
- métricas WS,
- tracing.

---

# Relación con otros documentos

Relacionado con:

- `20_JS_ARCHITECTURE.md`
- `22_REALTIME_DASHBOARD.md`
- `23_REALTIME_NOTIFICATIONS.md`
- `24_REALTIME_KANBAN.md`
- `15_AUDIT_SYSTEM.md`
- `17_DIALOG_SYSTEM.md`
- `18_TOAST_SYSTEM.md`

---

# Conclusión

El sistema WebSocket actual representa una arquitectura realtime sorprendentemente madura para una plataforma SSR.

La plataforma ya dispone de:

- realtime contextual,
- project rooms,
- dashboard live,
- realtime notifications,
- Kanban colaborativo,
- auditoría live,
- activity feed live,
- online presence,
- broadcasting desacoplado.

La siguiente evolución natural será:

```text
Redis + distributed realtime + reusable websocket framework
```