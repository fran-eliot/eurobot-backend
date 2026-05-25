# 14_CONTEXT_INJECTION.md

# SSR Context Injection Architecture

## Propósito

Este documento describe la arquitectura de inyección de contexto global SSR utilizada en Aula Robótica Platform.

La plataforma implementa un sistema avanzado de:

```text
Server-Side Context Injection
```

para:

- autorización contextual,
- navegación dinámica,
- rendering inteligente,
- notificaciones,
- breadcrumbs,
- helpers UI,
- flash messages,
- realtime UX.

---

# Filosofía Arquitectónica

La plataforma NO utiliza templates “pasivos”.

En su lugar implementa:

```text
SSR contextual inteligente
```

donde cada render recibe automáticamente:

- identidad actual,
- permisos efectivos,
- helpers reutilizables,
- navegación contextual,
- contexto UI,
- notificaciones,
- estado visual.

---

# Objetivos del Sistema

## Centralización

Evitar duplicación:

```text
request.user
roles
permissions
menu
breadcrumbs
notifications
flash
```

---

## Seguridad UI

Permitir rendering contextual:

```jinja2
{% if has_perm("tasks:update") %}
```

---

## UX Enterprise

Permitir:

- navegación adaptativa,
- layouts dinámicos,
- dashboards personalizados,
- feedback visual consistente.

---

## SSR-first

Optimizar arquitectura basada en:

```text
FastAPI + Jinja2 + AdminLTE
```

---

# Arquitectura General

```text
Request
   ↓
Auth Middleware
   ↓
request.state.user
   ↓
get_template_context()
   ↓
Jinja Global Context
   ↓
SSR Rendering
```

---

# Núcleo Principal

## context.py

El sistema principal vive en:

```text
app/web/context.py
```

:contentReference[oaicite:0]{index=0}

---

# Flujo Completo

## 1. Middleware autenticación

El middleware:

- valida JWT,
- obtiene payload,
- inyecta:

```python
request.state.user
```

---

## 2. Construcción del contexto

Cada render SSR ejecuta:

```python
get_template_context(request)
```

:contentReference[oaicite:1]{index=1}

---

## 3. Inyección global Jinja

El contexto se registra globalmente:

```python
templates.env.globals["can"] = can
```

:contentReference[oaicite:2]{index=2}

---

# Contexto Global Disponible

---

# Usuario Actual

## Variables disponibles

```python
current_user_id
current_username
current_user_roles
```

:contentReference[oaicite:3]{index=3}

---

# Helpers de Autorización

## has_role()

Verificación de roles.

Ejemplo:

```jinja2
{% if has_role("admin") %}
```

---

## has_perm()

Permisos RBAC efectivos.

Soporta:

```python
mode="any"
mode="all"
```

:contentReference[oaicite:4]{index=4}

Ejemplo:

```jinja2
{% if has_perm("tasks:update") %}
```

---

## is_owner()

Control ownership contextual.

---

## can()

Helper avanzado centralizado.

Usa:

```python
can_user_action()
```

:contentReference[oaicite:5]{index=5}

Ejemplo:

```jinja2
{% if can("update", "tasks", task) %}
```

---

## is_project_coordinator()

Roles contextuales desacoplados.

---

# Seguridad Contextual SSR

La UI SSR implementa:

```text
authorization-aware rendering
```

---

# Capacidades

## Ocultación contextual

Botones,
tabs,
acciones,
menús,
formularios.

---

## Navegación adaptativa

El menú cambia según permisos.

---

## Layouts inteligentes

Panels,
action bars,
detail layouts,
timelines.

---

## Render contextual avanzado

Cada usuario ve:

```text
solo lo relevante
```

---

# Importante

La seguridad REAL siempre reside en backend.

SSR únicamente mejora:

- UX,
- navegación,
- claridad visual.

---

# Menú Dinámico

## menu_service.py

La arquitectura de navegación utiliza:

```text
dynamic permission-driven menus
```

:contentReference[oaicite:6]{index=6}

---

# Estructura Base

El menú global define:

```python
permission: "projects:read"
```

:contentReference[oaicite:7]{index=7}

---

# Filtrado por permisos

```python
filter_menu_by_permissions()
```

elimina elementos no autorizados.

:contentReference[oaicite:8]{index=8}

---

# Estado Activo

```python
mark_active_menu()
```

gestiona:

- active,
- open,
- navegación visual.

:contentReference[oaicite:9]{index=9}

---

# Breadcrumbs Inteligentes

## build_smart_breadcrumbs()

Sistema avanzado de breadcrumbs dinámicos.

Soporta:

- entidades dinámicas,
- rutas regex,
- resolución automática,
- labels inteligentes.

:contentReference[oaicite:10]{index=10}

---

# Ejemplo

```text
/projects/4/tasks/10
```

→

```text
Proyectos
Proyecto X
Tarea Y
```

---

# Flash Message System

## Arquitectura

Sistema SSR persistente basado en:

```text
SessionMiddleware
+
server-side flash
+
toast rendering
```

---

# Implementación

## flash.py

Funciones:

```python
add_flash()
flash_success()
flash_error()
flash_warning()
flash_info()
```

:contentReference[oaicite:11]{index=11}

---

# Persistencia

Los flashes sobreviven:

```text
RedirectResponse
```

gracias a:

```python
request.session
```

---

# Cache Protection

El sistema evita duplicación de toasts mediante:

```python
request.state._cached_flash_messages
```

:contentReference[oaicite:12]{index=12}

Esto resolvió:

```text
duplicated toast rendering
multiple context evaluations
```

---

# Notifications Context

El contexto global inyecta:

```python
recent_notifications
unread_notifications_count
```

:contentReference[oaicite:13]{index=13}

---

# Notification Service Integration

Usa:

```python
get_user_notifications()
count_unread_notifications()
```

:contentReference[oaicite:14]{index=14}

---

# Objetivo UX

Permitir:

- navbar notifications,
- dropdown realtime,
- unread badges,
- SSR rendering consistente.

---

# Audit UI Helpers

## audit_ui.py

Helpers visuales para auditoría.

Funciones:

```python
get_audit_icon()
get_audit_color()
```

:contentReference[oaicite:15]{index=15}

---

# Objetivo

Centralizar:

```text
iconografía,
colores,
consistencia visual.
```

---

# Feed UI Helpers

## activity_feed_utils.py

Helpers equivalentes para activity feed.

Funciones:

```python
get_feed_icon()
get_feed_color()
```

:contentReference[oaicite:16]{index=16}

---

# Context Injection de Helpers

El contexto global expone:

```python
get_audit_icon
get_audit_color
get_feed_icon
get_feed_color
```

:contentReference[oaicite:17]{index=17}

---

# Contexto Fallback Seguro

## get_fallback_context()

Cuando:

- no hay usuario,
- falla autenticación,
- ocurre error,

el sistema devuelve contexto seguro mínimo.

:contentReference[oaicite:18]{index=18}

---

# Beneficios

## Nunca romper SSR

El render nunca debe fallar.

---

## Seguridad

Todo helper devuelve:

```python
False
```

por defecto.

---

# Session Architecture

## SessionMiddleware

La aplicación usa:

```python
SessionMiddleware
```

antes de AuthMiddleware.

:contentReference[oaicite:19]{index=19}

---

# Objetivos

Permitir:

- flash messages,
- estado SSR,
- persistencia navegación,
- futuras preferencias UI.

---

# Context Injection y Realtime

El contexto SSR convive con:

```text
WebSocket realtime architecture
```

---

# Integración

El SSR renderiza:

- estado inicial,
- feed inicial,
- notifications iniciales.

Después:

```text
WebSockets actualizan dinámicamente.
```

---

# Arquitectura Hybrid SSR + Realtime

La plataforma usa:

```text
SSR-first
+
Realtime progressive enhancement
```

---

# Ventajas del Sistema

## UX Enterprise

Experiencia tipo:

```text
admin console moderna
```

---

## DRY

Sin duplicación de helpers.

---

## Seguridad contextual

UI consciente de permisos.

---

## Navegación inteligente

Menús adaptativos.

---

## SSR profesional

Layouts ricos sin SPA compleja.

---

## Reutilización

Todos los templates reciben:

mismo contexto,
mismos helpers,
misma arquitectura.

---

# Limitaciones Actuales

## Coste de construcción contexto

Algunas partes:

- notifications,
- breadcrumbs dinámicos,

pueden generar queries adicionales.

---

## Cache parcial

Actualmente solo algunos elementos usan caching request-level.

---

## Contexto muy grande

El contexto global ha crecido considerablemente.

---

# Futuras Evoluciones

## Context Cache Layer

Cache por request más avanzada.

---

## Lazy Context Sections

Construcción diferida.

---

## Context Providers desacoplados

Separar:

```text
auth provider
navigation provider
notification provider
ui provider
```

---

## Redis-backed notification cache

Para escalabilidad realtime.

---

## Context observability

Métricas de render y contexto.

---

# Filosofía Final

La arquitectura de Context Injection es uno de los elementos más sofisticados del frontend SSR actual.

La plataforma ya NO utiliza:

```text
templates estáticos simples
```

sino:

```text
SSR contextual enterprise-grade
```

con:

- autorización contextual,
- navegación dinámica,
- feedback visual centralizado,
- rendering inteligente,
- realtime híbrido,
- UX moderna desacoplada.