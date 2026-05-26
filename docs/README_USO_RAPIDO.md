# README_USO_RAPIDO.md

# Aula Robótica Platform — Guía de Uso Rápido

## 1. Introducción

Aula Robótica Platform es una plataforma web colaborativa desarrollada para la gestión del Aula de Robótica de la Escuela Politécnica Superior de la Universidad de Alcalá.

El sistema integra funcionalidades de:

* gestión de usuarios e identidades,
* control de acceso basado en roles y permisos (IAM/RBAC),
* gestión colaborativa de proyectos,
* gestión de tareas y actividades,
* notificaciones,
* auditoría,
* dashboard de monitorización,
* sincronización realtime mediante WebSockets.

La aplicación está desarrollada con:

* FastAPI,
* SQLAlchemy,
* MariaDB,
* Jinja2 SSR,
* AdminLTE,
* WebSockets,
* JWT + Cookies HTTPOnly.

---

# 2. Acceso a la plataforma

## Login

Acceder mediante:

```text
/auth/login
```

Introducir:

* usuario/email,
* contraseña.

Tras autenticarse correctamente, el sistema redirige automáticamente al dashboard principal.

---

# 3. Dashboard principal

El dashboard proporciona una visión general del sistema.

Dependiendo del rol del usuario, se muestran diferentes métricas y funcionalidades.

## Información mostrada

### Administradores

* usuarios registrados,
* roles,
* identidades,
* proyectos activos,
* tareas,
* actividad reciente,
* logs de auditoría,
* feed de actividad.

### Estudiantes / Coordinadores

* proyectos asignados,
* tareas pendientes,
* progreso,
* actividad reciente,
* notificaciones.

---

# 4. Gestión de usuarios

## Acceso

```text
/users
```

## Funcionalidades

* listado de usuarios,
* alta de usuarios,
* edición,
* activación/desactivación,
* asignación de roles,
* visualización de detalle.

## Roles habituales

* Administrador,
* Profesor,
* Coordinador,
* Estudiante.

---

# 5. Gestión de identidades

## Acceso

```text
/identities
```

## Funcionalidades

* gestión de identidades locales,
* proveedores externos,
* asociación usuario-identidad,
* soporte preparado para SAML/SSO.

---

# 6. Gestión de proyectos

## Acceso

```text
/projects
```

## Funcionalidades

* creación de proyectos,
* edición,
* asignación de miembros,
* visualización de estado,
* seguimiento colaborativo.

Cada proyecto incluye:

* miembros,
* tareas,
* actividades,
* feed de actividad,
* notificaciones.

---

# 7. Gestión de tareas

Las tareas forman parte de cada proyecto.

## Funcionalidades

* creación,
* edición,
* asignación,
* prioridades,
* estados,
* seguimiento.

## Estados Kanban

* To Do,
* Doing,
* Done.

---

# 8. Kanban realtime

El sistema incorpora sincronización realtime mediante WebSockets.

Cuando un usuario modifica una tarea:

1. el backend valida permisos,
2. actualiza base de datos,
3. emite evento realtime,
4. el resto de clientes se sincronizan automáticamente.

Esto permite colaboración simultánea entre varios usuarios.

---

# 9. Registro de actividades

## Funcionalidades

* creación de actividades,
* registro de tiempo,
* descripción técnica,
* adjuntos,
* histórico.

Las actividades quedan asociadas a proyectos y usuarios.

---

# 10. Sistema de notificaciones

## Acceso

```text
/notifications
```

## Funcionalidades

* notificaciones realtime,
* tareas asignadas,
* cambios de estado,
* actividad reciente,
* marcado como leído.

---

# 11. Seguridad e IAM

La plataforma implementa:

* autenticación JWT,
* cookies HTTPOnly,
* RBAC contextual,
* control granular de permisos,
* auditoría de acciones,
* middleware de seguridad.

## Arquitectura IAM

El sistema permite:

* roles globales,
* roles contextuales por proyecto,
* permisos efectivos dinámicos.

---

# 12. Calidad software

El proyecto incorpora:

* testing automatizado,
* cobertura superior al 75%,
* integración CI/CD,
* SonarQube Cloud,
* Ruff,
* arquitectura modular,
* principios SOLID,
* Clean Code.

---

# 13. Ejecución local

## Requisitos

* Python 3.13+
* MariaDB/MySQL
* uv

## Instalación

```bash
uv sync
```

## Variables de entorno

Configurar:

```text
.env
```

con:

* base de datos,
* JWT secret,
* configuración aplicación.

## Lanzar servidor

```bash
uv run uvicorn app.main:app --reload
```

---

# 14. Testing

## Ejecutar tests

```bash
uv run pytest
```

## Cobertura

```bash
uv run pytest --cov=app --cov-report=html
```

---

# 15. Documentación adicional

El proyecto incluye documentación técnica extensa en:

```text
/docs
```

Incluyendo:

* arquitectura,
* seguridad,
* IAM,
* módulos,
* decisiones técnicas,
* despliegue,
* testing,
* evolución del proyecto.

---

# 16. Estado actual del proyecto

Actualmente el sistema incluye:

* arquitectura modular completa,
* SSR + realtime,
* IAM/RBAC contextual,
* proyectos colaborativos,
* Kanban realtime,
* auditoría,
* notificaciones,
* testing automatizado,
* CI/CD,
* integración preparada para SAML/SSO.

---

# 17. Autor

Fran Ramírez Martín

CFGS Desarrollo de Aplicaciones Multiplataforma (DAM)

Escuela Politécnica Superior — Universidad de Alcalá
