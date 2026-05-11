# 10_CHANGELOG.md

## 🧠 Propósito

Este documento registra los cambios relevantes del proyecto:

* Nuevas funcionalidades
* Refactorizaciones
* Cambios en modelo de datos
* Mejoras de seguridad
* Correcciones de errores

Permite:

* Trazabilidad técnica
* Seguimiento de evolución
* Preparación para versiones
* Comunicación clara de cambios

---

## 📌 Formato

Se utiliza el siguiente esquema:

* **Added** → nuevas funcionalidades
* **Changed** → cambios en comportamiento existente
* **Fixed** → bugs corregidos
* **Refactored** → mejoras internas sin cambio funcional
* **Security** → mejoras de seguridad

---

# 🚀 [Unreleased]

## 🔥 Added

### Módulo de gestión de proyectos (base)

* Implementación inicial de:

  * Projects
  * Tasks
  * Activities
* Integración en panel administrativo
* CRUD básico en UI

---

### Testing y calidad

* Introducción de tests con cobertura (~85%)
* Integración de linter en CI
* Configuración de SonarQube Cloud
* Gate de calidad en GitHub Actions

---

## ⚙️ Changed

### Evolución de arquitectura

* Paso de API pura a sistema híbrido:

  * API REST
  * Render server-side con Jinja2
* Introducción de módulos funcionales más allá de IAM

---

### UI administrativa

* Mejora de layouts
* Uso extensivo de macros Jinja2
* Sidebar dinámico basado en permisos

---

## ♻️ Refactored

### Templates

* Componentización de:

  * tablas
  * botones
  * layouts
* Reutilización de componentes

---

### Backend

* Separación progresiva de lógica en servicios
* Limpieza parcial de routers
* Mejora de estructura modular

---

## 🐛 Fixed

* Errores en macros Jinja2 sin contexto
* Problemas en rutas dinámicas (`/form` vs `{id}`)
* Fallos en renderizado de menú dinámico
* Errores en relaciones ORM
* Problemas de alineación UI

---

## 🔐 Security

* Implementación de JWT con cookies HTTPOnly
* Separación access / refresh token
* RBAC con permisos granulares
* Protección de rutas backend

---

# 🏗️ [v0.1.0] — Núcleo IAM (Completado)

## Added

* Autenticación JWT
* Login / Logout
* Refresh token
* Middleware de autenticación

---

* Gestión de usuarios
* Gestión de roles
* Gestión de identidades

---

* Sistema RBAC completo
* Permisos granulares

---

* Auditoría de acciones

---

* Dashboard administrativo

---

* UI con AdminLTE

---

## Security

* Hash de contraseñas con bcrypt
* Cookies HTTPOnly
* Validación de permisos en backend

---

# 🧪 [v0.2.0] — Mejora estructural y UI

## Added

* Componentes reutilizables en Jinja2
* Menú dinámico por permisos
* Sistema de contexto global en templates

---

## Changed

* Mejora de UX en panel administrativo
* Navegación más coherente

---

## Refactored

* Limpieza de templates
* Reorganización de estructura frontend

---

# 🚧 [v0.3.0] — Módulo de Proyectos (En progreso)

## Added

* Modelo inicial de proyectos
* Modelo de tareas
* Modelo de actividades

---

* CRUD básico para:

  * projects
  * tasks
  * activities

---

## Changed

* Expansión del sistema hacia lógica de negocio
* Inicio de transición IAM → plataforma operativa

---

## ⚠️ Known Limitations

* No existe `project_members`
* No existe `project_teams`
* Tasks sin asignación real (`assigned_to`)
* Sin modelo Kanban
* Permisos contextuales no implementados

---

# 🔮 Próxima versión (v0.4.0)

## Planned

### Backend

* Implementación de `project_members`
* Implementación de `project_teams`
* Roles contextuales (coordinator / member)

---

### Tasks

* Campo `assigned_to`
* Campo `status` (Kanban)

---

### Seguridad

* Validaciones por proyecto
* Helpers de permisos contextuales

---

### UI

* Mejora de templates
* Base de vista Kanban

---

### Testing

* Tests para nuevos módulos
* Tests de integración

---

# 🧭 Convención de versiones

Formato:
`MAJOR.MINOR.PATCH`

* MAJOR → cambios incompatibles
* MINOR → nuevas funcionalidades
* PATCH → correcciones

---

# 📌 Notas

* Este changelog debe actualizarse en cada iteración relevante
* Los cambios deben ser claros y concisos
* Evitar registrar cambios triviales

---

# 🚀 Estado actual

El proyecto se encuentra en:

👉 Transición de sistema IAM
➡️ Plataforma de gestión real

Con foco en:

* consolidación del módulo de proyectos
* mejora de arquitectura
* preparación para funcionalidades avanzadas

---

## [FEATURE] Timeline de Auditoría Realtime

### Añadido
- Timeline visual para auditoría de tareas
- Integración WebSocket en tiempo real
- Actualización dinámica del timeline
- Agrupación por:
  - Hoy
  - Ayer
  - Fecha

### Mejoras UX
- Iconos por acción
- Colores por tipo de evento
- Inserción dinámica sin recarga
- Prevención de duplicados de etiquetas

### Arquitectura
- Centralización de auditoría global
- Emisión desacoplada mediante `emit_project_event()`