# 37_LOGGING.md

# Logging Architecture

## Objetivo

Este documento describe la estrategia de logging actual y futura de Aula Robótica Platform.

Actualmente el sistema utiliza una combinación de:

- prints,
- logging Python,
- audit logs,
- browser console,
- debugging realtime,
- WebSocket inspection.

La arquitectura evolucionará progresivamente hacia:

```text
Structured Enterprise Logging
```

---

# Filosofía de Logging

El logging cumple múltiples objetivos:

- debugging,
- trazabilidad,
- observabilidad,
- seguridad,
- diagnóstico realtime,
- soporte operacional.

---

# Estado Actual

# Logging Development-first

Actualmente la plataforma se encuentra en fase de construcción activa.

Por ello, gran parte del logging está orientado a:

```text
debugging rápido y desarrollo iterativo
```

---

# Métodos actuales

## print()

Usado ampliamente para:

- inspección rápida,
- debugging,
- validación flujo,
- WebSockets,
- eventos runtime.

---

## logging Python

Uso parcial especialmente en:

- login,
- dashboard,
- backend core,
- errores relevantes.

---

# Consola Backend

Actualmente se inspecciona:

- uvicorn,
- startup,
- runtime,
- SQLAlchemy,
- errores websocket,
- excepciones FastAPI.

---

# Browser Console

El frontend usa:

- console.log(),
- websocket logs,
- network inspection,
- JS debugging,
- realtime tracing.

---

# Runtime Logs

# uvicorn

Actualmente proporciona:

- startup logs,
- reload logs,
- exceptions,
- HTTP requests,
- websocket events.

---

# SQLAlchemy

En desarrollo se observan:

- queries,
- errores SQL,
- relaciones,
- flush/commit errors.

---

# AuditLog como Logging Funcional

El sistema ya dispone de logging persistente mediante:

```text
audit_logs
```

---

# Eventos auditados

## Sesión

```text
LOGIN
LOGOUT
```

---

## Usuarios

```text
CREATE_USER
UPDATE_USER
DELETE_USER
```

---

## Proyectos

```text
CREATE_PROJECT
UPDATE_PROJECT
DELETE_PROJECT
```

---

## Tareas

```text
CREATE_TASK
UPDATE_TASK
TASK_STATUS_CHANGE
```

---

# Filosofía

El AuditLog funciona como:

```text
persistent structured operational logging
```

---

# Activity Feed

El sistema `activity_feed` actúa como:

```text
functional collaborative logging
```

---

# Diferencia importante

# AuditLog

```text
seguridad y trazabilidad técnica
```

---

# Activity Feed

```text
actividad funcional y colaboración
```

---

# Logging Realtime

# WebSockets

Actualmente se registran manualmente:

- conexiones,
- reconnections,
- eventos emitidos,
- broadcasts,
- usuarios online.

---

# Frontend Realtime Logs

El frontend usa:

```javascript
console.log()
console.error()
```

para:

- WebSocket state,
- reconnects,
- realtime payloads,
- dashboard events.

---

# Logging Frontend

# JS Runtime

Actualmente existen logs en:

- dashboard,
- notifications,
- realtime,
- Kanban,
- dialogs,
- toasts.

---

# Filosofía actual

El frontend sigue una estrategia:

```text
development-oriented debugging
```

---

# Logging Security

# Login

Actualmente el login ya posee logging parcial.

---

# Objetivos

- debugging auth,
- detectar errores JWT,
- validar cookies,
- inspeccionar sesiones.

---

# Logging Operacional

# Dashboard

El dashboard actúa parcialmente como consola operacional.

---

# Métricas visibles

- usuarios,
- tareas,
- actividades,
- productividad,
- feed realtime.

---

# Limitaciones Actuales

## 1. Logging inconsistente

Actualmente mezcla:

- print(),
- logging,
- console logs.

---

## 2. Sin logging estructurado

No existe:

```json
structured logging
```

---

## 3. Sin correlación

No hay:

- request IDs,
- trace IDs,
- correlation IDs.

---

## 4. Sin niveles claros

Uso irregular de:

```text
INFO
WARNING
ERROR
CRITICAL
```

---

## 5. Sin persistencia centralizada

Los logs viven principalmente en:

```text
consola runtime
```

---

## 6. Sin rotación

No existe:

- file rotation,
- archival,
- retention.

---

# Arquitectura Objetivo

# Structured Logging

La evolución prevista incluye:

```json
{
  "timestamp": "...",
  "level": "INFO",
  "module": "tasks",
  "event": "TASK_UPDATED",
  "user_id": 1,
  "project_id": 2
}
```

---

# Centralized Logging

Objetivo futuro:

- agregación,
- búsqueda,
- correlación,
- observabilidad.

---

# Posibles Herramientas Futuras

## Python Logging avanzado

```text
structlog
loguru
```

---

## Centralización

```text
ELK Stack
Loki
Grafana
```

---

## Cloud Logging

```text
CloudWatch
GCP Logging
```

---

# Logging Realtime Futuro

# Métricas WS

- conexiones activas,
- reconnects,
- broadcasts,
- payload size,
- dropped sockets.

---

# Frontend Logging Futuro

- JS errors,
- websocket failures,
- UX failures,
- toast failures.

---

# Logging Seguridad Futuro

- brute force,
- failed logins,
- suspicious activity,
- permission denials.

---

# Filosofía Evolutiva

La plataforma evoluciona desde:

```text
debugging manual
```

hacia:

```text
enterprise operational logging
```

---

# Relación con otros documentos

Relacionado con:

- `15_AUDIT_SYSTEM.md`
- `34_ACTIVITY_FEED_MODULE.md`
- `36_MONITORING.md`
- `38_OBSERVABILITY.md`
- `21_WEBSOCKET_SYSTEM.md`

---

# Conclusión

Aunque el logging actual todavía es híbrido y orientado a desarrollo, la plataforma ya dispone de:

- auditoría persistente,
- trazabilidad funcional,
- debugging realtime,
- inspección WebSocket,
- métricas visibles,
- runtime inspection.

La siguiente evolución natural será:

```text
structured centralized logging architecture
```