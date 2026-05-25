# 10_RBAC_CONTEXTUAL.md

# RBAC y Autorización Contextual

## Propósito

Este documento describe la arquitectura de autorización de Aula Robótica Platform.

El sistema combina:

- RBAC global,
- permisos granulares,
- autorización contextual por proyecto,
- ownership,
- autorización SSR visual,
- políticas reutilizables,
- helpers centralizados.

El objetivo es construir una arquitectura enterprise flexible y escalable. 

---

# Filosofía de diseño

La autorización del sistema sigue varios principios:

## 1. Desacoplamiento

Autenticación y autorización son sistemas independientes.

```text
Authentication → quién eres
Authorization → qué puedes hacer
```

---

## 2. Permisos atómicos

Los permisos son independientes de los roles.

Ejemplo:

```text
projects:update
tasks:create
activities:delete
```

---

## 3. Roles como agregadores

Los roles simplemente agrupan permisos.

---

## 4. Contextualización

El acceso depende también del contexto:

- proyecto,
- ownership,
- pertenencia,
- coordinación,
- relaciones funcionales.

---

## 5. Backend-first security

La seguridad real SIEMPRE se valida en backend.

El frontend SSR solo mejora UX.

---

# Arquitectura General

La autorización actual combina:

```text
JWT Permissions
        +
RBAC Global
        +
Project Membership
        +
Ownership
        +
Policies
        +
SSR Contextual Authorization
```

---

# Componentes Principales

## Núcleo RBAC

### User
### Role
### Permission
### UserRole
### RolePermission

---

## Autorización contextual

### ProjectMember
### ProjectRoleEnum

---

## Policies reutilizables

### can_user_action()
### can_manage_tasks()
### can_view_activity()

---

# Modelo RBAC Global

## Usuarios

Los usuarios representan personas del sistema. :contentReference[oaicite:0]{index=0}

No contienen credenciales.

Las credenciales viven en `Identity`.

---

## Identidades

Las identidades representan autenticación. :contentReference[oaicite:1]{index=1}

Permiten:

- login local,
- OAuth futuro,
- SAML futuro,
- múltiples providers.

---

## Roles

Los roles representan perfiles funcionales globales. :contentReference[oaicite:2]{index=2}

Ejemplos:

```text
admin
profesor
estudiante
```

---

## Permisos

Los permisos representan acciones específicas. :contentReference[oaicite:3]{index=3}

Formato estándar:

```text
resource:action
```

Ejemplos:

```text
users:read
projects:create
activities:update
tasks:delete
```

---

# Relación Usuario ↔ Rol

La relación es many-to-many mediante:

```text
user_rol
```

:contentReference[oaicite:4]{index=4}

Esto permite:

- múltiples roles por usuario,
- reutilización,
- evolución futura,
- granularidad enterprise.

---

# Relación Rol ↔ Permiso

La relación también es many-to-many mediante:

```text
role_permissions
```

:contentReference[oaicite:5]{index=5}

Esto desacopla:

```text
roles
≠
permissions
```

---

# Roles Globales Actuales

## admin

Acceso total del sistema.

Bypass global de autorización.

---

## profesor

Acceso funcional de gestión académica.

---

## estudiante

Acceso operativo limitado.

---

# Roles Globales Futuros

Arquitectura preparada para:

```text
coordinador
gestor
auditor
operador
supervisor
```

---

# Jerarquía de Roles

Existe jerarquía conceptual de roles. :contentReference[oaicite:6]{index=6}

```python
ROLE_HIERARCHY = {
    "admin": 4,
    "profesor": 3,
    "coordinator": 2,
    "estudiante": 1
}
```

Actualmente se usa principalmente para validaciones simples.

---

# Permisos Efectivos

Los permisos efectivos pueden derivarse desde:

- JWT,
- roles,
- relaciones contextuales.

---

## Helper principal

```python
get_permissions_from_roles()
```

:contentReference[oaicite:7]{index=7}

---

# RBAC basado en JWT

Tras autenticación, el JWT contiene:

```json
{
  "roles": [...],
  "permissions": [...]
}
```

Esto permite:

- reducir queries,
- SSR rápido,
- validación ligera,
- render contextual inmediato.

---

# Arquitectura Contextual

El RBAC global no es suficiente para un sistema colaborativo.

Por eso existe autorización contextual.

---

# Project Membership

Los proyectos usan:

```text
project_members
```

:contentReference[oaicite:8]{index=8}

Cada relación incluye:

```text
project_id
user_id
role
```

---

# Roles Contextuales de Proyecto

## coordinator

Puede:

- gestionar tareas,
- coordinar miembros,
- administrar flujo operativo,
- supervisar actividad.

---

## member

Puede:

- participar,
- ejecutar tareas,
- registrar actividad,
- subir adjuntos.

---

# Diferencia entre Roles Globales y Contextuales

## Roles Globales

Aplican a TODO el sistema.

Ejemplo:

```text
admin
profesor
```

---

## Roles Contextuales

Aplican SOLO dentro de un proyecto.

Ejemplo:

```text
coordinator
member
```

---

# Arquitectura Desacoplada

Esto es extremadamente importante.

Los roles contextuales NO dependen del RBAC global.

Esto evita:

- explosión de roles,
- acoplamiento,
- complejidad exponencial.

---

# Policies reutilizables

La autorización contextual vive principalmente en:

```text
app/core/authorization/
```

---

# Policies principales

## can_user_action()

Policy unificada principal. :contentReference[oaicite:9]{index=9}

Combina:

- roles,
- permisos,
- ownership,
- proyecto,
- coordinación.

---

# Flujo interno de autorización

```text
Admin bypass
    ↓
Permiso global
    ↓
Contexto proyecto
    ↓
Ownership
    ↓
Denegar
```

---

# Admin Bypass

Los administradores tienen acceso total.

```python
if "admin" in roles:
    return True
```

:contentReference[oaicite:10]{index=10}

---

# Permisos Globales

Validación estándar:

```python
permission_name = f"{resource}:{action}"
```

---

# Contexto Proyecto

Para tareas y proyectos:

- membership,
- coordinación,
- ownership contextual.

---

# Ejemplo Task Authorization

## Lectura

```text
Miembro del proyecto
```

---

## Escritura

```text
Coordinator del proyecto
```

---

# Ownership

Existe fallback ownership:

```python
if action in ["read", "update"] and user_id == target_id:
```

:contentReference[oaicite:11]{index=11}

---

# Project Permissions Helpers

Helpers especializados: :contentReference[oaicite:12]{index=12}

```python
is_project_member()
is_project_coordinator()
can_manage_project()
can_manage_tasks()
user_in_project()
```

---

# Task Permissions

Sistema especializado para tareas. :contentReference[oaicite:13]{index=13}

Incluye:

```python
can_view_task()
ensure_can_view_task()
```

---

# Activity Permissions

Sistema especializado para actividades. :contentReference[oaicite:14]{index=14}

Incluye:

```python
can_view_activity()
ensure_can_view_activity()
```

---

# Reglas Actuales de Actividades

## admin

Acceso total.

---

## estudiante

Solo actividades propias.

---

## profesor/coordinator

Actividades de proyectos donde participa.

---

# Dependencias FastAPI

La capa HTTP usa guards reutilizables.

Ejemplos:

```python
require_permission_web()
require_roles_web()
require_owner_or_permission_web()
```

---

# Frontend Authorization SSR

El frontend implementa autorización visual contextual.

NO es seguridad real.

Es UX contextual.

---

# Helpers SSR disponibles

```python
has_role()
has_perm()
can()
is_owner()
is_project_coordinator()
```

---

# Capacidades SSR

## Ocultación contextual

Botones.

---

## Navegación dinámica

Menús filtrados por permisos.

---

## Renderizado condicional

Tabs, acciones, formularios.

---

## Contexto dinámico

Detail layouts adaptativos.

---

# Ejemplo SSR

```jinja2
{% if has_perm("projects:update") %}
```

---

# Arquitectura Enterprise

El sistema ya implementa patrones enterprise reales:

- RBAC desacoplado,
- autorización contextual,
- ownership,
- policy engine,
- permisos granulares,
- SSR contextual,
- reusable guards.

---

# Beneficios de la Arquitectura

## Escalabilidad

Puede crecer a cientos de permisos.

---

## Flexibilidad

Roles y contexto desacoplados.

---

## Seguridad

Validación backend centralizada.

---

## Reutilización

Policies reutilizables.

---

## Bajo acoplamiento

Frontend desacoplado del backend.

---

## Evolución futura

Preparado para:

- multi-tenant,
- organizaciones,
- departamentos,
- jerarquías complejas,
- SSO institucional.

---

# Limitaciones Actuales

## Policies dispersas

Algunas reglas siguen repartidas entre módulos.

---

## No existe Policy Engine formal

Todavía no hay motor declarativo completo.

---

## No existe ABAC completo

Aún no se usan atributos avanzados.

---

## No existe cache de autorización

Cada request recalcula permisos.

---

# Evolución futura

## ABAC híbrido

```text
RBAC + atributos + contexto
```

---

## Policy registry

Centralizar todas las policies.

---

## Permission caching

Reducir carga en render SSR.

---

## Multi-organization support

Permisos por organización.

---

## Dynamic permission inheritance

Herencia contextual avanzada.

---

# Resumen

La plataforma implementa actualmente una arquitectura híbrida moderna:

```text
JWT + RBAC + Contextual Authorization + Ownership + SSR Authorization
```

El sistema ya supera ampliamente un CRUD académico tradicional y se aproxima a arquitecturas enterprise reales de:

- internal admin platforms,
- operations systems,
- collaborative management tools,
- educational enterprise platforms.