# 08_CURRENT_TASKS.md

## 🧠 Propósito

Este documento define el **estado actual del desarrollo** y las tareas activas del proyecto.

Sirve para:

* Priorizar trabajo
* Evitar pérdida de foco
* Coordinar desarrollo backend + frontend
* Tener una hoja de ruta operativa real

---

# 📊 Estado actual resumido

## ✅ Completado (estable)

### IAM / Core

* Autenticación JWT (cookies HTTPOnly)
* Refresh token
* RBAC (roles + permisos)
* Middleware de autenticación
* Auditoría

### Módulos administrativos

* Users (CRUD completo)
* Roles (CRUD completo)
* Identities (CRUD completo)
* Dashboard funcional

### UI

* AdminLTE integrado
* Templates Jinja2 reutilizables
* Menú dinámico por permisos

### Calidad

* Tests (~85% cobertura)
* Linter activo
* CI/CD (GitHub Actions)
* SonarQube integrado

---

## 🚧 En progreso

### 1. Módulo de Proyectos (CRÍTICO)

Estado:

* Modelo parcialmente implementado
* CRUD básico funcional
* Integrado en UI

Problemas:

* No existe `project_members`
* No existe `project_teams`
* No hay roles contextuales
* Permisos no definidos a nivel proyecto

👉 PRIORIDAD ALTA

---

### 2. Tasks y Activities

Estado:

* CRUD implementado
* Relación con proyectos funcional

Problemas:

* No existe `assigned_to`
* No existe estado Kanban real
* No hay lógica de asignación por coordinador

👉 DEPENDE del módulo proyectos

---

### 3. Refactor de Templates

Estado:

* Sistema de macros sólido

Problemas:

* Nuevos módulos no siguen estándar
* Posible duplicación de layouts
* Inconsistencias visuales

👉 PRIORIDAD MEDIA

---

### 4. Refactor de Routers

Estado:

* Arquitectura modular definida

Problemas:

* Nuevos routers no alineados con patrón original
* Posible mezcla lógica / presentación

👉 PRIORIDAD MEDIA

---

# 🔥 Tareas prioritarias (orden real recomendado)

---

## 🥇 BLOQUE 1 — BASE DE PROYECTOS (CRÍTICO)

### 1. Crear tabla `project_members`

* [ ] Modelo SQLAlchemy
* [ ] Migración DB
* [ ] Relación con users y projects

---

### 2. Crear tabla `project_teams`

* [ ] Modelo
* [ ] Relación N:M

---

### 3. Definir roles contextuales

* [ ] coordinator
* [ ] member

---

### 4. Crear helpers de permisos

Ejemplo:

* can_manage_project(user, project)
* can_assign_tasks(user, project)

---

## 🥈 BLOQUE 2 — TASKS (KANBAN READY)

### 5. Actualizar modelo Task

* [ ] Añadir `assigned_to`
* [ ] Añadir `status` (todo, doing, done)

---

### 6. Lógica de negocio

* [ ] Solo coordinador crea tareas
* [ ] Solo coordinador asigna tareas
* [ ] Validar que usuario pertenece al proyecto

---

### 7. UI Tasks

* [ ] Mostrar asignación
* [ ] Mostrar estado
* [ ] Preparar vista Kanban (base)

---

## 🥉 BLOQUE 3 — TEAMS

### 8. Implementar módulo Teams

* [ ] Modelo
* [ ] CRUD básico
* [ ] Relación con users

---

### 9. Integración Teams-Proyectos

* [ ] UI para asignar equipos a proyectos
* [ ] Validación backend

---

## 🧱 BLOQUE 4 — REFACTORIZACIÓN

### 10. Templates

* [ ] Unificar formularios
* [ ] Reutilizar macros existentes
* [ ] Revisar consistencia visual

---

### 11. Routers

* [ ] Separar lógica en servicios
* [ ] Alinear naming
* [ ] Evitar duplicación

---

## 🧪 BLOQUE 5 — TESTING

### 12. Tests nuevos

* [ ] project_members
* [ ] tasks asignación
* [ ] permisos contextuales

---

### 13. Cobertura

* [ ] Mantener >85%
* [ ] Añadir tests de integración

---

## 🔐 BLOQUE 6 — SEGURIDAD

### 14. Mejoras

* [ ] CSRF (pendiente)
* [ ] Validaciones más estrictas
* [ ] Revisión permisos nuevos módulos

---

## 🧭 BLOQUE 7 — API (EVOLUCIÓN)

### 15. Nuevos endpoints

#### Projects

* [ ] /projects/{id}/members
* [ ] /projects/{id}/teams

#### Tasks

* [ ] endpoint cambio estado
* [ ] endpoint asignación

---

## 🎯 BLOQUE 8 — KANBAN (FASE FUTURA INMEDIATA)

### 16. Backend

* [ ] endpoint kanban
* [ ] agrupación por estado

---

### 17. Frontend

* [ ] vista columnas
* [ ] drag & drop (fase 2)

---

# ⚠️ Riesgos actuales

* Mezcla de modelos antiguos y nuevos
* Falta de roles contextuales
* Posible deuda técnica en templates
* Falta de control fino de permisos en proyectos

---

# 🧠 Decisiones ya tomadas (importante no romper)

* RBAC global se mantiene
* Roles de proyecto son independientes
* Tasks dependen de Project, no de Team
* Equipos son organizativos, no ejecutores

---

# 📌 Regla de oro actual

👉 No implementar nuevas features sin cerrar:

* project_members
* estructura de tasks

---

# 🚀 Próximo objetivo inmediato

👉 Tener:

* Proyectos con miembros
* Tareas asignables
* Permisos funcionando

---

# 🧭 Estado operativo

El proyecto ha pasado de:

✔ Sistema IAM
➡️ A sistema híbrido IAM + gestión

Y está en transición hacia:

🔥 Plataforma operativa real de gestión de proyectos

---

## Timeline de Auditoría en Tiempo Real

### Estado
Implementado y funcional.

### Características
- Timeline visual de auditoría en `tasks_detail`
- Integración con WebSockets
- Actualización dinámica sin recarga
- Agrupación por fecha:
  - Hoy
  - Ayer
  - Fecha completa
- Prevención de duplicado de etiquetas de fecha
- Integración con AdminLTE Timeline

### Eventos soportados
- CREATE_TASK
- UPDATE_TASK
- DELETE_TASK
- TASK_STATUS_CHANGE

### Pendientes / Mejoras futuras
- Evitar mostrar eventos generados por el propio usuario
- Filtros por tipo de evento
- Timeline global del sistema