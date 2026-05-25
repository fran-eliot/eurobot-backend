# 32_NOTIFICATIONS_MODULE.md

# Módulo de Notificaciones

## Objetivo

El módulo de notificaciones proporciona comunicación realtime contextual dentro de Aula Robótica Platform.

Actualmente permite:

- generar notificaciones funcionales,
- distribuir eventos realtime,
- mostrar alertas SSR,
- sincronizar UI live,
- gestionar lectura de notificaciones,
- alimentar dropdowns dinámicos,
- actualizar contadores en tiempo real.

---

# Filosofía del módulo

El sistema NO está diseñado como simples mensajes informativos.

Actualmente funciona como:

```text
Realtime User Awareness System
```

integrado con:

- tareas,
- proyectos,
- activity feed,
- dashboard,
- WebSockets,
- toast system.

---

# Objetivos Arquitectónicos

## 1. Realtime UX

El usuario debe recibir feedback instantáneo.

---

## 2. Desacoplamiento

Las notificaciones se generan desde múltiples módulos sin dependencia fuerte.

---

## 3. Arquitectura híbrida SSR + Realtime

El sistema combina:

- render SSR inicial,
- WebSocket live updates,
- dropdown dinámico,
- toast system.

---

## 4. Escalabilidad futura

Preparado para:

- email,
- push,
- agrupación,
- preferencias,
- canales múltiples.

---

# Arquitectura General

```text
Task / Project / Activity Event
        ↓
create_notification()
        ↓
Notification DB
        ↓
emit_user_event()
        ↓
WebSocket User Channel
        ↓
notifications.js
        ↓
Dropdown Update
        ↓
Toast Realtime
```

---

# Componentes Principales

## Backend

```text
app/modules/notifications/
├── notification_model.py
├── notification_service.py
└── notifications_web.py
```

---

## Frontend

```text
templates/notifications/
└── notifications_list.html
```

:contentReference[oaicite:0]{index=0}

---

## JS Realtime

```text
static/js/notifications/notifications.js
```

:contentReference[oaicite:1]{index=1}

---

# Modelo de Notificación

La entidad `Notification` representa un evento relevante dirigido a un usuario concreto.

---

# Campos principales

```text
id_notification
user_id
type
title
message
entity_type
entity_id
url
is_read
read_at
created_at
```

---

# Filosofía del Modelo

## Notificación desacoplada

El modelo usa:

```text
entity_type
entity_id
```

en lugar de FKs rígidas.

---

# Beneficios

- flexibilidad,
- múltiples entidades,
- desacoplamiento,
- extensibilidad futura.

---

# Tipos de Notificación

Actualmente el sistema soporta:

```text
TASK_ASSIGNED
TASK_STATUS_CHANGED
TASK_UPDATED

PROJECT_MEMBER_ADDED
PROJECT_UPDATED

ACTIVITY_CREATED

SYSTEM
```

---

# Service Layer

Archivo:

```text
notification_service.py
```

:contentReference[oaicite:2]{index=2}

---

# Función Principal

## create_notification()

Core central del sistema.

---

# Responsabilidades

## Persistencia

Crear notificación DB.

---

## Emit realtime

Enviar evento WebSocket al usuario.

---

## Payload estructurado

Enviar información lista para UI.

---

# Arquitectura Realtime

## Emisión

```python
emit_user_event()
```

:contentReference[oaicite:3]{index=3}

---

# Filosofía

Cada usuario posee un canal realtime aislado.

---

# Payload emitido

```json
{
  "type": "notification",
  "notification": {
    "id_notification": ...,
    "notification_type": ...,
    "title": ...,
    "message": ...,
    "url": ...,
    "is_read": false,
    "created_at": ...
  }
}
```

:contentReference[oaicite:4]{index=4}

---

# Integración con otros módulos

# Tasks

Genera:

```text
TASK_ASSIGNED
TASK_STATUS_CHANGED
TASK_UPDATED
```

---

# Projects

Genera:

```text
PROJECT_MEMBER_ADDED
PROJECT_UPDATED
```

---

# Activities

Preparado para integración futura más profunda.

---

# Dashboard

Actualiza:

- dropdown,
- contador,
- toasts,
- activity stream contextual.

---

# Router SSR

Archivo:

```text
notifications_web.py
```

:contentReference[oaicite:5]{index=5}

---

# Rutas Principales

## Página principal

```text
GET /notifications/
```

---

## Marcar leída

```text
POST /notifications/{id}/read
```

---

## Marcar todas

```text
POST /notifications/read-all
```

---

## Abrir notificación

```text
GET /notifications/{id}/open
```

---

# Página de Notificaciones

Archivo:

```text
notifications_list.html
```

:contentReference[oaicite:6]{index=6}

---

# Funcionalidades

## Listado SSR

Muestra:

- icono contextual,
- título,
- mensaje,
- timestamp,
- estado leído/no leído.

---

## Badge "Nueva"

Las no leídas muestran:

```text
Nueva
```

:contentReference[oaicite:7]{index=7}

---

# Empty State

Si no existen notificaciones:

```text
No tienes notificaciones
```

:contentReference[oaicite:8]{index=8}

---

# Marcar todas como leídas

Disponible si:

```jinja2
unread_count > 0
```

:contentReference[oaicite:9]{index=9}

---

# Open Notification Flow

```text
click notification
    ↓
GET /notifications/{id}/open
    ↓
mark_notification_as_read()
    ↓
db.commit()
    ↓
RedirectResponse(notification.url)
```

:contentReference[oaicite:10]{index=10}

---

# Filosofía UX

La notificación actúa como:

```text
deep-link contextual
```

hacia:

- tarea,
- proyecto,
- dashboard,
- entidad relacionada.

---

# JS Realtime

Archivo:

```text
notifications.js
```

:contentReference[oaicite:11]{index=11}

---

# Arquitectura JS

## Bootstrap realtime

```javascript
DOMContentLoaded
    ↓
connectNotificationsWebSocket()
```

:contentReference[oaicite:12]{index=12}

---

# Conexión WebSocket

La conexión se realiza contra:

```text
/ws/notifications
```

:contentReference[oaicite:13]{index=13}

---

# Auto protocolo

El JS detecta automáticamente:

```text
ws://
wss://
```

según HTTP/HTTPS.

:contentReference[oaicite:14]{index=14}

---

# Keepalive

El sistema envía:

```text
ping
```

cada:

```text
30 segundos
```

:contentReference[oaicite:15]{index=15}

---

# Reconnect automático

Si el socket cae:

```javascript
setTimeout(connectNotificationsWebSocket, 3000)
```

:contentReference[oaicite:16]{index=16}

---

# Beneficios

- resiliencia,
- UX continua,
- tolerancia a cortes.

---

# Realtime Pipeline

## Evento recibido

```javascript
if (data.type === "notification")
```

:contentReference[oaicite:17]{index=17}

---

# Acciones realizadas

## prependNotification()

Añadir notificación dropdown.

---

## incrementNotificationCount()

Actualizar badge realtime.

---

## showToast()

Mostrar toast instantáneo.

:contentReference[oaicite:18]{index=18}

---

# Dropdown Realtime

La función:

```javascript
prependNotification()
```

inyecta dinámicamente:

- item,
- título,
- mensaje,
- fecha,
- enlace contextual.

:contentReference[oaicite:19]{index=19}

---

# Counter Realtime

El badge:

```text
#notification-count
```

se incrementa automáticamente. :contentReference[oaicite:20]{index=20}

---

# Toast Integration

Si existe:

```javascript
window.showToast
```

se muestra:

```javascript
showToast({
    title,
    message,
    type
})
```

:contentReference[oaicite:21]{index=21}

---

# Integración con Toast System

Las notificaciones reutilizan:

```text
18_TOAST_SYSTEM.md
```

para feedback visual inmediato.

---

# Iconografía Contextual

La página SSR renderiza iconos según tipo.

## TASK_ASSIGNED

```text
fa-tasks
```

---

## TASK_STATUS_CHANGED

```text
fa-exchange-alt
```

---

## PROJECT_MEMBER_ADDED

```text
fa-project-diagram
```

---

## PROJECT_UPDATED

```text
fa-edit
```

:contentReference[oaicite:22]{index=22}

---

# Integración con Realtime Dashboard

Las notificaciones alimentan:

- dropdown navbar,
- toast system,
- dashboard live,
- future metrics.

---

# Integración con Activity Feed

Actualmente son sistemas separados:

## Notifications

```text
orientadas al usuario
```

## Activity Feed

```text
orientado al proyecto/sistema
```

---

# Integración con RBAC

Las notificaciones heredan seguridad contextual desde el módulo emisor.

No existe acceso libre a notificaciones ajenas.

---

# Ownership

Toda query usa:

```python
Notification.user_id == current_user.id_usuario
```



---

# Estado Actual

## Implementado

- persistencia,
- realtime,
- dropdown live,
- toast integration,
- SSR page,
- unread counter,
- mark as read,
- mark all read,
- reconnect,
- keepalive,
- contextual links,
- iconografía contextual.

---

# Limitaciones actuales

## 1. Sin preferencias usuario

No existe configuración:

- mute,
- categorías,
- prioridad.

---

## 2. Sin agrupación

No se agrupan eventos similares.

---

## 3. Sin expiración

No existe retention policy.

---

## 4. Sin realtime sync de "read"

Marcar leída no sincroniza otros tabs.

---

## 5. Sin canales externos

No existe:

- email,
- push,
- mobile,
- Discord,
- Telegram.

---

## 6. Sin prioridad

No existe:

```text
info / warning / critical
```

---

# Mejoras Futuras

## Corto plazo

- sync realtime de lectura,
- badges contextuales,
- mejoras visuales,
- filtros.

---

## Medio plazo

- agrupación,
- prioridades,
- preferencias usuario,
- panel avanzado.

---

## Largo plazo

- email notifications,
- push notifications,
- mobile integration,
- distributed queues,
- notification center,
- analytics.

---

# Valor Arquitectónico

El módulo de notificaciones es una de las piezas clave para transformar la plataforma en:

```text
Realtime Collaborative Admin Platform
```

---

# Conclusión

El sistema actual ya posee capacidades muy avanzadas para el estado del proyecto.

Actualmente incluye:

- realtime,
- user channels,
- WebSockets,
- reconnect,
- SSR integration,
- dropdown dinámico,
- toast system,
- unread tracking,
- contextual deep-links,
- desacoplamiento funcional.

La siguiente evolución natural será:

```text
multi-channel enterprise notification system
```