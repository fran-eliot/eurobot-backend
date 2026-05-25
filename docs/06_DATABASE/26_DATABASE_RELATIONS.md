# 26_DATABASE_RELATIONS.md

# Relaciones de Base de Datos

## Objetivo

Este documento describe las relaciones principales del modelo de datos de Aula Robótica Platform.

La base de datos está diseñada alrededor de varios núcleos funcionales:

- usuarios e identidades,
- RBAC,
- proyectos,
- tareas,
- actividades,
- adjuntos,
- auditoría,
- activity feed,
- notificaciones.

---

# Visión General

```text
User
 ├── Identity
 ├── Role
 ├── ProjectMember
 ├── Task
 ├── Activity
 ├── ActivityAttachment
 ├── Notification
 └── AuditLog

Project
 ├── ProjectMember
 ├── Task
 └── ProjectActivityFeed

Task
 └── Activity

Activity
 └── ActivityAttachment
```

---

# Núcleo de Usuarios

## User

Tabla:

```text
usuarios
```

El modelo `User` representa a una persona dentro del sistema. No contiene credenciales; las credenciales viven en `Identity`. :contentReference[oaicite:0]{index=0}

---

## User → Identity

Relación:

```text
User 1 ─── N Identity
```

Una persona puede tener varias identidades de autenticación:

- local,
- SAML,
- OAuth futuro,
- otros proveedores externos.

La relación se define desde `User.identidades` y se elimina en cascada al borrar el usuario. 

---

## Identity → User

Cada identidad pertenece obligatoriamente a un usuario mediante:

```text
identities.user_id → usuarios.id_usuario
```

Con:

```text
ondelete="CASCADE"
```

Esto permite eliminar automáticamente identidades asociadas si se elimina el usuario. :contentReference[oaicite:2]{index=2}

---

# Modelo RBAC

## User ↔ Role

Relación:

```text
User N ─── N Role
```

Tabla intermedia:

```text
user_rol
```

La tabla `user_rol` usa clave primaria compuesta:

```text
user_id
rol_id
```

Esto evita duplicados de forma natural. :contentReference[oaicite:3]{index=3}

---

## UserRole

Relaciones:

```text
user_rol.user_id → usuarios.id_usuario
user_rol.rol_id  → roles.id_rol
```

Ambas claves foráneas usan:

```text
ondelete="CASCADE"
```

Si se elimina un usuario o un rol, sus relaciones RBAC se eliminan automáticamente. :contentReference[oaicite:4]{index=4}

---

## Role ↔ Permission

Relación:

```text
Role N ─── N Permission
```

Tabla intermedia:

```text
role_permissions
```

El modelo `RolePermission` usa clave primaria compuesta:

```text
role_id
permission_id
```

Ambas claves foráneas usan `ondelete="CASCADE"`. :contentReference[oaicite:5]{index=5}

---

## Permission

Tabla:

```text
permissions
```

Cada permiso tiene un nombre único con formato funcional:

```text
resource:action
```

Ejemplos:

```text
users:read
projects:create
tasks:update
```

El campo `nombre` es único y obligatorio. :contentReference[oaicite:6]{index=6}

---

# Núcleo de Proyectos

## Project

Tabla:

```text
projects
```

Un proyecto agrupa tareas, miembros y actividad funcional. :contentReference[oaicite:7]{index=7}

---

## User → Project

Relación indirecta mediante:

```text
project_members
```

Esto permite que un usuario participe en varios proyectos y que cada proyecto tenga varios miembros.

```text
User N ─── N Project
```

a través de:

```text
ProjectMember
```



---

## Project.creator

Cada proyecto puede tener un creador:

```text
projects.created_by → usuarios.id_usuario
```

Esta relación es nullable, por lo que un proyecto puede existir aunque no se conserve el usuario creador. :contentReference[oaicite:9]{index=9}

---

## Project → ProjectMember

Relación:

```text
Project 1 ─── N ProjectMember
```

Definida con:

```python
cascade="all, delete-orphan"
```

Si se elimina un proyecto, se eliminan sus miembros contextuales asociados. :contentReference[oaicite:10]{index=10}

---

## ProjectMember

Tabla:

```text
project_members
```

Relaciona:

```text
project_id → projects.id_project
user_id    → usuarios.id_usuario
```

Incluye además un rol contextual dentro del proyecto. :contentReference[oaicite:11]{index=11}

---

## Roles Contextuales

`ProjectMember.role` usa:

```text
ProjectRoleEnum
```

Valores actuales:

```text
coordinator
member
```

:contentReference[oaicite:12]{index=12}

---

# Núcleo de Tareas

## Project → Task

Relación:

```text
Project 1 ─── N Task
```

Una tarea pertenece obligatoriamente a un proyecto mediante:

```text
tasks.project_id → projects.id_project
```

con:

```text
ondelete="CASCADE"
```

:contentReference[oaicite:13]{index=13}

---

## Task → Project

Cada tarea tiene una relación ORM:

```python
project = relationship("Project", back_populates="tasks")
```

El proyecto define la relación inversa:

```python
tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
```



---

## Task.assignee

Una tarea puede tener un usuario asignado:

```text
tasks.assigned_to → usuarios.id_usuario
```

Esta relación es nullable. :contentReference[oaicite:15]{index=15}

---

## Task.creator

Una tarea tiene un creador:

```text
tasks.created_by → usuarios.id_usuario
```

Actualmente es obligatorio. :contentReference[oaicite:16]{index=16}

---

## Task → Activity

Relación:

```text
Task 1 ─── N Activity
```

La relación está definida con:

```python
cascade="all, delete-orphan"
```

Por tanto, si se elimina una tarea desde ORM, sus actividades asociadas también se eliminan. :contentReference[oaicite:17]{index=17}

---

# Núcleo de Actividades

## Activity

Tabla:

```text
activities
```

Una actividad representa trabajo registrado sobre una tarea concreta. :contentReference[oaicite:18]{index=18}

---

## Activity → Task

Cada actividad pertenece obligatoriamente a una tarea:

```text
activities.task_id → tasks.id_task
```

con:

```text
ondelete="CASCADE"
```

:contentReference[oaicite:19]{index=19}

---

## Activity → User

Cada actividad pertenece a un usuario:

```text
activities.user_id → usuarios.id_usuario
```

Es obligatorio. :contentReference[oaicite:20]{index=20}

---

## User → Activity

Relación:

```text
User 1 ─── N Activity
```

Desde `User.activities` y `Activity.user`. 

---

## Activity → ActivityAttachment

Relación:

```text
Activity 1 ─── N ActivityAttachment
```

Definida con:

```python
cascade="all, delete-orphan"
passive_deletes=True
```

:contentReference[oaicite:22]{index=22}

---

# Núcleo de Adjuntos

## ActivityAttachment

Tabla:

```text
activity_attachments
```

Un adjunto pertenece a una actividad y tiene un usuario uploader. :contentReference[oaicite:23]{index=23}

---

## Attachment → Activity

Relación:

```text
activity_attachments.activity_id → activities.id_activity
```

con:

```text
ondelete="CASCADE"
```

Esto permite eliminar adjuntos cuando se elimina la actividad asociada. :contentReference[oaicite:24]{index=24}

---

## Attachment → User

Relación:

```text
activity_attachments.uploaded_by → usuarios.id_usuario
```

Cada adjunto conserva quién lo subió. :contentReference[oaicite:25]{index=25}

---

## User → ActivityAttachment

Relación:

```text
User 1 ─── N ActivityAttachment
```

Definida mediante:

```python
User.activity_attachments
ActivityAttachment.uploader
```



---

# Núcleo de Notificaciones

## Notification

Tabla:

```text
notifications
```

Las notificaciones pertenecen siempre a un usuario. :contentReference[oaicite:27]{index=27}

---

## Notification → User

Relación:

```text
notifications.user_id → usuarios.id_usuario
```

con:

```text
ondelete="CASCADE"
```

Si se elimina un usuario, se eliminan sus notificaciones. :contentReference[oaicite:28]{index=28}

---

## User → Notification

Relación:

```text
User 1 ─── N Notification
```

Definida con:

```python
cascade="all, delete-orphan"
```



---

## Relación con entidades funcionales

Las notificaciones usan referencia polimórfica ligera:

```text
entity_type
entity_id
```

No existe ForeignKey directa hacia cada entidad.

Esto permite referenciar:

- tareas,
- proyectos,
- actividades,
- sistema,
- futuras entidades.

:contentReference[oaicite:30]{index=30}

---

# Núcleo de Auditoría

## AuditLog

Tabla:

```text
audit_logs
```

Registra acciones técnicas del sistema. :contentReference[oaicite:31]{index=31}

---

## AuditLog → User

Relación:

```text
audit_logs.user_id → usuarios.id_usuario
```

con:

```text
ondelete="SET NULL"
```

Esto permite conservar trazabilidad aunque el usuario sea eliminado. :contentReference[oaicite:32]{index=32}

---

## User → AuditLog

Relación:

```text
User 1 ─── N AuditLog
```

Definida mediante:

```python
User.audit_logs
AuditLog.user
```



---

## Relación con entidades auditadas

`AuditLog` usa referencia polimórfica ligera:

```text
resource_type
resource_id
```

No hay ForeignKey directa hacia cada entidad auditada. :contentReference[oaicite:34]{index=34}

---

# Núcleo de Activity Feed

## ProjectActivityFeed

Tabla:

```text
project_activity_feed
```

Registra actividad funcional visible en proyectos y dashboard. :contentReference[oaicite:35]{index=35}

---

## Feed → Project

Relación:

```text
project_activity_feed.project_id → projects.id_project
```

con:

```text
ondelete="CASCADE"
```

Si se elimina un proyecto, se eliminan sus eventos funcionales. :contentReference[oaicite:36]{index=36}

---

## Feed → User

Relación:

```text
project_activity_feed.user_id → usuarios.id_usuario
```

con:

```text
ondelete="SET NULL"
```

Esto permite conservar eventos aunque desaparezca el usuario actor. :contentReference[oaicite:37]{index=37}

---

## Relación funcional con entidades

El feed usa referencia polimórfica:

```text
entity_type
entity_id
```

Esto permite registrar eventos sobre:

- tareas,
- actividades,
- proyectos,
- miembros,
- adjuntos futuros.

:contentReference[oaicite:38]{index=38}

---

# Relaciones con Cascada

## Cascadas fuertes

| Origen | Destino | Comportamiento |
|---|---|---|
| User | Identity | cascade/delete |
| User | Notification | cascade/delete-orphan |
| Project | Task | cascade/delete-orphan |
| Project | ProjectMember | cascade/delete-orphan |
| Task | Activity | cascade/delete-orphan |
| Activity | ActivityAttachment | cascade/delete-orphan |
| Project | ProjectActivityFeed | ondelete CASCADE |
| UserRole | User/Role | ondelete CASCADE |
| RolePermission | Role/Permission | ondelete CASCADE |

---

# Relaciones con SET NULL

| Origen | Destino | Motivo |
|---|---|---|
| AuditLog.user_id | User | conservar auditoría histórica |
| ProjectActivityFeed.user_id | User | conservar feed funcional |

---

# Relaciones Polimórficas Ligeras

El sistema usa referencias polimórficas en:

## AuditLog

```text
resource_type
resource_id
```

## ProjectActivityFeed

```text
entity_type
entity_id
```

## Notification

```text
entity_type
entity_id
```

---

# Ventajas

- desacoplamiento,
- extensibilidad,
- menor complejidad relacional,
- compatibilidad con múltiples entidades,
- útil para auditoría y feeds.

---

# Riesgos

- no hay integridad referencial directa,
- requiere validación en service layer,
- puede dejar referencias huérfanas si no se controla.

---

# Relaciones Críticas del Dominio

## Usuario e Identidad

```text
User 1 ─── N Identity
```

Base de arquitectura IAM multi-provider.

---

## Usuario y Roles

```text
User N ─── N Role
```

Base del RBAC global.

---

## Rol y Permisos

```text
Role N ─── N Permission
```

Base de permisos granulares.

---

## Proyecto y Miembros

```text
Project 1 ─── N ProjectMember
```

Base de autorización contextual.

---

## Proyecto y Tareas

```text
Project 1 ─── N Task
```

Base del módulo operativo.

---

## Tarea y Actividades

```text
Task 1 ─── N Activity
```

Base del seguimiento de trabajo.

---

## Actividad y Adjuntos

```text
Activity 1 ─── N ActivityAttachment
```

Base documental del trabajo realizado.

---

# Observaciones de Diseño

## Separación User / Identity

Decisión importante.

Permite:

- login local,
- SAML,
- OAuth,
- múltiples identidades,
- SSO institucional.

---

## Separación Role / Permission

Decisión enterprise.

Permite:

- RBAC flexible,
- permisos atómicos,
- evolución sin romper roles,
- control granular.

---

## Separación Audit / Feed

Decisión importante.

Permite diferenciar:

```text
auditoría técnica
```

de:

```text
actividad funcional visible
```

---

## ProjectMember como RBAC contextual

Permite roles por proyecto sin contaminar roles globales.

---

# Mejoras Futuras Recomendadas

## 1. Unique constraint en ProjectMember

Recomendado:

```text
UNIQUE(project_id, user_id)
```

Para evitar duplicar miembros dentro del mismo proyecto.

---

## 2. Composite indexes

Recomendados:

```text
(project_id, created_at)
(user_id, is_read)
(resource_type, resource_id)
(entity_type, entity_id)
```

---

## 3. Relación Task.created_by explícita

Actualmente existe FK, pero sería recomendable añadir relationship ORM específica.

---

## 4. Relación ProjectActivityFeed inversa

Actualmente `ProjectActivityFeed.project` no usa `back_populates`.

Podría añadirse si se necesita navegación inversa desde `Project`.

---

## 5. Retention policy

Especialmente para:

- audit_logs,
- project_activity_feed,
- notifications.

---

# Conclusión

El modelo relacional actual ya soporta una plataforma bastante avanzada:

```text
IAM + RBAC + proyectos + tareas + actividades + adjuntos + auditoría + realtime + notificaciones
```

La arquitectura combina relaciones estrictas donde importa la integridad operativa y referencias polimórficas ligeras donde importa la flexibilidad.

Esto permite que Aula Robótica Platform evolucione desde un sistema académico hacia una plataforma enterprise modular orientada a operaciones, colaboración y trazabilidad.