# WEEKLY_UPDATE.md

## 🧠 Propósito

Registrar de forma continua:

* Trabajo realizado
* Problemas encontrados
* Decisiones tomadas
* Próximos pasos

Sirve para:

* Mantener contexto entre sesiones
* Evitar pérdida de información
* Facilitar debugging futuro
* Documentar evolución real del proyecto

---

# 📅 Formato de actualización

Cada semana debe seguir esta estructura:

---

## 🗓️ Semana: [YYYY-MM-DD → YYYY-MM-DD]

---

### ✅ Trabajo realizado

*
*
*

---

### 🚧 En progreso

*
*
*

---

### ❗ Problemas encontrados

*
*
*

---

### 🧠 Decisiones tomadas

*
*
*

---

### 🔧 Cambios técnicos relevantes

*
*
*

---

### 🧪 Testing

* Cobertura actual:
* Tests añadidos:
* Problemas detectados:

---

### 🔐 Seguridad

* Cambios realizados:
* Riesgos detectados:

---

### 📊 Estado general

* 🔴 Bloqueado
* 🟠 Inestable
* 🟡 Progresando
* 🟢 Estable

---

### 🎯 Próximos pasos

1.
2.
3.

---

---

# 🧾 HISTÓRICO

---

## 🗓️ Semana: 2026-XX-XX → 2026-XX-XX

### ✅ Trabajo realizado

* Consolidación del sistema IAM
* Implementación de RBAC completo
* Desarrollo de módulos:

  * users
  * roles
  * identities
  * dashboard

---

### 🚧 En progreso

* Integración del módulo de proyectos
* Refactor de templates
* Refactor de routers

---

### ❗ Problemas encontrados

* Falta de roles contextuales en proyectos
* Tasks sin modelo Kanban
* Inconsistencias entre módulos nuevos y antiguos

---

### 🧠 Decisiones tomadas

* Separar RBAC global de roles de proyecto
* Introducir `project_members`
* Definir coordinador como rol clave en proyectos

---

### 🔧 Cambios técnicos relevantes

* Introducción de modelo de proyectos
* Implementación parcial de tasks y activities
* Integración en UI

---

### 🧪 Testing

* Cobertura ~85%
* CI/CD activo
* SonarQube integrado

---

### 🔐 Seguridad

* JWT en cookies HTTPOnly
* RBAC funcional
* Pendiente CSRF

---

### 📊 Estado general

🟡 Progresando

---

### 🎯 Próximos pasos

1. Implementar `project_members`
2. Añadir `assigned_to` y `status` en tasks
3. Implementar Teams
4. Refactor templates

---

---

# 📌 Reglas de uso

* Actualizar al final de cada sesión importante
* Ser conciso pero claro
* Registrar decisiones clave (no solo tareas)
* No borrar histórico

---

# 🚀 Objetivo

Convertir este archivo en:

👉 La memoria real del desarrollo
👉 El punto de partida de cada sesión

---
