# 13_PROJECTS_MODULE.md

## 🧠 Propósito

Definir el módulo de **Gestión de Proyectos**, permitiendo:

* Gestión de proyectos
* Participación de equipos
* Roles contextuales por proyecto
* Gestión de tareas
* Registro de actividad
* Base para Kanban

---

## 🎯 Principios

* Separación RBAC vs roles de proyecto
* Proyectos como unidad de trabajo
* Equipos como agrupación organizativa
* Tareas pertenecen al proyecto
* Coordinador actúa a nivel de proyecto

---

## 🧩 Entidades

### Project

* id
* name
* description
* project_type_id
* status_id
* start_date
* end_date
* created_by

---

### Team

* id
* name
* description
* created_at

---

### ProjectTeam

* id
* project_id
* team_id

---

### ProjectMember 🔥

* id
* project_id
* user_id
* role (coordinator | member)

---

### Task

* id
* project_id
* name
* description
* status (todo | doing | done)
* priority
* assigned_to
* due_date
* created_by

---

### Activity

* id
* task_id
* user_id
* description
* time_spent
* date

---

### Attachment (pendiente)

---

## 🔗 Relaciones

Users → ProjectMembers → Projects → Tasks → Activities

Projects ↔ Teams (N:M)

---

## 🎭 Roles

### Globales (RBAC)

* admin
* profesor
* estudiante

---

### Proyecto

* coordinator
* member

---

## 🔐 Permisos

### Global

* projects:create → admin/profesor

### Contextual

#### Coordinator

* crear tareas
* asignar tareas
* cambiar estado
* ver proyecto

#### Member

* ver tareas
* registrar actividad

---

## ⚙️ Reglas

* Proyecto creado por admin/profesor
* Equipos asignados al proyecto
* Usuarios asignados vía ProjectMember
* Tareas gestionadas por coordinador
* Actividades registradas por miembros

---

## 📊 Kanban

Basado en:

* status
* assigned_to

---

## 🔌 API (borrador)

### Projects

* GET /projects
* POST /projects

### Members

* POST /projects/{id}/members

### Tasks

* POST /projects/{id}/tasks

---

## 🧱 Cambios DB

* Nueva tabla: project_members
* Nueva tabla: project_teams
* tasks: añadir status y assigned_to

---

## 🚧 Pendiente

* Teams
* Attachments
* Kanban UI
* permisos contextuales

---

## 📌 Resumen

Introduce:

* roles por proyecto
* workflow real
* base para gestión profesional

