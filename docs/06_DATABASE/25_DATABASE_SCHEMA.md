# 25_DATABASE_SCHEMA.md

# 📌 Esquema de Base de Datos

La plataforma utiliza MariaDB/MySQL como motor relacional principal.

El modelo de datos está diseñado siguiendo principios:

- modularidad
- normalización
- trazabilidad
- autorización contextual
- escalabilidad progresiva

---

# 🧱 Núcleo IAM / Seguridad

## users

Representa usuarios internos del sistema.

| Campo | Tipo |
|---|---|
| id_usuario | PK |
| nombre | VARCHAR |
| activo | BOOLEAN |
| fecha_creacion | DATETIME |

---

## identities

Credenciales y proveedores de autenticación.

| Campo | Tipo |
|---|---|
| id | PK |
| email | VARCHAR UNIQUE |
| password_hash | VARCHAR |
| provider | ENUM/local/saml/oauth |
| user_id | FK → users |

Relación:

```text
users (1) ──── (N) identities
```
---

# roles
Roles globales RBAC.
| Campo | Tipo |
| :--- | :--- |
| id_rol | PK |
| nombre | VARCHAR |
| descripcion | TEXT |

# permissions
Permisos atómicos.
| Campo | Tipo |
| :--- | :--- |
| id | PK |
| nombre | VARCHAR UNIQUE |

**Ejemplos:**
* users:create
* projects:update
* tasks:delete
* activities:read

# user_rol
Relación N:M usuarios ↔ roles.
| Campo | Tipo |
| :--- | :--- |
| user_id | FK |
| rol_id | FK |

# role_permissions
Relación N:M roles ↔ permisos.
| Campo | Tipo |
| :--- | :--- |
| role_id | FK |
| permission_id | FK |

# 🧾 Auditoría
## audit_logs
Registro de eventos críticos.
| Campo | Tipo |
| :--- | :--- |
| id_log | PK |
| action | VARCHAR |
| user_id | FK → users |
| resource_type | VARCHAR |
| resource_id | INTEGER |
| description | TEXT |
| ip_address | VARCHAR |
| user_agent | TEXT |
| created_at | DATETIME |

**Características:**
* auditoría completa
* trazabilidad
* logging enriquecido
* metadata de cliente

# 🧩 Módulo Proyectos
## projects
Entidad principal de proyectos.
| Campo | Tipo |
| :--- | :--- |
| id_project | PK |
| name | VARCHAR |
| description | TEXT |
| status | ENUM |
| start_date | DATE |
| end_date | DATE |
| created_by | FK → users |
| created_at | DATETIME |

**Estados actuales:**
* Activo
* Finalizado
* Pausado

## teams
Agrupaciones organizativas.
| Campo | Tipo |
| :--- | :--- |
| id_team | PK |
| name | VARCHAR |
| description | TEXT |
| created_at | DATETIME |

## team_members
Usuarios pertenecientes a equipos.
| Campo | Tipo |
| :--- | :--- |
| id | PK |
| team_id | FK |
| user_id | FK |

## project_teams
Asignación equipos ↔ proyectos.
| Campo | Tipo |
| :--- | :--- |
| id | PK |
| project_id | FK |
| team_id | FK |

## project_members
Participación contextual de usuarios en proyectos.
| Campo | Tipo |
| :--- | :--- |
| id | PK |
| project_id | FK |
| user_id | FK |
| role | ENUM(coordinator/member) |

**Importante:**
Separado del RBAC global.
Permite:
* ownership contextual
* coordinadores
* permisos específicos de proyecto

# ✅ Módulo Tareas
## tasks
Tareas pertenecientes a proyectos.
| Campo | Tipo |
| :--- | :--- |
| id_task | PK |
| project_id | FK → projects |
| name | VARCHAR |
| description | TEXT |
| status | ENUM(todo/doing/done) |
| priority | ENUM |
| assigned_to | FK → users |
| created_by | FK → users |
| due_date | DATE |
| created_at | DATETIME |

# 🕒 Módulo Actividades
## activities
Registro operativo del trabajo realizado.
| Campo | Tipo |
| :--- | :--- |
| id_activity | PK |
| name | VARCHAR |
| description | TEXT |
| status | ENUM |
| task_id | FK → tasks |
| user_id | FK → users |
| time_spent | FLOAT |
| created_at | DATETIME |

**Estados actuales:**
* Pendiente
* En progreso
* Completada

# 📎 Sistema de Adjuntos
## activity_attachments
Sistema completo de adjuntos para actividades.
| Campo | Tipo |
| :--- | :--- |
| id_attachment | PK |
| activity_id | FK → activities |
| uploaded_by | FK → users |
| original_filename | VARCHAR |
| stored_filename | VARCHAR |
| file_path | VARCHAR |
| mime_type | VARCHAR |
| size_bytes | INTEGER |
| description | TEXT NULL |
| created_at | DATETIME |

**Características:**
* almacenamiento filesystem
* metadata persistente
* ownership
* uploads seguros
* soporte imágenes/documentos

# 🔔 Sistema de Notificaciones
## notifications
Notificaciones persistentes por usuario.
| Campo | Tipo |
| :--- | :--- |
| id_notification | PK |
| user_id | FK → users |
| type | VARCHAR |
| title | VARCHAR |
| message | TEXT |
| entity_type | VARCHAR |
| entity_id | INTEGER |
| url | VARCHAR |
| is_read | BOOLEAN |
| created_at | DATETIME |
| read_at | DATETIME NULL |

**Características:**
* realtime compatible
* unread counters
* navegación contextual
* persistencia completa

# 📡 Activity Feed
## project_activity_feed
Timeline operacional realtime.
| Campo | Tipo |
| :--- | :--- |
| id_feed | PK |
| project_id | FK → projects |
| user_id | FK → users |
| event_type | VARCHAR |
| message | TEXT |
| entity_type | VARCHAR |
| entity_id | INTEGER |
| created_at | DATETIME |

**Usado para:**
* timelines
* dashboards
* realtime feeds
* trazabilidad operacional

# 🔗 Relaciones Principales
### IAM
* users ↔ roles (N:M)
* roles ↔ permissions (N:M)
* users → identities (1:N)
* users → audit_logs (1:N)

### Proyectos
* projects ↔ teams (N:M)
* projects ↔ users (N:M vía project_members)
* projects → tasks (1:N)

### Operaciones
* tasks → activities (1:N)
* activities → attachments (1:N)
* users → activities (1:N)

### Realtime / Feed
* projects → project_activity_feed (1:N)
* users → notifications (1:N)

# 🧠 Decisiones de Diseño
### Separación RBAC vs Contextual Roles
**RBAC global:**
* admin
* teacher
* student

**Roles contextuales:**
* project coordinator
* project member

### Attachments desacoplados
**Permite:**
* reutilización futura
* migración a object storage
* versionado futuro

### Notifications persistentes
No dependen únicamente de WebSockets.
**Permiten:**
* recuperación histórica
* unread counters
* sincronización multi-dispositivo

# 🚀 Preparado para Evolución
La arquitectura de datos ya está preparada para:
* Kanban avanzado
* comentarios
* realtime collaboration
* versionado documental
* object storage
* multi-tenant
* SSO/SAML
* analytics
* dashboards avanzados
