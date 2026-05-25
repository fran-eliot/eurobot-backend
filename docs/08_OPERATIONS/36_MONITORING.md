# 36_MONITORING.md

# Monitoring Architecture

## Objetivo

Este documento describe la estrategia de monitorización actual y futura de Aula Robótica Platform.

Actualmente la plataforma ya posee múltiples mecanismos de observación operativa:

- métricas dashboard,
- activity feed,
- audit logs,
- notificaciones realtime,
- logs consola,
- debugging manual,
- seguimiento WebSocket,
- métricas contextuales.

Aunque todavía no existe una plataforma formal de monitoring enterprise, la arquitectura ya está evolucionando hacia un modelo:

```text
Operational Realtime Monitoring Platform
```

---

# Filosofía de Monitoring

El objetivo no es únicamente detectar errores.

La plataforma busca:

- observar actividad,
- supervisar operaciones,
- detectar anomalías,
- entender comportamiento usuario,
- analizar colaboración,
- monitorizar realtime,
- preparar observabilidad avanzada.

---

# Estado Actual

# Monitoring actual implementado

## Dashboard Metrics

El dashboard ya funciona parcialmente como sistema de monitoring operativo.

Incluye:

- usuarios,
- roles,
- identidades,
- proyectos,
- tareas,
- actividades,
- productividad,
- activity feed realtime.

---

# Dashboard contextual

## Admin

Vista global sistema.

## Usuarios normales

Vista contextual según acceso.

---

# Métricas actuales

## Usuarios

```text
total_users
active_users
inactive_users
```

---

## IAM

```text
total_roles
total_identities
external_identities
```

---

## Operación

```text
projects
tasks
activities
hours
```

---

## Productividad

:contentReference[oaicite:0]{index=0}

---

# Activity Feed como Monitoring

El sistema `activity_feed` actúa como timeline operacional realtime.

Permite observar:

- creación de tareas,
- cambios de estado,
- actividades,
- miembros,
- operaciones colaborativas.

---

# AuditLog como Monitoring Seguridad

El sistema `audit_logs` permite monitorizar:

- login/logout,
- operaciones críticas,
- cambios administrativos,
- acciones de usuario,
- trazabilidad sistema.

---

# Notificaciones Realtime

Las notificaciones permiten:

- awareness inmediata,
- detección de cambios,
- seguimiento operativo live.

---

# Realtime Monitoring

# WebSockets

Actualmente el sistema monitoriza indirectamente:

- conexiones activas,
- reconnects,
- usuarios online,
- eventos broadcast,
- canales dashboard,
- canales proyecto.

---

# Users Online

El sistema ya muestra:

```text
usuarios conectados
```

en proyectos realtime.

---

# Reconnect Monitoring

Los módulos realtime implementan:

```javascript
setTimeout(reconnect...)
```

y logs de reconexión.

---

# Monitoring Manual Actual

# Consola Backend

Actualmente se emplea:

```python
print()
logging
```

durante desarrollo.

---

# Uso actual

Especialmente en:

- login,
- dashboard,
- realtime,
- debugging,
- servicios críticos.

---

# Browser DevTools

Actualmente se usan:

- console logs,
- network,
- websocket frames,
- errors,
- realtime inspection.

---

# Postman

En etapas tempranas se utilizó para:

- pruebas API,
- debugging,
- validación endpoints,
- JWT/cookies,
- workflows backend.

---

# Runtime Monitoring

# uv + uvicorn

La plataforma se ejecuta mediante:

```text
uv
uvicorn
```

---

# Monitoring actual runtime

Se observan:

- startup errors,
- reloads,
- websocket exceptions,
- SQLAlchemy errors,
- dependency issues.

---

# Configuración Actual

# Variables de entorno

La configuración usa:

```text
.env
```

para:

- DB,
- JWT,
- runtime,
- configuración general.

---

# Entornos

Actualmente orientado principalmente a:

```text
development environment
```

---

# Monitoring Realtime

# Dashboard Feed Live

El dashboard actúa parcialmente como consola operacional realtime.

Incluye:

- activity stream,
- updates live,
- toast feedback,
- WebSocket events.

---

# Arquitectura híbrida

```text
SSR
+
Realtime incremental
```

---

# Event Monitoring

Actualmente el sistema monitoriza eventos funcionales:

- TASK_CREATED,
- TASK_UPDATED,
- TASK_STATUS_CHANGED,
- ACTIVITY_CREATED,
- MEMBER_JOINED.

---

# Seguridad y Monitoring

# Backend-first

Toda lógica crítica se monitoriza desde backend.

---

# Activity Feed

Monitoriza:

```text
operación funcional
```

---

# AuditLog

Monitoriza:

```text
seguridad y trazabilidad
```

---

# Monitoring Gap Actual

Actualmente todavía NO existe:

- Prometheus,
- Grafana,
- tracing,
- metrics exporters,
- health endpoints avanzados,
- APM,
- distributed monitoring.

---

# Limitaciones Actuales

## 1. Monitoring manual

Gran parte del seguimiento sigue siendo:

```text
console-driven debugging
```

---

## 2. Sin métricas técnicas

No existen métricas sobre:

- latency,
- CPU,
- RAM,
- query time,
- websocket throughput.

---

## 3. Sin healthcheck avanzado

Actualmente no existe:

```text
/health
/metrics
```

enterprise-ready.

---

## 4. Sin alerting

No hay:

- emails,
- alerts,
- thresholds,
- incident detection.

---

## 5. Sin observabilidad distribuida

No existe:

- tracing,
- correlation IDs,
- distributed events.

---

# Arquitectura Objetivo

# Monitoring futuro

La visión futura incluye:

## Runtime Monitoring

- CPU,
- memoria,
- workers,
- conexiones.

---

## Database Monitoring

- queries lentas,
- locks,
- conexiones,
- índices.

---

## Realtime Monitoring

- websocket rooms,
- usuarios online,
- reconnects,
- broadcasts,
- dropped connections.

---

## UX Monitoring

- errores frontend,
- toasts críticos,
- navegación,
- latencia UI.

---

## Seguridad

- login failures,
- actividad sospechosa,
- auditoría avanzada.

---

# Herramientas Futuras Previstas

# Metrics

Posibles herramientas:

```text
Prometheus
Grafana
OpenTelemetry
```

---

# Logging

```text
structured logging
centralized logs
```

---

# Tracing

```text
distributed tracing
request tracing
```

---

# Alerting

```text
Slack
Discord
Email
```

---

# Healthchecks

Endpoints futuros:

```text
/health
/ready
/live
/metrics
```

---

# Visión Estratégica

El sistema evolucionará hacia:

```text
Realtime Educational Operations Monitoring Platform
```

---

# Relación con otros documentos

Relacionado con:

- `37_LOGGING.md`
- `38_OBSERVABILITY.md`
- `33_DASHBOARD_MODULE.md`
- `34_ACTIVITY_FEED_MODULE.md`
- `21_WEBSOCKET_SYSTEM.md`

---

# Conclusión

Aunque el monitoring actual todavía está en fase evolutiva, la plataforma ya dispone de:

- métricas operativas,
- activity streams,
- auditoría,
- realtime feedback,
- dashboard vivo,
- eventos contextualizados.

La evolución natural será incorporar:

```text
enterprise monitoring + observability stack
```

sin perder la arquitectura realtime ya existente.