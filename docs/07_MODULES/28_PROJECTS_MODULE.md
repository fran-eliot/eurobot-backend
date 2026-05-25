# 28_PROJECTS_MODULE.md

# 🧠 Módulo de Gestión de Proyectos

# 🎯 Propósito

El módulo de proyectos constituye actualmente:

```text
el núcleo operativo de la plataforma
```

# Permite:
* gestión de proyectos
* gestión de tareas
* gestión de actividades
* auditoría realtime
* timelines operativos
* notificaciones
* attachments
* colaboración administrativa
* workflows organizativos

# 🏗️ Visión Arquitectónica
El sistema evolucionó desde un **CRUD académico simple** hacia una **plataforma SSR enterprise orientada a gestión operativa**.

# 📦 Capas Funcionales
| Capa | Responsabilidad |
| :--- | :--- |
| **Projects** | Unidad organizativa |
| **Tasks** | Gestión operativa |
| **Activities** | Ejecución granular |
| **Audit Timeline** | Trazabilidad |
| **Notifications** | Comunicación realtime |
| **Attachments** | Evidencias/documentos |
| **Permissions** | Seguridad contextual |
| **UI System** | Render enterprise SSR |

# 🧩 Entidades Principales
## Project
**Representa:**
* proyecto organizativo
* iniciativa académica
* flujo operativo

### Campos
| Campo | Descripción |
| :--- | :--- |
| **id_project** | PK |
| **name** | Nombre |
| **description** | Descripción |
| **status** | Estado |
| **start_date** | Inicio |
| **end_date** | Fin |
| **created_by** | Usuario creador |
| **created_at** | Timestamp |

### Relaciones
```text
 Project
 ├── Tasks
 ├── ActivityFeed
 ├── AuditTimeline
 └── (futuro) ProjectMembers
 ```
## Task
Unidad operativa principal.

### Campos
| Campo | Descripción |
| :--- | :--- |
| **id_task** | PK |
| **project_id** | Proyecto |
| **name** | Nombre |
| **description** | Descripción |
| **status** | todo / doing / done |
| **priority** | Prioridad |
| **assigned_to** | Responsable |
| **due_date** | Fecha límite |
| **created_by** | Autor |
| **created_at** | Timestamp |

### Características actuales
**Workflow Kanban parcial**  
**Estados:**
* todo
* doing
* done

**Prioridades**  
**Soporte:**
* low
* medium
* high
* critical

### Relaciones
```text
Task
 ├── Project
 ├── Activities
 ├── Assigned User
 └── Audit Timeline
 ```

## Activity
Unidad granular de trabajo real.

**Representa:**
* trabajo ejecutado
* avance
* evidencia operativa
* trazabilidad

### Campos
| Campo | Descripción |
| :--- | :--- |
| **id_activity** | PK |
| **task_id** | Tarea |
| **user_id** | Usuario |
| **name** | Nombre |
| **description** | Descripción |
| **status** | Estado |
| **time_spent** | Tiempo invertido |
| **created_at** | Timestamp |

### Evolución del sistema Activity
El módulo evolucionó significativamente.
**Actualmente soporta:**
* detail layouts modernos
* attachments
* audit timeline
* render contextual
* realtime updates
* integración SSR avanzada

## Activity Attachments
**Implementado ✔**  
Sistema completo de adjuntos.

**Capacidades:**
* upload
* descarga
* eliminación
* metadata persistente
* validación
* render UI

### Entity: ActivityAttachment
| Campo | Descripción |
| :--- | :--- |
| **id_attachment** | PK |
| **activity_id** | Actividad |
| **uploaded_by** | Usuario |
| **original_filename** | Nombre original |
| **stored_filename** | UUID físico |
| **file_path** | Ruta |
| **mime_type** | MIME |
| **size_bytes** | Tamaño |
| **description** | Descripción |
| **created_at** | Timestamp |

### Relaciones
```text
Activity 
 └── ActivityAttachments
 ```

 # Audit & Timeline System
**Implementado ✔**  
El módulo de proyectos integra:
* auditoría estructurada
* timelines realtime
* eventos contextuales

## Eventos auditados
### Projects
* creación
* modificación
* eliminación

### Tasks
* creación
* cambio estado
* asignación
* edición

### Activities
* creación
* edición
* uploads
* eliminación attachments

# Realtime Architecture
**Integrado ✔**  
El módulo soporta:
* websocket realtime
* dashboard sync
* notifications
* audit timeline realtime

## Características
* actualización incremental
* render parcial
* inserción dinámica
* sincronización visual

# Notifications System
**Integrado ✔**  
El módulo ya integra:
* notificaciones persistentes
* realtime notifications
* dropdown dinámico
* unread counters

## Eventos típicos
* nueva actividad
* tarea asignada
* cambios críticos
* uploads importantes

# Seguridad & Permisos
## RBAC Global
**Roles actuales:**
| Rol | Capacidades |
| :--- | :--- |
| **admin** | Control total |
| **profesor** | Gestión operativa |
| **estudiante** | Acceso limitado |

## Permisos Granulares
**Ejemplos:**
* `projects:create`
* `projects:update`
* `tasks:create`
* `activities:update`

## Render Contextual SSR
La UI renderiza botones, acciones, navegación y formularios según permisos reales.

### Helpers UI
**Disponibles:**
* `has_perm()`
* `has_role()`
* `can()`
* `is_owner()`

# Arquitectura UI del módulo
**Consolidada ✔**  
El módulo usa:
* SSR enterprise layouts
* reusable cards
* contextual toolbars
* reusable rows
* timelines
* action systems

## Detail Layouts
**Patrón actual:**

```text
LEFT PANEL
 ├── información principal
 ├── timeline
 ├── attachments
 └── contenido

RIGHT PANEL
 ├── metadata
 ├── acciones
 ├── estadísticas
 └── información contextual
 ```

 # Reusable Components
**Implementados**
* `project_row`
* `task_row`
* `activity_row`
* reusable buttons
* reusable actions
* reusable dialogs
* reusable toasts

# Sistema Toast & Dialogs
**Integrado ✔**

**Reemplazado**
* **Anterior:** `alert()`, `confirm()`
* **Actual:** toast system, confirm dialogs

# Estado actual del módulo
## Nivel de madurez
| Área | Estado |
| :--- | :--- |
| **CRUD Projects** | ✔ Maduro |
| **CRUD Tasks** | ✔ Maduro |
| **CRUD Activities** | ✔ Maduro |
| **Attachments** | ✔ Maduro |
| **Audit Timeline** | ✔ Maduro |
| **Notifications** | ✔ Maduro |
| **Realtime** | ⚠️ Parcial |
| **Kanban visual** | 🚧 Pendiente |
| **Roles contextuales proyecto** | 🚧 Pendiente |

# Relaciones ORM actuales
```text
Users
 ├── Tasks (assigned)
 ├── Activities
 ├── ActivityAttachments
 └── Notifications

Projects
 └── Tasks

Tasks
 └── Activities

Activities
 └── Attachments
 ```

 # API actual
## Projects
* **GET** `/projects`
* **GET** `/projects/{id}`
* **POST** `/projects/create`
* **POST** `/projects/{id}/edit`
* **POST** `/projects/{id}/delete`

## Tasks
* **GET** `/tasks`
* **GET** `/tasks/{id}`
* **POST** `/tasks/create`
* **POST** `/tasks/{id}/edit`
* **POST** `/tasks/{id}/delete`

## Activities
* **GET** `/activities`
* **GET** `/activities/{id}`
* **POST** `/activities/create`
* **POST** `/activities/{id}/edit`
* **POST** `/activities/{id}/delete`

## Attachments
* **POST** `/activity-attachments/upload`
* **POST** `/activity-attachments/{id}/delete`
* **GET** `/activity-attachments/{id}/download`

# Próximas Evoluciones
## Corto plazo
* CSRF
* websocket reconnect
* cache invalidation
* drag & drop uploads

## Medio plazo
* `project_members`
* contextual project roles
* Kanban visual realtime
* activity comments

## Largo plazo
* collaborative editing
* cloud storage
* distributed realtime
* advanced workflow engine

# Arquitectura futura prevista
```text
Projects
 ├── Teams
 ├── Members
 ├── Kanban
 ├── Comments
 ├── Realtime Collaboration
 ├── File Storage
 └── Workflow Engine
 ```

 # Conclusión
El módulo de proyectos actualmente ya representa:
> **un sistema enterprise operativo real**

**Con:**
* arquitectura SSR moderna
* realtime parcial
* UI reusable madura
* auditoría integrada
* trazabilidad completa
* workflows organizativos reales
