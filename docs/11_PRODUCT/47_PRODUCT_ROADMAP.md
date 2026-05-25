# 47_PRODUCT_ROADMAP.md

# Aula Robótica Platform — Product Roadmap

Roadmap estratégico, técnico y funcional de evolución de la plataforma.

---

# Visión del producto

Aula Robótica Platform evoluciona hacia una plataforma enterprise modular orientada a:

- gestión operativa del Aula de Robótica,
- administración académica,
- coordinación de proyectos,
- colaboración educativa,
- operación realtime,
- gestión de competiciones,
- observabilidad institucional,
- integración SSO universitaria.

El objetivo ya no es únicamente construir un CRUD administrativo, sino una:

- internal operations platform,
- educational management platform,
- realtime collaboration platform,
- robotics operations hub.

---

# Estado actual del producto (Current State)

## Plataforma actualmente implementada

La plataforma dispone actualmente de una arquitectura SSR enterprise moderna basada en:

- FastAPI
- SQLAlchemy
- MariaDB
- Jinja2 SSR
- JWT + HTTPOnly Cookies
- WebSockets realtime
- Arquitectura modular reusable

---

# Funcionalidades implementadas

## IAM / Seguridad

- Login JWT
- Refresh Tokens
- HTTPOnly Cookies
- RBAC granular
- Roles globales
- Roles contextuales
- Helpers de autorización
- Context Injection SSR
- Seguridad UI contextual

---

## Gestión administrativa

- Usuarios
- Roles
- Identidades
- Dashboard administrativo
- Navegación dinámica
- Menús contextuales
- Breadcrumbs

---

## Gestión de proyectos

- CRUD proyectos
- Miembros de proyecto
- Roles contextuales
- Timeline funcional
- Actividad realtime
- Coordinación operativa

---

## Gestión de tareas

- CRUD tareas
- Kanban realtime
- Prioridades
- Estados
- Ownership
- Asignaciones

---

## Sistema de actividades

- Registro operativo
- Tracking temporal
- Timeline
- Relaciones proyecto/tarea
- Actividad colaborativa

---

## Sistema de adjuntos

- Upload de archivos
- Metadata persistente
- UUID filenames
- MIME validation
- Ownership tracking
- Descarga segura

---

## Auditoría y trazabilidad

- Audit logs centralizados
- Timeline administrativa
- Eventos críticos
- Logging contextual
- Auditoría SSR integrada

---

## Realtime Architecture

- Dashboard realtime
- Kanban realtime
- Notifications realtime
- WebSocket rooms
- Broadcasting contextual
- Connection manager

---

## Frontend/UI System

- Arquitectura reusable SSR
- Detail layouts modernos
- Cards reutilizables
- Tables reutilizables
- Dialog system
- Toast system
- Timeline system
- Macros Jinja2
- Rendering contextual
- UI authorization

---

# Near-Term Roadmap (0–3 meses)

## Consolidación técnica

### Objetivos prioritarios

- Refactor JS modular completo
- Consolidación frontend architecture
- Mejoras UX enterprise
- Realtime stability improvements
- Cache strategy
- Error handling unificado
- Mejoras de accesibilidad

---

## Testing Expansion

### Unit Testing

- services
- repositories
- auth helpers
- websocket managers

### Integration Testing

- auth flows
- realtime flows
- uploads
- permissions

### UI Testing

- dialogs
- toasts
- contextual rendering
- reusable components

---

## Seguridad avanzada

### Prioridades

- CSRF protection
- Session invalidation
- Token revocation
- Rate limiting
- Upload hardening
- WebSocket authorization hardening

---

## Observabilidad inicial

### Logging

- structured logging
- request tracing
- websocket logs
- audit enrichment

### Monitoring

- métricas básicas
- health checks
- error tracking

---

# Mid-Term Roadmap (3–9 meses)

# Módulo académico

## Students Module

- perfiles estudiante
- estado académico
- participación
- histórico operativo

---

## Courses / Workshops

- talleres
- cursos
- laboratorios
- sesiones prácticas

---

## Evaluación y participación

- seguimiento de actividad
- métricas de participación
- progreso académico

---

# Gestión operativa avanzada

## Inventory System

- inventario robótico
- componentes
- kits
- disponibilidad
- trazabilidad

---

## Equipment Reservations

- reservas
- calendario
- disponibilidad
- préstamos

---

## Competition System

### Eurobot

- equipos
- rankings
- participantes
- documentación
- resultados

---

# Arquitectura realtime avanzada

## Objetivos

- websocket reconnect
- event queue
- optimistic UI
- sync parcial
- invalidación inteligente

---

# Mid/Long-Term Technical Roadmap

# DevOps Roadmap

## Infraestructura

- Docker
- Docker Compose
- Reverse Proxy
- HTTPS
- Static serving optimizado

---

## CI/CD

- GitHub Actions
- pipelines automáticos
- tests automáticos
- linting
- quality gates

---

## Calidad de código

- SonarCloud
- coverage reports
- static analysis
- security analysis

---

## Entornos

- local
- development
- staging
- production

---

## Observabilidad avanzada

### Monitoring

- Prometheus
- Grafana
- uptime monitoring

### Logging

- centralización logs
- structured logs
- audit analytics

---

# Security Roadmap

## Seguridad avanzada

- 2FA
- OAuth2
- SAML institucional UAH
- SSO universitario
- políticas avanzadas
- session management
- refresh rotation

---

## Hardening

- CSP headers
- CSRF full protection
- upload sandboxing
- websocket hardening
- rate limiting avanzado

---

# Long-Term Product Vision (9–24 meses)

# Plataforma institucional completa

## Objetivos

Convertir Aula Robótica Platform en:

- plataforma operativa del aula,
- plataforma de coordinación académica,
- plataforma de gestión de competiciones,
- plataforma colaborativa realtime,
- plataforma institucional integrada.

---

# Ecosistema esperado

## Integraciones

- SSO UAH
- APIs universitarias
- exportaciones académicas
- reporting institucional

---

## Analytics

- dashboards operativos
- métricas académicas
- participación
- productividad
- uso de recursos

---

## Inteligencia operacional

- recomendaciones
- automatización
- alertas inteligentes
- reporting avanzado

---

# Technical Debt

## Frontend

- modularización JS completa
- reducción inline scripts
- unificación componentes legacy

---

## Backend

- normalización parcial naming
- consolidación services layer
- refactor permisos contextuales

---

## Realtime

- reconnect strategy
- event synchronization
- websocket lifecycle management

---

## Seguridad

- CSRF aún pendiente
- hardening uploads parcial
- revocación avanzada pendiente

---

# Prioridades estratégicas actuales

## Prioridad Alta

1. Testing real
2. Seguridad avanzada
3. Realtime hardening
4. DevOps base
5. Observabilidad

---

## Prioridad Media

1. Students module
2. Inventory system
3. Competitions module
4. Analytics

---

## Prioridad Baja

1. IA operacional
2. Automatización avanzada
3. Integraciones institucionales complejas

---

# Filosofía de evolución

La plataforma evoluciona siguiendo principios de:

- arquitectura modular,
- seguridad primero,
- reutilización,
- escalabilidad,
- mantenibilidad,
- UX enterprise,
- realtime collaboration,
- evolución incremental sostenible.

---

# Estado estratégico actual

El proyecto ya ha superado ampliamente el nivel de:

- CRUD académico,
- proyecto demo,
- panel administrativo básico.

Actualmente evoluciona hacia una:

- enterprise educational platform,
- realtime operations console,
- modular robotics management platform.