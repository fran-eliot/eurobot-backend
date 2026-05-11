# 09_KNOWN_ISSUES.md

## 🧠 Propósito

Este documento recoge:

* Problemas conocidos del sistema
* Deuda técnica acumulada
* Limitaciones actuales
* Riesgos arquitectónicos

Sirve para:

* Evitar regresiones
* Priorizar refactorizaciones
* Documentar decisiones pendientes
* Acelerar debugging

---

# 🚨 BLOQUE 1 — PROBLEMAS CRÍTICOS (Arquitectura)

## 1. Falta de roles contextuales en proyectos

### Problema

El sistema solo utiliza RBAC global.

No existe:

* `project_members`
* roles por proyecto (coordinator / member)

### Impacto

* No se pueden controlar permisos dentro de proyectos
* Lógica de negocio incompleta
* Riesgo de accesos incorrectos

### Estado

🔴 Crítico

---

## 2. Modelo de proyectos incompleto

### Problema

Faltan entidades clave:

* project_members
* project_teams

### Impacto

* Relaciones inconsistentes
* Lógica parcial en backend
* UI sin soporte completo

### Estado

🔴 Crítico

---

## 3. Tasks sin modelo Kanban real

### Problema

Tasks no tienen:

* `assigned_to`
* `status` definido correctamente

### Impacto

* No hay flujo de trabajo real
* No se puede implementar Kanban
* Limitación funcional importante

### Estado

🔴 Crítico

---

# ⚠️ BLOQUE 2 — PROBLEMAS IMPORTANTES

## 4. Inconsistencias entre módulos antiguos y nuevos

### Problema

Los módulos nuevos (projects, tasks, activities):

* no siguen completamente la arquitectura original
* pueden tener lógica duplicada

### Impacto

* Mayor complejidad
* Difícil mantenimiento

### Estado

🟠 Alto

---

## 5. Refactor incompleto de templates

### Problema

* Nuevas vistas no usan correctamente macros existentes
* Posible duplicación de código HTML

### Impacto

* Inconsistencia visual
* Dificultad para cambios globales

### Estado

🟠 Alto

---

## 6. Refactor incompleto de routers

### Problema

* Mezcla de lógica en routers
* Falta de uso consistente de services

### Impacto

* Baja mantenibilidad
* Testing más complejo

### Estado

🟠 Alto

---

## 7. Falta de validaciones de pertenencia a proyecto

### Problema

No se valida correctamente:

* si un usuario pertenece a un proyecto
* si puede modificar tareas

### Impacto

* Posibles accesos indebidos
* Riesgo de seguridad funcional

### Estado

🟠 Alto

---

# 🧪 BLOQUE 3 — TESTING Y CALIDAD

## 8. Cobertura incompleta en nuevos módulos

### Problema

Tests no cubren:

* projects
* tasks avanzados
* lógica futura de project_members

### Impacto

* Riesgo de regresiones

### Estado

🟡 Medio

---

## 9. Falta de tests de integración

### Problema

No hay pruebas completas de flujo:

Login → Proyecto → Tareas → Actividades

### Impacto

* Fallos no detectados en producción

### Estado

🟡 Medio

---

# 🔐 BLOQUE 4 — SEGURIDAD

## 10. Falta de protección CSRF

### Problema

Uso de cookies sin CSRF tokens

### Impacto

* Vulnerabilidad potencial

### Estado

🟠 Alto

---

## 11. Falta de control fino en permisos de nuevos módulos

### Problema

Projects/Tasks no tienen permisos definidos a nivel granular

### Impacto

* Accesos incorrectos posibles

### Estado

🟠 Alto

---

## 12. Refresh token sin rotación

### Problema

El refresh token no rota

### Impacto

* Riesgo en caso de robo

### Estado

🟡 Medio

---

# 🧱 BLOQUE 5 — BASE DE DATOS

## 13. Modelo no alineado con documentación nueva

### Problema

DB actual no incluye:

* project_members
* assigned_to en tasks

### Impacto

* Desfase entre diseño y código

### Estado

🔴 Crítico

---

## 14. Posibles inconsistencias en naming

### Problema

* mezcla de nombres (`id_user`, `user_id`, etc.)

### Impacto

* Confusión
* Bugs sutiles

### Estado

🟡 Medio

---

# 🌐 BLOQUE 6 — API Y RUTAS

## 15. API incompleta para proyectos

### Problema

No existen endpoints para:

* miembros de proyecto
* equipos en proyecto

### Impacto

* Limitación para frontend futuro

### Estado

🟠 Alto

---

## 16. No hay versionado de API

### Problema

No existe `/api/v1`

### Impacto

* Difícil evolución futura

### Estado

🟡 Medio

---

# 🎨 BLOQUE 7 — UI / UX

## 17. No existe Kanban

### Problema

No hay vista Kanban para tareas

### Impacto

* Experiencia limitada
* No refleja modelo de datos objetivo

### Estado

🟡 Medio

---

## 18. Posible inconsistencia en navegación

### Problema

Nuevos módulos pueden no integrarse bien en el menú dinámico

### Impacto

* UX inconsistente

### Estado

🟡 Medio

---

# 🔌 BLOQUE 8 — INTEGRACIONES

## 19. SAML parcialmente implementado

### Problema

* No validado completamente en entorno real
* Flujo incompleto

### Impacto

* Riesgo en producción

### Estado

🟡 Medio

---

# 🧠 BLOQUE 9 — DEUDA TÉCNICA

## 20. Falta de helpers reutilizables

Ejemplo:

* can_manage_project()
* can_assign_task()

### Impacto

* duplicación de lógica
* errores de permisos

### Estado

🟠 Alto

---

## 21. Falta de capa de servicios consolidada

### Problema

No toda la lógica está desacoplada del router

### Impacto

* difícil testing
* menor escalabilidad

### Estado

🟠 Alto

---

# 📌 RESUMEN EJECUTIVO

## 🔴 Crítico (hacer YA)

* project_members
* project_teams
* tasks (assigned_to + status)
* alineación DB

---

## 🟠 Alto (siguiente fase)

* permisos contextuales
* refactor templates
* refactor routers
* CSRF

---

## 🟡 Medio (mejora continua)

* testing integración
* API versionado
* Kanban UI
* SAML completo

---

# 🧭 Regla operativa

👉 No avanzar en features nuevas sin cerrar:

* modelo de proyectos
* control de permisos

---

# 🚀 Conclusión

El sistema es:

✔ Sólido en IAM
⚠️ En transición en negocio
🔥 A punto de convertirse en plataforma real

Pero requiere:

👉 consolidar el módulo de proyectos
👉 estabilizar la arquitectura

---
