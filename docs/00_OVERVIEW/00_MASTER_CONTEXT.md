# 00_MASTER_CONTEXT.md

# Aula Robótica Platform

## 🧠 Identidad del Proyecto

**Nombre del proyecto:** Aula Robótica Platform  
**Tipo:** Plataforma administrativa y colaborativa enterprise-style basada en SSR  
**Dominio:** Aula de Robótica / Universidad / Gestión técnica y académica  
**Arquitectura:** Plataforma modular SSR con capacidades realtime  
**Estado actual:** Desarrollo avanzado activo

---

# 🎯 Visión Principal

Aula Robótica Platform tiene como objetivo evolucionar hacia una plataforma modular completa para:

- gestión de identidades y accesos
- gestión colaborativa de proyectos
- operaciones académicas y técnicas
- trazabilidad y auditoría
- sincronización realtime
- integraciones futuras con ecosistemas universitarios

El proyecto comenzó como una plataforma IAM/RBAC y ha evolucionado progresivamente hacia un sistema operativo moderno inspirado en plataformas internas enterprise.

---

# 🏗️ Filosofía Arquitectónica

La plataforma sigue varios principios fundamentales.

---

## 1. Seguridad backend-first

Toda validación y autorización real debe ocurrir en backend.

La lógica frontend nunca se considera confiable.

---

## 2. Arquitectura SSR-first

El sistema está construido principalmente alrededor de:

- FastAPI
- Jinja2
- renderizado server-side
- macros reutilizables

En lugar de una arquitectura SPA-first.

Esto permite:

- menor complejidad frontend
- mejor mantenibilidad
- límites de seguridad claros
- renderizado robusto
- mejor trazabilidad

---

## 3. Arquitectura UI reutilizable

El frontend está diseñado alrededor de patrones reutilizables:

- macros
- row components
- layouts reutilizables
- dialogs centralizados
- sistema toast centralizado
- sistemas de acciones reutilizables

Objetivo:

👉 eliminar duplicación al máximo.

---

## 4. Arquitectura modular por dominios

Cada módulo posee:

- modelos
- routers
- servicios
- schemas
- templates
- JavaScript asociado

Ejemplos:

- users
- roles
- identities
- projects
- tasks
- activities
- audit
- notifications

---

## 5. Seguridad por diseño

La seguridad es una capa arquitectónica central.

Actualmente implementado:

- JWT
- refresh tokens
- cookies HTTPOnly
- RBAC
- permisos contextuales
- auditoría
- aislamiento websocket

Pendiente:

- protección CSRF
- motor avanzado de policies

---

# ⚙️ Stack Tecnológico Actual

## Backend

- Python
- FastAPI
- SQLAlchemy
- MariaDB
- Pydantic
- WebSockets

---

## Frontend

- Jinja2
- Bootstrap
- AdminLTE
- JavaScript
- Chart.js
- Font Awesome

---

## Calidad y DevOps

- pytest
- pytest-cov
- Ruff
- GitHub Actions
- SonarCloud
- uv

---

# 🔐 Arquitectura de Seguridad

## Autenticación

Implementada mediante:

- JWT access tokens
- refresh tokens
- cookies seguras HTTPOnly
- middleware de validación

---

## Autorización

Existen dos niveles principales.

### RBAC global

Ejemplos:

- admin
- profesor
- estudiante

---

### Permisos contextuales

Ejemplos:

- coordinador de proyecto
- ownership de recursos
- ownership de tareas

---

## Auditoría

Las operaciones importantes generan:

- logs de auditoría
- timeline events
- notificaciones
- actualizaciones realtime

---

# 🧩 Áreas Funcionales Principales

## Sistema IAM

Incluye:

- users
- identities
- roles
- permissions
- audit logging

Es actualmente la parte más madura de la plataforma.

---

## Gestión de Proyectos

Soporta:

- proyectos
- miembros
- tareas
- actividades
- adjuntos

La arquitectura ya está preparada para:

- Kanban
- colaboración realtime
- notificaciones

---

## Dashboard Administrativo

El dashboard actual incluye:

- métricas del sistema
- estadísticas operativas
- resúmenes de actividad
- gráficas dinámicas
- resúmenes de auditoría

---

## Sistema de Actividad y Auditoría

Una de las áreas más sólidas arquitectónicamente.

Incluye:

- timelines
- auditoría visual
- realtime updates
- renderizado contextual
- indicadores visuales de estado

---

## Sistema de Adjuntos

Las actividades soportan adjuntos con:

- subida segura
- eliminación controlada
- metadatos
- trazabilidad del uploader
- persistencia filesystem

---

# 🎨 Filosofía Frontend/UI

La UI sigue un enfoque tipo:

👉 “enterprise admin platform”

Objetivos:

- claridad
- consistencia
- mantenibilidad
- reutilización visual

---

# 🧱 Sistemas UI Importantes

## Sistema Toast

Renderizado custom de flash messages con:

- success
- error
- warning
- info

Integrado con sesiones.

---

## Sistema de Confirm Dialogs

Los `confirm()` nativos están siendo reemplazados por:

- dialogs reutilizables
- handlers JS centralizados
- formularios confirmables reutilizables

---

## Sistema de Detail Layouts

Las páginas detail utilizan patrones reutilizables:

- paneles laterales
- metadata cards
- timelines
- actions sections
- attachments sections

---

# 🔄 Arquitectura Realtime

La plataforma ya incluye infraestructura realtime mediante WebSockets.

Usos actuales:

- notificaciones
- dashboard sync
- timelines dinámicos

Usos futuros:

- Kanban live sync
- presencia de usuarios
- colaboración en vivo

---

# 🧪 Filosofía de Testing

El testing se considera una prioridad arquitectónica.

Foco actual:

- testing backend
- testing de servicios
- permisos
- autenticación
- routers

Objetivo de cobertura:

```text
>= 85%
```

Objetivo futuro:

```text
90%+
```
---

# 📊 Evaluación Actual de Madurez

## Muy maduros
- IAM
- arquitectura SSR
- sistema reusable de templates
- RBAC
- dashboard
- auditoría
- workflows de actividades

## Maduros pero evolucionando
- realtime
- permisos contextuales
- attachments
- arquitectura UI

## Todavía evolucionando
- Teams
- notifications
- Kanban UX
- CSRF
- robustez websocket

# 🚀 Visión a Largo Plazo
El objetivo a largo plazo es transformar **Aula Robótica Platform** en un ecosistema universitario completo.

### Posibles módulos futuros:
- inventario
- reservas
- dispositivos robóticos
- gestión de laboratorios
- SSO/SAML
- coordinación académica
- reporting
- workflows asistidos por IA

# 📌 Filosofía de Desarrollo
El proyecto prioriza:
- calidad arquitectónica
- mantenibilidad
- seguridad
- modularidad
- evolución progresiva

**Por encima de:**
- sobreingeniería
- complejidad innecesaria
- dependencia excesiva frontend

# 🧠 Decisiones Arquitectónicas Importantes
*Elegidas deliberadamente*

### SSR sobre SPA
Por mantenibilidad y seguridad.

### Macros reutilizables Jinja2
Para reducir duplicación.

### RBAC + permisos contextuales
Para soportar workflows enterprise-style.

### Separación Router → Service
Para aislar lógica de negocio.

### Introducción progresiva de WebSockets
Para evitar complejidad prematura.

# 📁 Estructura General del Proyecto
```text
app/
├── core/
├── modules/
├── templates/
├── static/
├── websocket/
├── middleware/
├── services/
└── tests/
'''

## 📌 Prioridades Estratégicas Actuales

### Alta prioridad
- protección CSRF
- hardening de permisos contextuales
- resiliencia websocket
- testing realtime
- sistema de notificaciones

### Prioridad media
- Kanban avanzado
- módulo Teams
- versionado API
- dockerización

### Largo plazo
- SAML/SSO
- multi-tenant
- observabilidad avanzada
- integraciones IA

---

## 🏁 Resumen
Aula Robótica Platform ya no es únicamente un proyecto IAM.

Ha evolucionado hacia:
👉 **una plataforma colaborativa SSR modular enterprise-style**

**Centrada en:**
- seguridad
- operaciones realtime
- arquitectura reutilizable
- trazabilidad
- mantenibilidad
- escalabilidad progresiva

*Manteniendo siempre una complejidad razonable y controlada.*