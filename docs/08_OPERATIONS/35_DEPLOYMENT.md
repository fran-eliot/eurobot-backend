# 35_DEPLOYMENT.md

# 🚀 Estrategia de Despliegue

# 🎯 Propósito

Documento de referencia para:

- despliegue local,
- staging,
- producción,
- operación realtime,
- observabilidad,
- mantenimiento.

---

# 🏗️ Filosofía de Deployment

La plataforma está diseñada como:

```text
SSR Enterprise Administrative Platform
```
# Arquitectura y Despliegue
## Basada en:
* **FastAPI**
* **SSR con Jinja2**
* **WebSockets**
* **MariaDB**
* **Arquitectura modular**

# 🌍 Entornos

## Local Development
**Entorno de desarrollo diario.**
### Objetivos
* desarrollo rápido
* debugging
* hot reload
* testing funcional

### Tecnologías
* **uv**
* **Uvicorn**
* **MariaDB local**
* **FastAPI reload**

## Staging
**Entorno previo a producción.**
### Objetivos
* validación funcional
* pruebas realtime
* validación UI
* smoke tests

## Production
**Entorno real de usuarios.**
### Objetivos
* estabilidad
* seguridad
* observabilidad
* escalabilidad

# 📦 Stack de Deployment

| Componente | Tecnología |
| :--- | :--- |
| **Runtime** | Python 3.12+ |
| **Package Manager** | uv |
| **ASGI** | Uvicorn |
| **Reverse Proxy** | Nginx |
| **Database** | MariaDB |
| **Realtime** | WebSockets |
| **CI/CD** | GitHub Actions |
| **Calidad** | SonarCloud |

# 🧰 Requisitos mínimos

### Backend
* Python 3.12+
* **uv**
* MariaDB
* Git

### Recomendado
* Linux server
* Nginx
* HTTPS
* **systemd**
* **Fail2ban**

# 🧪 Desarrollo Local

### 1. Clonar repositorio
```bash
git clone [https://github.com/fran-eliot/aula-robotica-platform](https://github.com/fran-eliot/aula-robotica-platform)
cd aula-robotica-platform
```
### Instalar dependencias
**Recomendado: uv**
```bash
uv sync
```

### Alternativa legacy
```bash
pip install -r requirements.txt
```

### Variables de entorno
```bash
.env
```

### Ejemplo
```bash
SECRET_KEY=change_me
DATABASE_URL=mysql+pymysql://user:pass@localhost/db

ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

DEBUG=True
```

### Ejecutar aplicación
```bash
uv run uvicorn app.main:app --reload
```

# 🏗️ Arquitectura Producción

## Arquitectura recomendada
```text
Internet
   │
   ▼
Nginx Reverse Proxy
   │
   ├── Static Files
   ├── HTTPS
   ├── WebSocket Upgrade
   │
   ▼
Gunicorn + Uvicorn Workers
   │
   ▼
FastAPI SSR Platform
   │
   ▼
MariaDB
```

## 🌐 Nginx

### Responsabilidades
* **reverse proxy**
* **HTTPS**
* **static serving**
* **websocket proxy**
* **gzip**
* **security headers**
* **buffering**

---

### Static Files
**Servidos directamente por Nginx**

**Ejemplos:**
* `/static/css`
* `/static/js`
* `/static/uploads`

**Beneficios:**
* menor carga ASGI
* mejor rendimiento
* cache frontend
* menor latencia

---

## 🔌 WebSockets en Producción
> **Muy importante**  

La plataforma usa:
* dashboard realtime
* notifications websocket
* audit timeline realtime

### Ngix debe soportar
```ngix
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
```

### Timeout recomendado
```text
proxy_read_timeout 3600;
```

### Problemas típicos
| Problema | Causa |
| :--- | :--- |
| **desconexiones** | timeout |
| **reconnect infinito** | proxy mal configurado |
| **websocket 400** | upgrade headers ausentes |

---

### Gunicorn + Uvicorn
**Recomendado**

```bash
gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker \
  -w 4
  ```

  ### Workers
**Recomendación inicial**

| CPU | Workers |
| :--- | :--- |
| **2 cores** | 2-4 |
| **4 cores** | 4-8 |

> [!WARNING]
> **⚠️ Nota Realtime**  
> Muchos workers pueden requerir **shared websocket state** en el futuro.

**Futuro recomendado**
* Redis Pub/Sub
* event bus
* distributed websocket layer

---

### 🔐 Seguridad Producción
**HTTPS obligatorio**
* **Recomendado:** Let's Encrypt / Certbot

**Cookies seguras (JWT Cookies)**
Configurar:
* `HttpOnly`
* `Secure`
* `SameSite`

**SessionMiddleware**
La plataforma usa `SessionMiddleware` para:
* flash messages
* SSR session state

**Configuración recomendada**
```python
https_only=True
same_site="lax"
```

Variables sensibles
Nunca subir
.env
SECRET_KEY
DATABASE_URL real
credenciales admin
tokens
Recomendado

Usar:

variables entorno,
secret managers,
CI secrets.
🧾 Logging
Arquitectura actual

La plataforma ya dispone de:

audit logs,
access logs,
error logs,
eventos realtime.
Recomendado producción
Backend
structured logging,
rotating logs,
JSON logs futuros.
Nginx
access.log
error.log
Logs importantes
Tipo	Estado
Audit	✔
Errors	✔
Access	✔
Realtime events	⚠️ parcial
Metrics	🚧 futuro
📊 Observabilidad
Recomendado
Monitorización
uptime,
CPU,
RAM,
websocket connections,
DB latency,
response times.
Herramientas posibles
Herramienta	Uso
Grafana	métricas
Prometheus	monitoring
Sentry	errores
UptimeRobot	uptime
🧪 CI/CD
Estado actual
GitHub Actions

✔ Integrado

SonarCloud

✔ Integrado

Pipeline actual
``Lint
→ Tests
→ Quality Gates`
```

Pipeline futuro
```text
Tests
→ Lint
→ SonarCloud
→ Build
→ Deploy Staging
→ Smoke Tests
→ Deploy Production
```

### 🗄️ Base de Datos

**Motor actual**
* MariaDB

---

**Backup recomendado**
* **Frecuencia:** Diario
* **Comando:**
  ```bash
  mysqldump db > backup.sql
  ```
### 📂 Storage
**Estado actual**
* **Attachments:** ✔ almacenamiento local.
* **Ruta típica:** `storage/activity_attachments/`

**Futuro recomendado**
* S3 / MinIO
* Object storage
* CDN

---

### 🐳 Docker
**Estado:** 🚧 Pendiente.
**Objetivo futuro:** `docker-compose`

**Servicios previstos**
| Servicio | Función |
| :--- | :--- |
| **app** | FastAPI |
| **db** | MariaDB |
| **nginx** | reverse proxy |
| **redis** | realtime/event bus |

---

### ☸️ Escalabilidad futura
**Posibles evoluciones**
* Redis cache
* Distributed websocket layer
* Background workers / Async jobs
* PostgreSQL
* Kubernetes

---

### ⚠️ Riesgos actuales
| Riesgo | Estado |
| :--- | :--- |
| **WebSocket reconnect** | pendiente |
| **Shared websocket state** | pendiente |
| **CSRF** | pendiente |
| **Distributed realtime** | pendiente |
| **Cache invalidation** | parcial |

---

### ✅ Checklist Producción

#### Seguridad
- [ ] HTTPS activo
- [ ] `DEBUG=False`
- [ ] `SECRET_KEY` segura
- [ ] Cookies seguras
- [ ] Firewall / Fail2ban

#### Backend
- [ ] Gunicorn configurado
- [ ] Workers optimizados
- [ ] Logs activos
- [ ] Backups activos

#### Realtime
- [ ] WebSocket proxy correcto
- [ ] Upgrade headers
- [ ] Reconnect strategy
- [ ] Timeouts ajustados

#### Observabilidad
- [ ] Monitoring
- [ ] Error tracking
- [ ] Uptime checks

---

### 🚀 Estado Actual del Deployment
| Área | Estado |
| :--- | :--- |
| **Desarrollo local** | ✔ Maduro |
| **SSR deployment** | ✔ Maduro |
| **Realtime básico** | ✔ Funcional |
| **Producción enterprise** | ⚠️ Parcial |
| **Docker** | 🚧 Futuro |
| **Escalabilidad horizontal** | 🚧 Futuro |

---

### 🎯 Conclusión
La plataforma ya soporta **despliegue SSR enterprise moderno**, incluyendo:
* FastAPI SSR
* Realtime websocket
* UI avanzada
* JWT cookies
* Auditoría / Notifications
* Attachments
* Arquitectura modular

> **El siguiente gran salto será:**  
> `distributed realtime architecture` + `cloud-native deployment`


