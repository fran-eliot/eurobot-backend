# 49_FEATURE_BACKLOG.md

# Feature Backlog

# Objetivo

Este documento define el backlog funcional y estratégico de Aula Robótica Platform.

El backlog refleja:

- prioridades reales,
- evolución arquitectónica,
- visión producto,
- deuda técnica,
- roadmap operativo.

---

# Filosofía del Backlog

La plataforma prioriza:

```text
arquitectura sólida
+
realtime collaboration
+
IAM institucional
```

sobre acumulación masiva de features.

---

# Prioridades Estratégicas

Actualmente las prioridades principales son:

# 1. IAM / SSO institucional

Máxima prioridad actual.

---

# 2. Realtime collaboration

Kanban, dashboards y actividad viva.

---

# 3. Escalabilidad arquitectónica

Preparación para crecimiento real.

---

# Feature Classification

El backlog se divide en:

- Critical,
- High Priority,
- Medium Priority,
- Long-term Vision,
- Explicitly Out-of-Scope.

---

# CRITICAL PRIORITY

# SAML Real UAH

## Estado

Parcialmente implementado con login fake actual.

---

# Objetivo

Integración institucional real.

---

# Incluye

- metadata real,
- provider real,
- atributos usuario,
- login institucional,
- provisioning automático.

---

# Impacto

Muy alto.

---

# Dependencias

- coordinación UAH,
- infraestructura institucional.

---

# HIGH PRIORITY

# Mejoras Kanban

## Objetivo

Convertir Kanban en sistema realtime mucho más robusto.

---

# Mejoras previstas

- optimistic UI madura,
- rollback realtime,
- drag visual mejorado,
- activity sync,
- avatars,
- locks visuales.

---

# Adjuntos Avanzados

## Objetivo

Evolucionar attachments hacia sistema documental más maduro.

---

# Posibles mejoras

- previews,
- thumbnails,
- drag & drop,
- uploads async,
- validación MIME,
- progress bars.

---

# Comentarios Realtime

## Objetivo

Añadir colaboración contextual.

---

# Incluye

- comentarios tareas,
- comentarios actividades,
- realtime updates,
- mentions futuras.

---

# Beneficios

- colaboración,
- coordinación,
- contexto operativo.

---

# MEDIUM PRIORITY

# Dashboard Analytics

Posibles mejoras:

- métricas históricas,
- tendencias,
- actividad temporal,
- analytics proyectos.

---

# Realtime Improvements

- reconnect avanzado,
- offline recovery,
- sync tabs,
- event deduplication.

---

# Notifications avanzadas

- prioridades,
- agrupación,
- filtros,
- preferencias usuario.

---

# Search System

Posible buscador global:

- tareas,
- proyectos,
- actividades,
- usuarios.

---

# Inventory System

Posible módulo:

- hardware,
- componentes,
- robots,
- préstamos.

---

# Competition Module

Posible evolución:

- equipos,
- torneos,
- resultados,
- métricas competición.

---

# LONG-TERM VISION

# Mobile Support

## Estado

Visión futura.

---

# Posibilidades

- responsive avanzado,
- PWA,
- app híbrida.

---

# Objetivo

Acceso rápido operativo móvil.

---

# Observability Platform

Futuro:

- métricas,
- tracing,
- analytics realtime.

---

# Multi-Aula Architecture

Posible soporte:

- múltiples laboratorios,
- múltiples equipos,
- múltiples espacios.

---

# AI / Intelligence

Posibles ideas futuras:

- analytics inteligentes,
- recomendaciones,
- detección anomalías.

---

# OUT OF SCOPE

# Chat tipo Discord

La plataforma NO busca convertirse en:

```text
chat persistente masivo
```

---

# Videoconferencia

No se pretende integrar:

- Zoom,
- Meet,
- Teams.

---

# LMS Completo

No se busca replicar:

- Moodle,
- Blackboard,
- LMS clásicos.

---

# Filosofía

La plataforma quiere mantenerse enfocada en:

```text
operación + colaboración + coordinación
```

---

# Technical Debt Backlog

# Frontend JS

- modularización,
- reducción JS inline,
- separación responsabilidades.

---

# Realtime Testing

- tests websocket,
- race conditions,
- stress testing.

---

# Observability

- monitoring,
- metrics,
- tracing.

---

# Docker / DevOps

- Docker,
- staging,
- deploy reproducible.

---

# Arquitectura Prioritaria

El backlog prioriza especialmente:

# Realtime

Elemento diferencial clave.

---

# IAM

Elemento institucional estratégico.

---

# Escalabilidad

Elemento arquitectónico fundamental.

---

# Filosofía Evolutiva

La plataforma evoluciona mediante:

```text
incremental architecture maturity
```

---

# Estrategia

Primero:

- arquitectura,
- seguridad,
- modularidad.

Después:

- features avanzadas,
- analytics,
- inteligencia operacional.

---

# Relación con otros documentos

Relacionado con:

- `47_PRODUCT_ROADMAP.md`
- `48_PRODUCT_VISION.md`
- `21_WEBSOCKET_SYSTEM.md`
- `33_DASHBOARD_MODULE.md`
- `38_OBSERVABILITY.md`

---

# Conclusión

El backlog actual refleja una evolución muy clara:

```text
de CRUD académico
→ hacia plataforma colaborativa realtime
```

Las prioridades más importantes actualmente son:

- SAML institucional,
- colaboración realtime,
- escalabilidad,
- madurez operativa.

El foco seguirá siendo:

```text
plataforma operativa colaborativa moderna
```

y no un LMS tradicional o una plataforma de comunicación masiva.