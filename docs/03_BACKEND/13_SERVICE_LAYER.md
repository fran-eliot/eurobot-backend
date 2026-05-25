# 13_SERVICE_LAYER.md

# Backend Service Layer Architecture

## Propósito

Este documento describe la arquitectura de la capa de servicios (`Service Layer`) de Aula Robótica Platform.

La plataforma implementa una arquitectura backend basada en:

```text
Router → Service → ORM/Database
```

con separación clara entre:

- presentación,
- autorización,
- lógica de negocio,
- persistencia,
- realtime,
- auditoría,
- notificaciones.

---

# Filosofía Arquitectónica

La plataforma NO implementa lógica compleja directamente en routers FastAPI.

Los routers deben permanecer:

```text
finos,
declarativos,
predecibles.
```

Toda lógica de negocio relevante se desplaza hacia:

```text
services/
```

---

# Objetivos de la Service Layer

## Separación de responsabilidades

Separar:

- HTTP,
- SSR,
- WebSockets,
- ORM,
- negocio,
- seguridad,
- auditoría.

---

## Reutilización

La lógica puede reutilizarse desde:

- rutas SSR,
- APIs REST,
- tareas background,
- WebSockets,
- workers futuros.

---

## Escalabilidad

Permite evolucionar hacia:

```text
microservicios,
CQRS,
event-driven,
workers async,
APIs públicas.
```

---

## Testing

La lógica puede testearse aislada de FastAPI.

---

# Arquitectura General

```text
Routers
   ↓
Service Layer
   ↓
SQLAlchemy ORM
   ↓
MariaDB
```

---

# Organización de Servicios

La arquitectura sigue separación modular por dominio.

Ejemplo:

```text
modules/
├── auth/
│   └── auth_service.py
├── projects/
│   └── projects_service.py
├── tasks/
│   └── task_service.py
├── notifications/
│   └── notification_service.py
├── activity_feed/
│   └── activity_feed_service.py
├── audit/
│   └── audit_service.py
```

---

# Tipos de Servicios

## 1. Business Services

Implementan lógica funcional principal.

Ejemplos:

```text
project_service
task_service
user_service
```

---

## 2. View Services

Servicios orientados a render SSR.

Ejemplos:

```text
task_view_service
user_view_service
dashboard_service
```

Responsabilidades:

- agregación de datos,
- joins complejos,
- estadísticas,
- estructuras para templates.

---

## 3. Infrastructure Services

Servicios transversales.

Ejemplos:

```text
audit_service
notification_service
activity_feed_service
```

---

# Arquitectura por Dominio

---

# Auth Service

## auth_service.py

Responsable de:

- autenticación local,
- JWT,
- payloads,
- cookies,
- login/logout,
- validación credenciales.

Funciones relevantes:

```python
authenticate_user()
create_access_token()
build_auth_payload()
```

:contentReference[oaicite:0]{index=0}

---

# SAML Service

## saml_service.py

Responsable de:

- integración SAML,
- ACS,
- metadata,
- validación assertions,
- auto-provisioning,
- integración IdP.

Arquitectura desacoplada del RBAC interno.

:contentReference[oaicite:1]{index=1}

---

# User Service

## user_service.py

Responsable de:

- CRUD usuarios,
- activación/desactivación,
- relaciones roles,
- operaciones administrativas.

Incluye integración con:

- auditoría,
- permisos,
- validación.

:contentReference[oaicite:2]{index=2}

---

# Role Service

## role_service.py

Responsable de:

- CRUD roles,
- gestión permisos,
- asignación RBAC.

:contentReference[oaicite:3]{index=3}

---

# Identity Service

## identity_service.py

Gestiona:

- identidades federadas,
- múltiples providers,
- vinculación usuario-identidad.

Arquitectura preparada para:

```text
local
SAML
OAuth
OIDC
```

:contentReference[oaicite:4]{index=4}

---

# Projects Service

## projects_service.py

Responsable de:

- CRUD proyectos,
- estado proyectos,
- relaciones proyecto-usuario,
- coordinación operativa.

Integraciones:

- activity feed,
- auditoría,
- realtime,
- permisos.

:contentReference[oaicite:5]{index=5}

---

# Project Members Service

## project_members_service.py

Responsable de:

- gestión miembros proyecto,
- roles contextuales,
- membership,
- coordinadores.

Arquitectura desacoplada del RBAC global.

:contentReference[oaicite:6]{index=6}

---

# Task Service

## task_service.py

Uno de los módulos más avanzados actualmente.

Responsable de:

- CRUD tareas,
- estados Kanban,
- prioridades,
- asignación usuarios,
- realtime updates,
- activity feed,
- auditoría.

Incluye:

```text
todo
doing
done
```

:contentReference[oaicite:7]{index=7}

---

# Task View Service

## task_view_service.py

Servicio especializado SSR.

Responsabilidades:

- joins complejos,
- render detail layouts,
- agregación relaciones,
- optimización templates.

:contentReference[oaicite:8]{index=8}

---

# Dashboard Service

## dashboard_service.py

Responsable de:

- métricas globales,
- KPIs,
- estadísticas,
- timeline dashboard,
- agregación realtime.

Incluye:

- usuarios,
- proyectos,
- tareas,
- actividades,
- auditoría,
- activity feed.

:contentReference[oaicite:9]{index=9}

---

# Notification Service

## notification_service.py

Responsable de:

- notificaciones internas,
- unread tracking,
- realtime notifications,
- integración SSR.

Preparado para:

```text
email
push
websocket
future mobile
```

:contentReference[oaicite:10]{index=10}

---

# Audit Service

## audit_service.py

Responsable de:

- auditoría centralizada,
- trazabilidad,
- logging administrativo,
- eventos críticos.

Eventos auditados:

```text
login
logout
CRUD
uploads
delete
status changes
admin actions
```

:contentReference[oaicite:11]{index=11}

---

# Activity Feed Service

## activity_feed_service.py

Sistema desacoplado de auditoría.

Orientado a:

```text
UX
timeline
colaboración
actividad funcional
```

NO seguridad.

Ejemplos:

```text
usuario creó tarea,
usuario subió adjunto,
actividad completada.
```

:contentReference[oaicite:12]{index=12}

---

# Arquitectura SSR

Los routers SSR delegan:

```python
data = dashboard_service.get_dashboard_stats()
```

y únicamente renderizan:

```python
return templates.TemplateResponse(...)
```

Esto mantiene:

```text
routers finos,
SSR limpio,
mejor mantenibilidad.
```

---

# Patrón de Dependencias

Los services normalmente reciben:

```python
db: Session
current_user
request
```

---

# Integración con Auditoría

Muchos services integran automáticamente:

```python
log_action(...)
```

desde audit_service.

---

# Integración con Activity Feed

Los eventos funcionales usan:

```python
create_feed_event(...)
```

---

# Integración Realtime

Algunos services emiten eventos WebSocket:

```python
broadcast_to_project()
broadcast_dashboard_update()
```

Esto desacopla:

```text
persistencia
≠
realtime transport
```

---

# Arquitectura Async-Ready

Aunque gran parte del ORM es sync actualmente, la arquitectura está preparada para:

```text
async services
background tasks
workers
event queues
```

---

# Validación de Negocio

La validación compleja NO vive en templates.

Ejemplos:

- ownership,
- coordinadores,
- permisos derivados,
- reglas contexto proyecto.

---

# Seguridad

La autorización se ejecuta en:

```text
dependencies
+
services
```

Nunca únicamente en frontend.

---

# Patrón Thin Router

## Router

Responsabilidades:

- parse request,
- dependencias,
- SSR response,
- redirect.

---

## Service

Responsabilidades:

- negocio,
- validación,
- persistencia,
- integración,
- realtime,
- auditoría.

---

# Ventajas de la Arquitectura

## Escalabilidad

Preparada para crecimiento real.

---

## Reutilización

Lógica centralizada.

---

## Bajo acoplamiento

Separación clara de capas.

---

## Testing

Más sencillo testear lógica.

---

## Enterprise-readiness

Arquitectura cercana a plataformas enterprise reales.

---

## SSR-friendly

Perfectamente compatible con:

```text
FastAPI + Jinja2 + AdminLTE
```

---

# Limitaciones Actuales

## Algunos services todavía mezclan responsabilidades

Especialmente:

- ORM,
- validación,
- emisión realtime.

---

## Falta capa repository explícita

Actualmente:

```text
Service → ORM directo
```

---

## Algunas operaciones complejas aún viven parcialmente en routers

Pendiente de refactor.

---

## Transacciones avanzadas limitadas

No existe todavía:

```text
Unit of Work
```

formal.

---

# Futuras Evoluciones

## Repository Pattern

Separar ORM del negocio.

---

## CQRS parcial

Separar:

```text
commands
queries
```

---

## Event Bus

Arquitectura event-driven.

---

## Background Workers

Especialmente para:

- notificaciones,
- emails,
- analytics,
- sincronización externa.

---

## Cache Layer

Redis/memory cache.

---

## Async ORM

Migración futura.

---

# Filosofía Final

La Service Layer es actualmente uno de los núcleos arquitectónicos más importantes de Aula Robótica Platform.

La plataforma ya NO funciona como:

```text
CRUD monolítico simple
```

sino como:

```text
modular enterprise backend platform
```

con separación progresiva entre:

- transporte,
- lógica,
- realtime,
- seguridad,
- persistencia,
- render SSR.