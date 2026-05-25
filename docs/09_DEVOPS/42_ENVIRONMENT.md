# 42_ENVIRONMENT.md

# Environment Architecture

## Objetivo

Este documento describe la arquitectura de configuración y entornos de Aula Robótica Platform.

Actualmente la plataforma utiliza una estrategia basada en:

- `.env`,
- `pydantic-settings`,
- runtime configurable,
- separación de secretos,
- configuración desacoplada.

---

# Filosofía

La configuración debe ser:

- desacoplada,
- portable,
- segura,
- reproducible,
- preparada para múltiples entornos.

---

# Arquitectura Actual

# Configuración centralizada

Archivo principal:

```text
app/core/config.py
```

:contentReference[oaicite:0]{index=0}

---

# Tecnología usada

```python
pydantic-settings
```

---

# Beneficios

- tipado,
- validación,
- defaults,
- integración `.env`.

---

# Variables Actuales

# Database

```text
DATABASE_URL
```

---

# Seguridad

```text
SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES
```

---

# Runtime

```text
DEBUG
ENV
```

---

# Application

```text
app_base_url
```

---

# SAML

```text
saml_entity_id
saml_acs_url
saml_metadata_url
```

:contentReference[oaicite:1]{index=1}

---

# Entornos Actuales

# Development

Actualmente el proyecto opera principalmente en:

```text
development environment
```

---

# Variables actuales

```python
DEBUG = True
ENV = "dev"
```

:contentReference[oaicite:2]{index=2}

---

# Runtime Actual

# FastAPI

La aplicación se inicializa desde:

```text
app/main.py
```

:contentReference[oaicite:3]{index=3}

---

# Runtime stack

```text
FastAPI
uvicorn
uv
MariaDB
SSR
WebSockets
```

---

# Middleware Stack

Actualmente:

## SessionMiddleware

```python
SessionMiddleware
```

---

## AuthMiddleware

```python
AuthMiddleware
```

:contentReference[oaicite:4]{index=4}

---

# Arquitectura SSR

La app integra:

- templates,
- static files,
- websockets,
- realtime.

:contentReference[oaicite:5]{index=5}

---

# Variables Sensibles

# SECRET_KEY

Usada para:

- JWT,
- sesiones,
- cookies.

---

# DATABASE_URL

Controla conexión MariaDB.

---

# Filosofía Seguridad

Los secretos NO deben hardcodearse.

---

# .env Strategy

El sistema usa:

```python
env_file=".env"
```

:contentReference[oaicite:6]{index=6}

---

# Beneficios

- separación config/código,
- seguridad,
- multi-entorno,
- despliegue portable.

---

# SAML Environment

La arquitectura ya está preparada para:

```text
SAML
SSO
OAuth future
```

---

# Variables SAML

```text
saml_entity_id
saml_acs_url
saml_metadata_url
```

:contentReference[oaicite:7]{index=7}

---

# Filosofía Evolutiva

Actualmente muchas variables están orientadas a:

```text
development-first
```

pero la arquitectura ya está preparada para:

```text
enterprise deployment
```

---

# Futuros Entornos

# Development

Local development.

---

# Staging

Testing integración.

---

# Production

Despliegue institucional.

---

# Docker Integration Futura

La arquitectura `.env` facilitará:

```text
Docker
Docker Compose
Kubernetes Secrets
```

---

# Variables Futuras Previstas

# Monitoring

```text
LOG_LEVEL
METRICS_ENABLED
```

---

# Observability

```text
SENTRY_DSN
OTEL_ENDPOINT
```

---

# Realtime

```text
REDIS_URL
WS_HEARTBEAT_INTERVAL
```

---

# Security

```text
COOKIE_SECURE
JWT_ROTATION
```

---

# Riesgos Actuales

## 1. DEBUG=True

Actualmente orientado solo a desarrollo.

---

## 2. Single environment

No existe separación real:

- dev,
- staging,
- prod.

---

## 3. Secret management básico

No existe vault/secrets manager.

---

## 4. Runtime local-only

No existe despliegue distribuido.

---

# Arquitectura Objetivo

# Multi-environment

Objetivo futuro:

```text
dev
staging
production
```

---

# Container-ready

Variables preparadas para:

- Docker,
- Kubernetes,
- cloud deployment.

---

# Security-first

Separación estricta:

- secrets,
- runtime,
- feature flags.

---

# Observability-ready

Preparado para:

- metrics,
- tracing,
- monitoring.

---

# Valor Arquitectónico

Aunque todavía simple, la arquitectura de entorno ya posee bases muy correctas:

- configuración desacoplada,
- tipado,
- variables entorno,
- SSR-ready,
- realtime-ready,
- SAML-ready.

---

# Relación con otros documentos

Relacionado con:

- `39_CI_CD.md`
- `40_DOCKER.md`
- `41_GITHUB_ACTIONS.md`
- `36_MONITORING.md`
- `38_OBSERVABILITY.md`
- `12_SAML_INTEGRATION.md`

---

# Conclusión

La plataforma ya posee una arquitectura de configuración moderna y extensible.

Actualmente permite:

- desacoplamiento entorno/código,
- configuración segura,
- soporte realtime,
- preparación SAML,
- evolución multi-entorno.

La siguiente gran evolución será:

```text
containerized multi-environment enterprise runtime
```