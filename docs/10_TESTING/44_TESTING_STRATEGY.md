# 44_TESTING_STRATEGY.md

# Testing Strategy

## Objetivo

Este documento describe la estrategia global de testing de Aula Robótica Platform.

Actualmente el proyecto ya dispone de una arquitectura de testing bastante madura para una plataforma en evolución:

- pytest,
- FastAPI TestClient,
- fixtures reutilizables,
- base de datos aislada,
- testing RBAC,
- testing SSR,
- testing services,
- testing middleware,
- testing JWT,
- testing permisos,
- coverage gates,
- CI automatizado.

La estrategia actual prioriza:

```text
seguridad + estabilidad + evolución segura
```

---

# Filosofía de Testing

La plataforma sigue una estrategia:

```text
backend-first testing
```

---

# Prioridades actuales

## Seguridad

Validar:

- JWT,
- middleware,
- permisos,
- RBAC,
- ownership,
- sesiones.

---

## Arquitectura SSR

Validar:

- rutas web,
- formularios,
- redirecciones,
- render contextual.

---

## Service Layer

Validar:

- lógica negocio,
- sincronización,
- validaciones,
- helpers.

---

## Realtime (fase actual)

Actualmente:

```text
sin cobertura automática formal
```

aunque la arquitectura ya está preparada para evolucionar.

---

# Stack Actual

# Framework Principal

```text
pytest
```

:contentReference[oaicite:0]{index=0}

---

# Cliente HTTP

```python
FastAPI TestClient
```

:contentReference[oaicite:1]{index=1}

---

# Database Strategy

# SQLite in-memory

Los tests usan:

```python
sqlite://
```

con:

```python
StaticPool
```

:contentReference[oaicite:2]{index=2}

---

# Beneficios

- velocidad,
- aislamiento,
- reproducibilidad.

---

# Dependency Override

Los tests sobrescriben:

```python
get_db
```

mediante:

```python
app.dependency_overrides
```

:contentReference[oaicite:3]{index=3}

---

# Reset Strategy

Cada test reinicia:

```python
drop_all()
create_all()
```

:contentReference[oaicite:4]{index=4}

---

# Seed Strategy

La suite incluye datos base:

- usuarios,
- roles,
- permisos,
- identidades,
- SAML fake.

:contentReference[oaicite:5]{index=5}

---

# Arquitectura de Cobertura

# Core Security

Cobertura muy fuerte actualmente.

Incluye:

- JWT,
- refresh,
- auth middleware,
- login/logout,
- permisos.



---

# RBAC / Authorization

Cobertura sólida:

- roles,
- permisos,
- ownership,
- autorización contextual.



---

# Services

Cobertura importante:

- users,
- roles,
- auth,
- menus.



---

# SSR Web Routes

Actualmente existe testing SSR sobre:

- login,
- users,
- roles,
- identities,
- dashboard.



---

# Context Injection

Existe cobertura sobre:

- breadcrumbs,
- menus,
- flash,
- helpers.

:contentReference[oaicite:10]{index=10}

---

# Middleware Coverage

Cobertura avanzada sobre:

- JWT invalid,
- refresh flow,
- redirect behavior,
- protected routes.



---

# Filosofía Arquitectónica

# Testing desacoplado

Los tests priorizan:

```text
services
middlewares
helpers
```

sobre testing E2E pesado.

---

# Beneficios

- velocidad,
- mantenibilidad,
- menor fragilidad.

---

# Testing Pyramid

# Base fuerte

## Unit Tests

Actualmente predominantes.

---

# Integration Tests

Parcialmente implementados mediante:

```python
TestClient
```

---

# E2E Tests

Actualmente inexistentes.

---

# Frontend Testing

Actualmente parcial y centrado indirectamente en SSR.

---

# Realtime Testing

Actualmente:

```text
muy limitado
```

tras el gran refactor realtime reciente.

---

# CI Integration

La estrategia se integra con:

- GitHub Actions,
- coverage gates,
- SonarCloud.

---

# Coverage Philosophy

El proyecto usa:

```text
coverage como quality gate
```

NO como métrica vanity.

---

# Testing Security-first

Gran parte de la estrategia actual gira alrededor de:

- autenticación,
- autorización,
- ownership,
- RBAC.

---

# Testing Patterns

# Monkeypatching

Uso frecuente de:

```python
monkeypatch
```

para aislar dependencias.



---

# Fake Payloads

Uso de payloads simulados JWT.

---

# Fixtures reutilizables

Especialmente:

```python
client
db
seed_data
```

:contentReference[oaicite:13]{index=13}

---

# Gaps Actuales

## 1. Sin tests WebSocket reales

Actualmente no existen.

---

## 2. Frontend JS testing inexistente

No hay:

- Jest,
- Playwright,
- Vitest.

---

## 3. Sin E2E browser testing

No existen tests navegador completos.

---

## 4. Cobertura realtime limitada

Dashboard/Kanban aún poco cubiertos.

---

## 5. Attachments poco cubiertos

Necesita más testing.

---

# Roadmap Testing

# Corto plazo

- ampliar services,
- ampliar SSR,
- tests dashboard,
- tests attachments.

---

# Medio plazo

- WebSocket testing,
- realtime integration tests,
- JS modular testing.

---

# Largo plazo

- Playwright,
- E2E enterprise,
- load testing,
- realtime stress testing.

---

# Objetivo Estratégico

La visión futura es evolucionar hacia:

```text
Enterprise-grade Realtime Testing Architecture
```

---

# Relación con otros documentos

Relacionado con:

- `43_TESTING_STATUS.md`
- `45_UI_TESTING.md`
- `46_REALTIME_TESTING.md`
- `39_CI_CD.md`
- `41_GITHUB_ACTIONS.md`

---

# Conclusión

Aunque todavía en evolución, el proyecto ya dispone de una estrategia de testing sorprendentemente sólida.

Especialmente destacan:

- testing seguridad,
- testing SSR,
- testing RBAC,
- testing middleware,
- testing services,
- integración CI,
- coverage gates.

La siguiente gran evolución será:

```text
realtime + frontend testing maturity
```