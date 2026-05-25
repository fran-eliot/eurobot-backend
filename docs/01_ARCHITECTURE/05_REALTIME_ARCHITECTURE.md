# 05_REALTIME_ARCHITECTURE.md

# Arquitectura Realtime

# 📌 Visión General

La plataforma incorpora una arquitectura realtime basada en WebSockets.

Objetivos:

- sincronización instantánea
- colaboración multiusuario
- actualización parcial UI
- dashboards vivos

---

# ⚡ Tecnologías

- FastAPI WebSockets
- asyncio
- JSON events
- websocket rooms

---

# 🏗️ Arquitectura General

```text
Client
   │
WebSocket
   │
Connection Manager
   │
Rooms / Channels
   │
Broadcast Events
```
---

## 🧩 Connection Manager
Responsable de:
- conexiones activas
- rooms
- broadcasts
- desconexiones
- aislamiento por proyecto

## 🏠 WebSocket Rooms
La arquitectura utiliza rooms lógicas.
**Ejemplos:**
- dashboard room
- project rooms
- user notification rooms

## 📡 Eventos Actuales

### Dashboard Updates
Actualización de métricas.

### Notifications
Notificaciones realtime.

### Timeline Updates
Inserción dinámica de eventos.

### Kanban Events
Sincronización de estados.

### Users Online
Presencia de usuarios.

## 🔄 Emisión de Eventos
Eventos desacoplados mediante:
```python
emit_project_event()
```

Uso de:
```python
asyncio.create_task()
```
para evitar bloquear requests HTTP.

## 🔐 Seguridad Realtime
Validaciones:
- JWT válido
- usuario activo
- permisos
- acceso contextual
- aislamiento rooms

## 🚀 Objetivos futuros
- collaborative editing
- realtime Kanban avanzado
- live dashboards
- shared cursors
- activity streaming