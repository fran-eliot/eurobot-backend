# 52_ARCHITECTURAL_DECISIONS.md

# Decisiones Arquitectónicas — Aula Robótica Platform

## Objetivo del documento

Este documento recoge las principales decisiones arquitectónicas y técnicas tomadas durante el desarrollo de Aula Robótica Platform.

Su finalidad es:

- mantener trazabilidad técnica,
- justificar elecciones estructurales,
- facilitar futuras evoluciones,
- documentar trade-offs,
- preservar coherencia arquitectónica,
- acelerar onboarding técnico.

---

# Filosofía arquitectónica del proyecto

Aula Robótica Platform sigue una filosofía:

- modular,
- enterprise-oriented,
- SSR-first,
- security-first,
- realtime-ready,
- reusable UI-driven.

El sistema prioriza:

1. Seguridad
2. Mantenibilidad
3. Escalabilidad
4. Claridad arquitectónica
5. Reutilización
6. Observabilidad
7. Experiencia de usuario administrativa profesional

---

# DEC-001 — Uso de FastAPI como framework principal

## Decisión

El backend se construye sobre FastAPI.

## Motivos

- Alto rendimiento ASGI
- Excelente soporte async
- Integración natural con WebSockets
- Dependency Injection muy potente
- Swagger/OpenAPI automático
- Excelente integración con Pydantic
- Tipado moderno
- Arquitectura modular sencilla
- Gran flexibilidad enterprise

## Alternativas valoradas

- Flask
- Django
- Spring Boot

## Trade-offs

FastAPI requiere más estructura manual que Django, pero ofrece mucha mayor flexibilidad arquitectónica.

---

# DEC-002 — SQLAlchemy ORM como capa de persistencia

## Decisión

Persistencia gestionada mediante SQLAlchemy ORM.

## Motivos

- Relaciones complejas mantenibles
- Bajo acoplamiento con DB engine
- Modelado relacional expresivo
- Lazy/Eager loading configurable
- Escalabilidad futura
- Compatibilidad multi-engine
- Buen estándar profesional Python

## Trade-offs

Mayor complejidad inicial frente a SQL directo.

---

# DEC-003 — MariaDB/MySQL como motor relacional

## Decisión

Uso de MariaDB compatible con MySQL.

## Motivos

- Estabilidad
- Compatibilidad amplia
- Facilidad de despliegue
- Buen rendimiento
- Familiaridad académica/profesional
- Excelente integración SQLAlchemy

## Evolución futura

La arquitectura está preparada para migración futura a PostgreSQL.

---

# DEC-004 — Arquitectura modular por dominios

## Decisión

Separación del sistema en módulos funcionales independientes.

## Ejemplos

- auth
- users
- roles
- identities
- projects
- tasks
- activities
- dashboard
- notifications
- audit
- activity_feed

## Motivos

- Escalabilidad
- Bajo acoplamiento
- Navegabilidad
- Mantenibilidad
- Testing aislado
- Evolución independiente por dominios

---

# DEC-005 — Separación User / Identity

## Decisión

Usuario e identidad son entidades independientes.

## User representa

La persona dentro del sistema.

## Identity representa

La credencial de autenticación.

Ejemplo:

- email/password
- SAML
- OAuth
- proveedor externo

## Beneficios

- Múltiples identidades por usuario
- SSO futuro
- Modelo enterprise realista
- Flexibilidad IAM avanzada

---

# DEC-006 — JWT en cookies HTTPOnly

## Decisión

Los tokens JWT se almacenan en cookies HTTPOnly seguras.

## Motivos

- Mitigar exposición XSS
- Integración SSR limpia
- Experiencia transparente
- Mejor seguridad que localStorage
- Compatibilidad con middleware SSR

## Trade-offs

Requiere estrategia CSRF dedicada.

---

# DEC-007 — Access Token + Refresh Token

## Decisión

Separación entre tokens cortos y tokens renovables.

## Beneficios

- Mejor seguridad
- Sesiones persistentes
- Renovación transparente
- Base para refresh automático futuro

---

# DEC-008 — SessionMiddleware para Flash System SSR

## Decisión

Uso de SessionMiddleware únicamente para flash messages SSR.

## Importante

La autenticación NO usa sesiones server-side.

La sesión se emplea exclusivamente para:

- toasts,
- mensajes flash,
- feedback UX temporal.

## Beneficios

- UX moderna SSR
- Integración limpia con redirects
- Compatibilidad server-rendered

---

# DEC-009 — RBAC híbrido con permisos granulares

## Decisión

Sistema híbrido basado en:

- roles,
- permissions,
- validaciones contextuales.

## Ejemplo

```python
users:create
projects:update
activities:delete
```

## Beneficios

- Escalabilidad
- Flexibilidad
- Seguridad enterprise
- Delegación granular

---

# DEC-010 — Seguridad también en frontend

## Decisión

El frontend SSR aplica renderizado contextual por permisos.

## Ejemplos

- ocultar botones
- ocultar menús
- ocultar acciones
- ocultar tabs
- ocultar formularios

## Importante

La seguridad REAL siempre se valida en backend.

## Beneficios

- Mejor UX
- Menor ruido visual
- Navegación contextual
- Experiencia profesional

---

# DEC-011 — Render Server-Side con Jinja2

## Decisión

Frontend administrativo SSR usando Jinja2.

## Motivos

- Desarrollo rápido
- Menor complejidad SPA
- Excelente para paneles administrativos
- SSR robusto
- Mejor integración con permisos
- Menor carga JS

## Trade-offs

Menor interactividad que SPA completa.

---

# DEC-012 — Arquitectura UI reusable

## Decisión

Construcción de un mini design-system reusable.

## Componentes reutilizables

- rows
- cards
- tables
- macros
- badges
- dialogs
- toasts
- timelines
- dropdowns
- detail layouts
- action bars

## Beneficios

- DRY
- Consistencia visual
- Evolución rápida
- UX homogénea
- Mantenimiento simplificado

---

# DEC-013 — Sistema reusable de dialogs

## Decisión

Eliminar `window.confirm()` nativo.

Uso de dialogs reutilizables basados en Bootstrap/AdminLTE.

## Implementación

- `.js-confirm-form`
- dialogs dinámicos
- confirmaciones visuales modernas

## Beneficios

- UX enterprise
- Consistencia visual
- Mejor accesibilidad
- Sistema centralizado

---

# DEC-014 — Sistema centralizado de Toasts

## Decisión

Sistema reusable de notificaciones toast SSR.

## Arquitectura

- Session flash backend
- Context injection
- Render SSR
- Bootstrap Toast API
- Toast manager JS

## Beneficios

- Feedback consistente
- UX moderna
- Reutilización
- Compatibilidad SSR

---

# DEC-015 — Auditoría centralizada

## Decisión

Registro centralizado de acciones críticas.

## Eventos auditados

- login/logout
- CRUD
- cambios de estado
- uploads
- borrados
- acciones administrativas

## Beneficios

- Seguridad
- Trazabilidad
- Diagnóstico
- Compliance futuro
- Timeline administrativa

---

# DEC-016 — Activity Feed desacoplado de auditoría

## Decisión

Separar:

- audit log técnico
- activity feed funcional

## Diferencia

### Audit

Orientado a seguridad y trazabilidad técnica.

### Activity Feed

Orientado a UX y colaboración funcional.

## Beneficios

- Menor acoplamiento
- Mejor UX
- Mejor modelado semántico

---

# DEC-017 — Arquitectura realtime con WebSockets

## Decisión

Uso de WebSockets para realtime.

## Casos actuales

- dashboard realtime
- kanban realtime
- notifications
- activity updates

## Arquitectura

- connection manager
- rooms
- broadcasting
- aislamiento por proyecto

## Beneficios

- UX moderna
- colaboración realtime
- dashboards vivos

---

# DEC-018 — Arquitectura de attachments desacoplada

## Decisión

Sistema de adjuntos desacoplado del core de actividades.

## Características

- metadata persistente
- filesystem storage
- uploader relation
- ownership tracking
- MIME validation
- UUID filenames

## Beneficios

- Escalabilidad
- Seguridad
- mantenibilidad
- extensibilidad futura

---

# DEC-019 — Context Injection centralizado

## Decisión

Inyección global de contexto SSR.

## Incluye

- usuario actual
- roles
- permisos
- helpers
- menú dinámico
- breadcrumbs
- flash messages
- notifications
- helpers visuales

## Beneficios

- reducción de duplicación
- render contextual
- consistencia SSR

---

# DEC-020 — Arquitectura JS modular

## Decisión

Separación JavaScript por dominios y componentes.

## Ejemplos

- `core/`
- `dashboard/`
- `projects/`
- `notifications/`
- `dialogs/`
- `toasts/`

## Beneficios

- escalabilidad
- mantenibilidad
- aislamiento funcional
- menor deuda técnica

---

# DEC-021 — Realtime Dashboard Architecture

## Decisión

El dashboard funciona como sistema realtime desacoplado.

## Incluye

- websocket dedicado
- updates parciales
- métricas vivas
- activity timeline
- notificaciones dinámicas

## Objetivo

Crear experiencia tipo enterprise admin console.

---

# DEC-022 — Arquitectura preparada para SSO/SAML/OAuth

## Decisión

Diseñar IAM preparado para federación futura.

## Objetivos

- SAML UAH
- OAuth2
- SSO institucional
- identidades externas

## Beneficios

- Escalabilidad institucional
- Integración universitaria
- Enterprise readiness

---

# DEC-023 — Uso de uv como runtime principal

## Decisión

Uso de `uv` como entorno moderno Python.

## Beneficios

- Velocidad
- Gestión moderna
- Mejor DX
- Resolución rápida de dependencias

---

# DEC-024 — Arquitectura orientada a evolución progresiva

## Decisión

El sistema se construye de forma incremental.

## Prioridad

### Primero

- arquitectura sólida
- seguridad
- reutilización
- mantenibilidad

### Después

- features avanzadas
- DevOps
- observabilidad
- escalado

---

# DEC-025 — Filosofía “Enterprise Admin Platform”

## Decisión

La plataforma evoluciona hacia una arquitectura tipo:

- internal operations platform
- realtime admin console
- educational management platform
- robotics operations hub

## Resultado

El proyecto deja de ser un CRUD académico simple y evoluciona hacia una plataforma enterprise modular real.
