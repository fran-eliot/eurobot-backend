# 27_ENUMS_AND_CONSTRAINTS.md

# Enums, Constraints y Reglas de Integridad

## Objetivo

Este documento describe:

- enums funcionales,
- restricciones SQL,
- constraints lógicas,
- reglas de integridad,
- convenciones de validación,
- políticas de consistencia.

El objetivo es documentar la capa de integridad de datos de Aula Robótica Platform.

---

# Filosofía General

La arquitectura de datos sigue varios principios:

## 1. Integridad fuerte

La base de datos protege:

- relaciones,
- ownership,
- consistencia,
- referencias críticas.

---

## 2. Flexibilidad evolutiva

Algunas áreas usan referencias polimórficas ligeras:

```text
entity_type
resource_type
```

para facilitar escalabilidad futura.

---

## 3. Validación multicapa

Las validaciones se distribuyen entre:

- SQLAlchemy,
- constraints SQL,
- Pydantic,
- service layer,
- autorización contextual.

---

# ENUMS Principales

# TaskStatusEnum

Define el workflow Kanban de tareas. :contentReference[oaicite:0]{index=0}

## Valores

```text
todo
doing
done
```

---

## Objetivo

Representar el flujo operativo realtime del sistema Kanban.

---

## Uso

Campo:

```python
Task.status
```

:contentReference[oaicite:1]{index=1}

---

# TaskPriorityEnum

Define prioridad operativa de tareas. :contentReference[oaicite:2]{index=2}

## Valores

```text
low
medium
high
```

---

## Objetivo

Permitir:

- organización visual,
- priorización,
- dashboards,
- métricas futuras.

---

# ProjectRoleEnum

Define roles contextuales dentro de proyectos. :contentReference[oaicite:3]{index=3}

## Valores

```text
coordinator
member
```

---

## Objetivo

Separar:

```text
RBAC global
```

de:

```text
roles contextuales por proyecto
```

---

# NotificationType

Define tipos funcionales de notificación realtime. :contentReference[oaicite:4]{index=4}

## Valores actuales

```text
TASK_ASSIGNED
TASK_STATUS_CHANGED
TASK_UPDATED

PROJECT_MEMBER_ADDED
PROJECT_UPDATED

ACTIVITY_CREATED

SYSTEM
```

---

## Objetivo

Permitir:

- render contextual,
- iconografía,
- agrupación futura,
- categorización realtime.

---

# FeedEvent

Define eventos funcionales del activity feed. :contentReference[oaicite:5]{index=5}

## Eventos de tareas

```text
TASK_CREATED
TASK_UPDATED
TASK_DELETED
TASK_STATUS_CHANGED
```

---

## Eventos de actividades

```text
ACTIVITY_CREATED
ACTIVITY_UPDATED
ACTIVITY_DELETED
```

---

## Eventos de proyectos

```text
PROJECT_CREATED
PROJECT_UPDATED
PROJECT_DELETED
```

---

## Eventos de miembros

```text
MEMBER_JOINED
MEMBER_REMOVED
```

---

# AuditAction

Define acciones auditables del sistema. :contentReference[oaicite:6]{index=6}

## Sesión

```text
LOGIN
LOGOUT
```

---

## Usuarios

```text
CREATE_USER
UPDATE_USER
DELETE_USER
ACTIVATE_USER
DEACTIVATE_USER
```

---

## Proyectos

```text
CREATE_PROJECT
UPDATE_PROJECT
DELETE_PROJECT
```

---

## Tareas

```text
CREATE_TASK
UPDATE_TASK
DELETE_TASK
TASK_STATUS_CHANGE
```

---

# Actions

Acciones atómicas del sistema RBAC. :contentReference[oaicite:7]{index=7}

## Valores

```text
read
create
update
delete
```

---

## Objetivo

Composición dinámica de permisos:

```text
resource:action
```

Ejemplo:

```text
projects:update
```

---

# Resources

Recursos protegidos por RBAC. :contentReference[oaicite:8]{index=8}

## Valores actuales

```text
users
roles
identities
dashboard
students
audit
projects
tasks
activities
```

---

# Constraints SQL Principales

# Primary Keys

Todas las entidades principales poseen PK explícita.

## Ejemplos

```text
usuarios.id_usuario
projects.id_project
tasks.id_task
activities.id_activity
notifications.id_notification
```



---

# Composite Primary Keys

# user_rol

La tabla pivote RBAC usa PK compuesta. :contentReference[oaicite:10]{index=10}

## Campos

```text
user_id
rol_id
```

---

## Beneficios

- evita duplicados,
- simplifica integridad,
- elimina IDs artificiales.

---

# role_permissions

También usa PK compuesta. :contentReference[oaicite:11]{index=11}

## Campos

```text
role_id
permission_id
```

---

# Unique Constraints

# Identity.email

Constraint:

```python
unique=True
```

:contentReference[oaicite:12]{index=12}

---

## Objetivo

Evitar duplicación de identidad autenticable.

---

# Permission.nombre

Constraint:

```python
unique=True
```

:contentReference[oaicite:13]{index=13}

---

# Role.nombre

Constraint:

```python
unique=True
```

:contentReference[oaicite:14]{index=14}

---

# Nullable Constraints

# Campos obligatorios críticos

## User

```text
nombre
activo
fecha_creacion
```

:contentReference[oaicite:15]{index=15}

---

## Identity

```text
email
provider
user_id
```

:contentReference[oaicite:16]{index=16}

---

## Project

```text
name
status
created_at
```

:contentReference[oaicite:17]{index=17}

---

## Task

```text
project_id
name
status
priority
created_by
created_at
```

:contentReference[oaicite:18]{index=18}

---

## Activity

```text
name
status
task_id
user_id
created_at
```

:contentReference[oaicite:19]{index=19}

---

## Notification

```text
user_id
type
title
message
is_read
created_at
```

:contentReference[oaicite:20]{index=20}

---

# Nullable Fields Estratégicos

# Identity.password_hash

Nullable para soportar:

```text
OAuth / SAML / login externo
```

:contentReference[oaicite:21]{index=21}

---

# Task.assigned_to

Nullable porque una tarea puede no estar asignada. :contentReference[oaicite:22]{index=22}

---

# Project.created_by

Nullable para permitir persistencia histórica aunque desaparezca el creador. :contentReference[oaicite:23]{index=23}

---

# Notification.read_at

Nullable hasta lectura. :contentReference[oaicite:24]{index=24}

---

# Foreign Keys y OnDelete

# CASCADE

Usado cuando la entidad hija no tiene sentido sin el padre.

---

## Ejemplos

### Task → Project

```text
ondelete="CASCADE"
```

:contentReference[oaicite:25]{index=25}

---

### Activity → Task

```text
ondelete="CASCADE"
```

:contentReference[oaicite:26]{index=26}

---

### Attachment → Activity

```text
ondelete="CASCADE"
```

:contentReference[oaicite:27]{index=27}

---

### Identity → User

```text
ondelete="CASCADE"
```

:contentReference[oaicite:28]{index=28}

---

### Notification → User

```text
ondelete="CASCADE"
```

:contentReference[oaicite:29]{index=29}

---

# SET NULL

Usado cuando la trazabilidad debe sobrevivir.

---

## AuditLog.user_id

```text
ondelete="SET NULL"
```

:contentReference[oaicite:30]{index=30}

---

## ProjectActivityFeed.user_id

```text
ondelete="SET NULL"
```

:contentReference[oaicite:31]{index=31}

---

# Índices Existentes

# Índices explícitos

## Identity.email

```python
index=True
```

:contentReference[oaicite:32]{index=32}

---

## Notification.user_id

```python
index=True
```

:contentReference[oaicite:33]{index=33}

---

## Notification.type

```python
index=True
```

:contentReference[oaicite:34]{index=34}

---

## Notification.is_read

```python
index=True
```

:contentReference[oaicite:35]{index=35}

---

## ProjectActivityFeed.project_id

```python
index=True
```

:contentReference[oaicite:36]{index=36}

---

## ActivityAttachment.activity_id

```python
index=True
```

:contentReference[oaicite:37]{index=37}

---

# Constraints ORM

# delete-orphan

Usado para ownership fuerte.

---

## Project.tasks

```python
cascade="all, delete-orphan"
```

:contentReference[oaicite:38]{index=38}

---

## Task.activities

```python
cascade="all, delete-orphan"
```

:contentReference[oaicite:39]{index=39}

---

## Activity.attachments

```python
cascade="all, delete-orphan"
```

:contentReference[oaicite:40]{index=40}

---

## User.notifications

```python
cascade="all, delete-orphan"
```

:contentReference[oaicite:41]{index=41}

---

# passive_deletes

Usado para delegar borrado al motor SQL.

## Identity

```python
passive_deletes=True
```



---

## ActivityAttachment

```python
passive_deletes=True
```

:contentReference[oaicite:43]{index=43}

---

# Constraints de Validación Pydantic

# LoginRequest.password

## Reglas

- min_length=4
- no vacío
- trim validation

:contentReference[oaicite:44]{index=44}

---

# User.nombre

## Reglas

- obligatorio,
- trim automático,
- no vacío.

:contentReference[oaicite:45]{index=45}

---

# Constraints Lógicos del Sistema

# RBAC desacoplado

Los permisos NO están hardcodeados por rol.

Arquitectura:

```text
Role ↔ Permission
```

:contentReference[oaicite:46]{index=46}

---

# Roles contextuales desacoplados

Los roles de proyecto viven separados del RBAC global:

```text
ProjectMember.role
```

:contentReference[oaicite:47]{index=47}

---

# Auditoría desacoplada

`AuditLog` usa:

```text
resource_type
resource_id
```

No hay FK directa. :contentReference[oaicite:48]{index=48}

---

# Feed desacoplado

`ProjectActivityFeed` usa:

```text
entity_type
entity_id
```

:contentReference[oaicite:49]{index=49}

---

# Notifications desacopladas

`Notification` usa:

```text
entity_type
entity_id
```

:contentReference[oaicite:50]{index=50}

---

# Constraints Implícitos Recomendados

# ProjectMember unique

Actualmente NO existe:

```text
UNIQUE(project_id, user_id)
```

---

## Recomendación

Añadirlo para evitar:

- miembros duplicados,
- inconsistencias contextuales.

---

# Identity multi-provider

Actualmente:

```text
email UNIQUE
```

limita múltiples providers con mismo email.

---

## Futuro recomendado

Migrar hacia:

```text
UNIQUE(provider, provider_user_id)
```

para soportar:

- SAML,
- Google,
- GitHub,
- OAuth múltiple.

---

# Constraints futuros recomendados

## Attachment MIME whitelist

Actualmente lógica backend.

Recomendable documentar:

```text
allowed MIME types
```

---

## Positive size_bytes

Recomendable:

```sql
CHECK(size_bytes >= 0)
```

---

## Positive time_spent

Recomendable:

```sql
CHECK(time_spent >= 0)
```

---

## Notification read consistency

Recomendable:

```text
read_at != NULL when is_read=True
```

---

# Convenciones del Proyecto

# Naming

## Primary Keys

```text
id_entity
```

Ejemplo:

```text
id_project
id_task
id_activity
```

---

## Foreign Keys

```text
entity_id
```

Ejemplo:

```text
project_id
task_id
user_id
```

---

# Timestamps UTC

Todos los timestamps usan:

```python
datetime.now(UTC)
```



---

# Filosofía de Constraints

La arquitectura prioriza:

## Fuerte integridad donde importa

- ownership,
- relaciones críticas,
- cascadas funcionales.

---

## Flexibilidad donde importa escalabilidad

- auditoría,
- feed,
- notificaciones,
- referencias polimórficas.

---

# Riesgos Actuales

## 1. Constraints faltantes

Algunos unique constraints aún no existen.

---

## 2. CHECK constraints mínimos

Muchos controles viven en service layer.

---

## 3. Integridad polimórfica

No existe FK real para:

```text
entity_type/entity_id
```

---

# Ventajas del Diseño

## Escalabilidad

Modelo preparado para crecer.

---

## Compatibilidad realtime

Optimizado para:

- dashboards,
- feeds,
- websocket events,
- notificaciones.

---

## Enterprise readiness

Separación clara entre:

- identidad,
- autorización,
- ownership,
- actividad,
- auditoría.

---

# Conclusión

El sistema actual ya posee una arquitectura de integridad bastante madura para una plataforma educativa-operacional.

La combinación de:

- enums explícitos,
- constraints SQL,
- validaciones Pydantic,
- reglas ORM,
- service layer validation,
- RBAC desacoplado,
- relaciones contextuales,

permite una base sólida para evolucionar Aula Robótica Platform hacia una plataforma enterprise realtime y multiusuario.