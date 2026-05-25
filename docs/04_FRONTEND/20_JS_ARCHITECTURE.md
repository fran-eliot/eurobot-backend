# 20_JS_ARCHITECTURE.md

# Arquitectura JavaScript

## Objetivo

Este documento describe la arquitectura JavaScript actual de Aula Robótica Platform.

La plataforma utiliza JavaScript como capa de mejora progresiva sobre una arquitectura principal:

```text
FastAPI + Jinja2 SSR + AdminLTE + WebSockets
```

El frontend no es una SPA, sino una aplicación SSR enriquecida con módulos JavaScript específicos para:

- dialogs,
- toasts,
- notificaciones realtime,
- dashboard realtime,
- Kanban realtime,
- activity feed,
- WebSocket UX,
- interacciones progresivas.

---

# Filosofía Arquitectónica

La arquitectura JavaScript sigue una filosofía:

```text
SSR-first + Progressive Enhancement
```

Esto significa:

- el backend renderiza la vista inicial,
- Jinja2 genera HTML completo,
- JS añade interactividad,
- WebSockets actualizan zonas concretas,
- no existe dependencia de un framework SPA.

---

# Estado Actual

La estructura JavaScript actual está organizada en:

```text
static/js/
├── core/
│   ├── confirmations.js
│   ├── dialog.js
│   ├── notifications.js
│   └── toasts.js
│
├── dashboard/
│   └── dashboard.js
│
├── projects/
│   └── project_detail.js
│
└── realtime/
    ├── audit_timeline.js
    └── websocket.js
```

Los archivos `audit_timeline.js` y `websocket.js` existen como preparación arquitectónica, pero todavía no contienen la lógica extraída desde los módulos actuales. :contentReference[oaicite:0]{index=0}

---

# Arquitectura General

```text
base.html
   ↓
core JS
   ↓
page-specific JS
   ↓
WebSocket handlers
   ↓
DOM updates
```

---

# Carga Global de Scripts

Los scripts principales se cargan desde `base.html`.

## Librerías base

```html
<script src="/static/adminlte/plugins/jquery/jquery.min.js"></script>
<script src="/static/adminlte/plugins/bootstrap/js/bootstrap.bundle.min.js"></script>
<script src="/static/adminlte/js/adminlte.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
```

## Core JS

```html
<script src="{{ url_for('static', path='js/core/toasts.js') }}"></script>
<script src="{{ url_for('static', path='js/core/dialog.js') }}"></script>
<script src="{{ url_for('static', path='js/core/confirmations.js') }}"></script>
<script src="{{ url_for('static', path='js/core/notifications.js') }}"></script>
```

## Page-specific JS

Cada template puede añadir lógica propia mediante:

```jinja2
{% block extra_js %}{% endblock %}
```

:contentReference[oaicite:1]{index=1}

---

# Core JS

## `core/dialog.js`

Define funciones globales reutilizables basadas en SweetAlert2:

```javascript
showSuccess()
showError()
showWarning()
confirmAction()
```

`confirmAction()` centraliza confirmaciones modernas y devuelve un booleano según la decisión del usuario. :contentReference[oaicite:2]{index=2}

---

## `core/confirmations.js`

Intercepta formularios con:

```html
.js-confirm-form
```

Lee atributos declarativos:

```html
data-confirm-title
data-confirm-text
data-confirm-button
data-confirm-icon
```

y ejecuta `confirmAction()` antes de permitir el submit. :contentReference[oaicite:3]{index=3}

---

## `core/toasts.js`

Define la API global:

```javascript
showToast({
    title,
    message,
    type,
    duration
})
```

Crea dinámicamente el toast, lo inserta en `#toast-container` y lo elimina automáticamente tras la duración configurada. :contentReference[oaicite:4]{index=4}

---

## `core/notifications.js`

Gestiona el WebSocket global de notificaciones:

```text
/ws/notifications
```

Responsabilidades:

- abrir conexión WebSocket,
- mantener conexión con ping,
- recibir notificaciones,
- insertarlas en el dropdown,
- incrementar contador,
- mostrar toast,
- reconectar automáticamente.

:contentReference[oaicite:5]{index=5}

---

# Dashboard JS

## `dashboard/dashboard.js`

Gestiona el dashboard realtime mediante:

```text
/ws/dashboard
```

Responsabilidades:

- conectar al WebSocket del dashboard,
- recibir eventos de activity feed,
- insertar actividad reciente,
- evitar duplicados,
- limitar número de elementos visibles,
- mostrar toast informativo.

:contentReference[oaicite:6]{index=6}

---

# Project Detail JS

## `projects/project_detail.js`

Es actualmente el módulo JavaScript más complejo.

Gestiona:

- Kanban drag & drop,
- cambio de estado por botón,
- optimistic UI,
- rollback en error,
- WebSocket de proyecto,
- usuarios online,
- activity feed realtime,
- auditoría realtime,
- contadores Kanban,
- empty states dinámicos.

:contentReference[oaicite:7]{index=7}

---

# Configuración desde SSR

Las páginas pueden inyectar configuración inicial mediante:

```javascript
window.APP_CONFIG = {
    currentUserId: Number("{{ current_user_id | tojson }}"),
    projectId: Number("{{ project.id_project | tojson }}")
};
```

Esto permite conectar datos SSR con lógica JavaScript sin acoplar el archivo JS a Jinja2. :contentReference[oaicite:8]{index=8}

---

# WebSocket Architecture

La capa JavaScript consume tres canales WebSocket principales:

```text
/ws/projects/{project_id}
/ws/dashboard
/ws/notifications
```

El backend gestiona rooms de proyecto, conexiones dashboard y conexiones por usuario. :contentReference[oaicite:9]{index=9}

Los endpoints WebSocket validan usuario mediante JWT en cookie y rechazan conexiones no autorizadas con código `1008`. :contentReference[oaicite:10]{index=10}

---

# Patrón Realtime General

```text
SSR render inicial
    ↓
JS conecta WebSocket
    ↓
Backend emite evento
    ↓
JS recibe JSON
    ↓
Actualización parcial DOM
    ↓
Toast / Feed / Counter / Timeline
```

---

# Project WebSocket Events

`project_detail.js` maneja actualmente:

```javascript
users_online
task_updated
audit
feed_event
```

Cada evento actualiza una zona concreta de la pantalla:

| Evento | Efecto |
|---|---|
| `users_online` | actualiza usuarios conectados |
| `task_updated` | mueve tarjeta Kanban |
| `audit` | añade entrada timeline |
| `feed_event` | inserta evento en activity feed |

:contentReference[oaicite:11]{index=11}

---

# Dashboard WebSocket Events

El dashboard procesa:

```javascript
dashboard_feed_event
```

y actualiza:

- lista de actividad reciente,
- toast informativo,
- feed visual.

:contentReference[oaicite:12]{index=12}

---

# Notification WebSocket Events

El sistema de notificaciones procesa:

```javascript
notification
```

y actualiza:

- dropdown navbar,
- contador de no leídas,
- toast visual.

:contentReference[oaicite:13]{index=13}

---

# Patrón Optimistic UI

El Kanban implementa optimistic UI.

## Flujo

```text
Usuario mueve tarjeta
    ↓
JS mueve tarjeta inmediatamente
    ↓
POST /tasks/{id}/status
    ↓
Si OK: confirma visualmente
    ↓
Si error: rollback
```

Este patrón mejora percepción de velocidad, pero requiere buen manejo de errores y sincronización realtime. :contentReference[oaicite:14]{index=14}

---

# DOM Update Patterns

La arquitectura usa actualizaciones parciales del DOM:

- `prepend()`,
- `appendChild()`,
- `insertAdjacentHTML()`,
- `querySelector()`,
- `dataset`,
- clases temporales de estado.

Ejemplos:

- insertar feed realtime,
- mover tarjetas Kanban,
- actualizar contadores,
- eliminar empty states,
- renderizar usuarios conectados.

---

# Estado de Modularización

## Módulos ya separados

- dialogs,
- confirmations,
- toasts,
- notifications,
- dashboard,
- project detail.

## Pendiente de modularizar

Actualmente `project_detail.js` contiene demasiadas responsabilidades:

- Kanban,
- WebSocket,
- audit timeline,
- feed,
- online users,
- helpers visuales.

Los archivos `realtime/audit_timeline.js` y `realtime/websocket.js` ya existen, pero todavía falta traspasarles lógica. :contentReference[oaicite:15]{index=15}

---

# Propuesta de Refactor Futuro

## `realtime/websocket.js`

Debería centralizar:

- creación de URL `ws/wss`,
- reconexión,
- ping/keepalive,
- parseo seguro JSON,
- callbacks por tipo de evento,
- cierre controlado.

---

## `realtime/audit_timeline.js`

Debería centralizar:

- `appendAuditToTimeline()`,
- `getAuditIcon()`,
- `getAuditColor()`,
- agrupación por día,
- highlight temporal.

---

## `projects/kanban.js`

Futuro módulo recomendado para:

- drag & drop,
- status buttons,
- optimistic UI,
- rollback,
- counters,
- empty states.

---

## `projects/project_feed.js`

Futuro módulo recomendado para:

- `prependFeedEvent()`,
- deduplicación,
- render de feed,
- formato de fechas.

---

# Riesgos Actuales

## 1. Demasiada lógica en `project_detail.js`

Es funcional, pero grande.

---

## 2. Helpers duplicados frontend/backend

Hay mappings visuales de audit/feed tanto en backend como en JS.

---

## 3. `alert()` residual

En el rollback del Kanban todavía aparece:

```javascript
alert("Error al actualizar estado");
```

Sería mejor sustituirlo por `showToast()` o `showError()`. :contentReference[oaicite:16]{index=16}

---

## 4. Reconexión básica

Los WebSockets reconectan con `setTimeout`, pero aún no hay:

- backoff exponencial,
- límite de reintentos,
- estado visual de conexión,
- cierre intencional.

---

## 5. Falta JS bundling

Actualmente los scripts se cargan como archivos sueltos.

Es adecuado para el estado actual, pero puede evolucionar a:

- Vite,
- ES modules,
- bundling ligero.

---

# Buenas Prácticas Actuales

## Declarative hooks

Uso de clases y atributos declarativos:

```html
.js-confirm-form
.js-change-status
data-task-id
data-next-status
data-status
```

---

## Progressive enhancement

La vista inicial funciona con SSR.

JS añade experiencia avanzada.

---

## Separación por dominio

Hay carpetas por dominio:

```text
core/
dashboard/
projects/
realtime/
```

---

## Integración limpia con SSR

`window.APP_CONFIG` evita incrustar demasiada lógica Jinja dentro del JS.

---

# Reglas Recomendadas

## 1. No usar `onclick` inline

Preferir:

```javascript
addEventListener()
```

---

## 2. Usar `data-*`

Para comunicar HTML SSR con JS.

---

## 3. No duplicar lógica de permisos

La autorización real pertenece al backend.

JS solo mejora UX.

---

## 4. Centralizar WebSockets

Evitar crear conexiones ad hoc sin patrón común.

---

## 5. Usar toast/dialog system

No usar:

```javascript
alert()
confirm()
```

---

## 6. Separar módulos grandes

Cuando un archivo supera varias responsabilidades, dividirlo por dominio.

---

# Roadmap JS

## Corto plazo

- eliminar `alert()` residual,
- extraer WebSocket helper,
- extraer audit timeline,
- extraer Kanban logic,
- añadir manejo robusto de errores.

---

## Medio plazo

- ES modules,
- helpers compartidos,
- websocket manager frontend,
- reconnect strategy avanzada,
- tests básicos JS.

---

## Largo plazo

- Vite o bundling ligero,
- TypeScript opcional,
- componentes realtime reutilizables,
- design system JS formal.

---

# Relación con otros documentos

Relacionado con:

- `17_DIALOG_SYSTEM.md`
- `18_TOAST_SYSTEM.md`
- `19_COMPONENT_PATTERNS.md`
- `21_WEBSOCKET_SYSTEM.md`
- `22_REALTIME_DASHBOARD.md`
- `23_REALTIME_NOTIFICATIONS.md`
- `24_REALTIME_KANBAN.md`

---

# Conclusión

La arquitectura JavaScript actual ya aporta una capa avanzada de interactividad sobre SSR.

El sistema dispone de:

- core JS reusable,
- dialogs centralizados,
- toasts globales,
- notificaciones realtime,
- dashboard realtime,
- Kanban colaborativo,
- WebSocket rooms,
- progressive enhancement.

La evolución natural es extraer responsabilidades de `project_detail.js` hacia módulos especializados y consolidar un pequeño framework interno de frontend realtime.