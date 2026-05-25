# 40_DOCKER.md

# Docker Architecture

## Objetivo

Este documento describe la estrategia futura de containerización de Aula Robótica Platform.

Actualmente Docker todavía NO está implementado, pero la arquitectura ya está siendo diseñada para evolucionar hacia:

```text
Containerized Realtime Platform
```

---

# Estado Actual

# Situación actual

Actualmente:

```text
No existe Docker
```

---

# Runtime actual

La plataforma se ejecuta mediante:

```text
uv
uvicorn
```

en entorno local.

---

# Arquitectura actual

```text
FastAPI
+
MariaDB
+
Static SSR
+
WebSockets
+
uv runtime
```

---

# Filosofía Docker

Docker no se plantea únicamente para despliegue.

También busca:

- reproducibilidad,
- aislamiento,
- onboarding rápido,
- consistencia entornos,
- CI/CD,
- escalabilidad futura.

---

# Objetivos de Containerización

# 1. Desarrollo reproducible

Todos los desarrolladores ejecutando:

```text
mismo entorno
```

---

# 2. Despliegue consistente

Evitar diferencias:

```text
works on my machine
```

---

# 3. Escalabilidad futura

Preparar:

- staging,
- producción,
- CI/CD,
- cloud deployment.

---

# 4. Realtime-ready deployment

Preparar despliegue estable para:

- WebSockets,
- dashboard realtime,
- notifications,
- activity feeds.

---

# Arquitectura Objetivo

# Container principal

## FastAPI App

```text
FastAPI
uvicorn
SSR templates
WebSockets
```

---

# Database Container

## MariaDB

Persistencia separada.

---

# Posibles servicios futuros

## Redis

Para:

- websocket scaling,
- pub/sub,
- cache,
- realtime coordination.

---

## Nginx

Como:

- reverse proxy,
- static serving,
- websocket proxy.

---

# Arquitectura prevista

```text
Nginx
   ↓
FastAPI Container
   ↓
MariaDB Container
```

---

# Docker Compose Futuro

# Objetivo

Orquestar:

- app,
- db,
- networking,
- volumes,
- environment variables.

---

# Volúmenes previstos

## Database

Persistencia MariaDB.

---

## Attachments

Persistencia:

```text
storage/activity_attachments/
```

---

# Networking

# WebSocket Support

La arquitectura Docker deberá soportar:

```text
Upgrade
Connection
WebSocket proxy
```

---

# Realtime Considerations

Importante para:

- dashboard live,
- notifications,
- project rooms,
- activity feeds.

---

# Variables de Entorno

Docker integrará:

```text
.env
```

---

# Variables previstas

- DATABASE_URL
- SECRET_KEY
- DEBUG
- ENV
- app_base_url
- SAML config

---

# Build Strategy

# Imagen Python moderna

Posible base:

```text
python:3.12-slim
```

---

# Dependency Strategy

Compatibilidad con:

```text
uv
pyproject.toml
uv.lock
```

---

# Beneficios esperados

# Desarrollo

- onboarding rápido,
- consistencia.

---

# DevOps

- CI/CD,
- staging,
- despliegues repetibles.

---

# Producción

- aislamiento,
- escalabilidad,
- mantenimiento.

---

# Riesgos y Desafíos

# WebSockets

Necesidad de configuración correcta reverse proxy.

---

# Volúmenes persistentes

Especialmente para:

```text
attachments
```

---

# Realtime scaling

En futuro multiworker probablemente requerirá:

```text
Redis pub/sub
```

---

# Estado Arquitectónico

Actualmente Docker es:

```text
planned architecture
```

NO implementación activa.

---

# Roadmap Docker

# Corto plazo

- Dockerfile básico,
- docker-compose.dev,
- MariaDB container.

---

# Medio plazo

- Nginx reverse proxy,
- websocket support,
- staging deployment.

---

# Largo plazo

- Kubernetes,
- autoscaling,
- distributed realtime,
- observability stack.

---

# Relación con otros documentos

Relacionado con:

- `39_CI_CD.md`
- `41_GITHUB_ACTIONS.md`
- `42_ENVIRONMENT.md`
- `36_MONITORING.md`
- `38_OBSERVABILITY.md`

---

# Conclusión

Aunque Docker todavía no existe en el proyecto, la arquitectura actual ya está claramente preparada para evolucionar hacia una plataforma containerizada moderna.

La combinación de:

- FastAPI modular,
- SSR,
- WebSockets,
- realtime,
- CI,
- uv,
- separación servicios,

facilitará enormemente la transición futura hacia:

```text
Containerized Realtime Enterprise Platform
```