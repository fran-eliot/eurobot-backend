# 01_PROJECT_OVERVIEW.md

# Aula Robótica Platform

## 📌 Descripción General

Aula Robótica Platform es una plataforma web modular enterprise-style desarrollada para la gestión integral del Aula de Robótica de la Escuela Politécnica Superior de la Universidad de Alcalá.

El proyecto ha evolucionado desde un sistema inicial IAM/RBAC hacia una plataforma SSR colaborativa moderna orientada a:

- gestión académica
- gestión operativa
- coordinación de proyectos
- trazabilidad completa
- operaciones realtime
- administración centralizada

La arquitectura prioriza:

- seguridad backend-first
- renderizado server-side
- modularidad
- reutilización UI
- mantenibilidad
- escalabilidad progresiva

---

# 🏗️ Arquitectura General

La plataforma utiliza una arquitectura SSR (Server Side Rendering) basada en FastAPI + Jinja2 con enfoque enterprise admin platform.

## Stack principal

### Backend

- FastAPI
- SQLAlchemy
- MariaDB
- Pydantic
- WebSockets
- JWT Authentication

### Frontend

- Jinja2
- Bootstrap
- AdminLTE
- JavaScript modular
- Chart.js
- Font Awesome

---

# 🎯 Objetivos Principales

## Objetivos funcionales

- Gestión centralizada de usuarios
- Gestión de identidades
- Roles y permisos avanzados
- Gestión de proyectos colaborativos
- Gestión de tareas y actividades
- Timeline de actividad
- Sistema de adjuntos
- Notificaciones realtime
- Auditoría completa
- Dashboard administrativo

---

## Objetivos técnicos

- Arquitectura modular
- Seguridad por diseño
- Reutilización máxima UI
- SSR-first architecture
- Contextual authorization
- Escalabilidad progresiva
- Realtime synchronization
- Preparación para SSO/SAML
- Testing automatizado

---

# 🔐 Arquitectura de Seguridad

La seguridad es uno de los pilares fundamentales del sistema.

## Autenticación

Actualmente implementado:

- JWT access tokens
- refresh tokens
- cookies HTTPOnly
- middleware de autenticación
- validación backend centralizada

---

## Autorización

La plataforma combina:

### RBAC global

Ejemplos:

- admin
- profesor
- estudiante

---

### Permisos contextuales

El sistema soporta autorización dinámica basada en contexto:

- ownership de recursos
- coordinadores de proyecto
- permisos por entidad
- validaciones condicionales

---

## Seguridad UI contextual

La interfaz se adapta dinámicamente según permisos del usuario:

- acciones visibles/invisibles
- menús dinámicos
- botones protegidos
- acciones contextuales
- renderizado condicional SSR

---

# 🧩 Sistemas Funcionales Principales

# IAM / RBAC

El núcleo IAM incluye:

- users
- identities
- roles
- permissions
- policies
- auditoría de accesos

Es actualmente uno de los módulos más maduros del proyecto.

---

# Gestión de Proyectos

La plataforma soporta:

- proyectos colaborativos
- miembros
- coordinadores
- tareas
- actividades
- timelines

La arquitectura ya está preparada para evolución tipo:

- Kanban avanzado
- realtime collaboration
- dashboards operativos

---

# Gestión de Actividades

Cada actividad puede incluir:

- estado
- horas invertidas
- usuario responsable
- trazabilidad
- archivos adjuntos

El sistema de actividades es uno de los núcleos operativos principales.

---

# Sistema de Adjuntos

Las actividades soportan subida y gestión de archivos:

- almacenamiento filesystem
- metadatos persistentes
- subida segura
- eliminación controlada
- ownership tracking

Actualmente integrado completamente en SSR.

---

# Sistema de Auditoría

Toda acción importante genera trazabilidad.

Incluye:

- audit logs
- timelines visuales
- historial de acciones
- metadata contextual
- información de usuario
- timestamps completos

---

# Timeline Realtime

La plataforma ya incorpora capacidades realtime mediante WebSockets.

Actualmente se utilizan para:

- notificaciones
- dashboard sync
- timelines dinámicos
- actualización parcial UI

La arquitectura está preparada para:

- colaboración en vivo
- presencia de usuarios
- Kanban realtime

---

# 🔔 Sistema de Notificaciones

El sistema de notificaciones soporta:

- notificaciones persistentes
- unread counters
- actualización realtime
- renderizado SSR
- integración websocket

Actualmente ya existe infraestructura backend y frontend funcional.

---

# 🎨 Arquitectura UI Reutilizable

Uno de los pilares actuales del proyecto es la reutilización visual y estructural.

---

## Sistema de macros reutilizables

La UI utiliza macros Jinja2 reutilizables para:

- tablas
- badges
- botones
- filas
- layouts
- acciones

---

## Reusable Row Components

Se utilizan componentes parciales reutilizables:

- activity_row
- task_row
- project_row
- notification_row

---

## Reusable Dialog System

Los antiguos `confirm()` nativos han sido reemplazados progresivamente por:

- dialogs reutilizables
- confirm handlers centralizados
- atributos data-confirm
- UX consistente

---

## Sistema Toast Centralizado

La plataforma utiliza un sistema moderno de toast notifications para:

- success
- error
- warning
- info

Características:

- renderizado SSR
- autoclose
- integración con flash messages
- persistencia controlada
- limpieza automática de sesión

---

# 📊 Dashboard Administrativo

El dashboard actual incluye:

- métricas globales
- estadísticas operativas
- actividad reciente
- timelines
- indicadores visuales
- gráficas Chart.js
- auditoría reciente

---

# 🧪 Testing y Calidad

La plataforma incorpora:

- pytest
- pytest-cov
- Ruff
- GitHub Actions
- SonarCloud

Objetivos actuales:

- aumentar cobertura
- robustecer realtime
- validar permisos contextuales

---

# 📈 Estado Actual del Proyecto

## Muy maduros

- IAM
- RBAC
- arquitectura SSR
- reusable UI
- auditoría
- dashboard
- activities workflow

---

## Maduros

- notifications
- realtime
- attachment system
- contextual authorization
- toast/dialog systems

---

## En evolución

- Kanban avanzado
- Teams
- CSRF protection
- SAML/SSO
- observabilidad avanzada

---

# 🚀 Roadmap Futuro

## Corto plazo

- hardening de seguridad
- mejora realtime
- testing avanzado
- optimización UI reusable

---

## Medio plazo

- SSO/SAML
- dashboards avanzados
- colaboración realtime avanzada
- Dockerización

---

## Largo plazo

- multi-tenant
- IA aplicada
- integración universitaria
- workflows inteligentes

---

# 🏁 Resumen

Aula Robótica Platform ha evolucionado hacia una plataforma SSR enterprise-style moderna centrada en:

- seguridad
- mantenibilidad
- trazabilidad
- realtime
- reutilización
- modularidad

manteniendo una arquitectura coherente, escalable y preparada para crecimiento progresivo.