# 04_DATABASE_SCHEMA.md

## 🧱 Núcleo IAM

### users

* id_usuario (PK)
* nombre
* activo
* fecha_creacion

---

### identities

* id_identidad (PK)
* email
* password_hash
* provider
* user_id (FK)

---

### roles

* id_rol (PK)
* nombre

---

### permissions

* id (PK)
* nombre

---

### user_roles

* user_id (FK)
* role_id (FK)

---

### role_permissions

* role_id (FK)
* permission_id (FK)

---

### audit_logs

* id_log (PK)
* user_id (FK)
* action
* resource_type
* resource_id
* description
* ip_address
* user_agent
* created_at

---

# 🧩 Módulo Proyectos

### projects

* id_project (PK)
* name
* description
* project_type_id
* status_id
* start_date
* end_date
* created_by (FK users)

---

### teams

* id_team (PK)
* name
* description
* created_at

---

### team_members

* id
* team_id (FK)
* user_id (FK)

---

### project_teams

* id
* project_id (FK)
* team_id (FK)

---

### project_members 🔥

* id
* project_id (FK)
* user_id (FK)
* role ENUM('coordinator','member')

---

### tasks

* id_task (PK)
* project_id (FK)
* name
* description
* status ENUM('todo','doing','done')
* priority
* assigned_to (FK users)
* due_date
* created_by (FK users)

---

### activities

* id_activity (PK)
* task_id (FK)
* user_id (FK)
* description
* time_spent
* date

---

### attachments (pendiente)

* id_attachment (PK)
* activity_id (FK)
* filename
* file_path
* mime_type

---

## 🔗 Relaciones clave

* users ↔ roles (N:M)
* roles ↔ permissions (N:M)
* users → identities (1:N)
* users → audit_logs (1:N)

---

## Proyectos

* projects ↔ teams (N:M)
* projects ↔ users (N:M vía project_members)
* projects → tasks (1:N)
* tasks → activities (1:N)
* activities → attachments (1:N)

---

## 📌 Notas

* Separación RBAC vs roles de proyecto
* Equipos no contienen lógica de ejecución
* Tareas pertenecen al proyecto
* Preparado para Kanban
