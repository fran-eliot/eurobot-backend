# Aula Robótica Platform

## Descripción general

Aula Robótica Platform es una plataforma web modular diseñada para la gestión integral del Aula de Robótica de la Escuela Politécnica Superior de la Universidad de Alcalá.

El sistema combina:

- gestión académica
- gestión de proyectos colaborativos
- control de usuarios y permisos
- auditoría
- sincronización en tiempo real

Todo ello bajo una arquitectura moderna basada en FastAPI y renderizado server-side.

---

# Objetivos del proyecto

## Objetivos funcionales

- Gestión centralizada de usuarios
- Control de identidades y roles
- Gestión de estudiantes
- Gestión de proyectos colaborativos
- Gestión de tareas y actividades
- Auditoría de acciones
- Colaboración en tiempo real

## Objetivos técnicos

- Arquitectura modular
- Seguridad por diseño
- Escalabilidad
- Mantenibilidad
- Reutilización de componentes
- Preparación para SSO/SAML

---

# Características principales

## Gestión IAM / RBAC

- Roles globales
- Permisos granulares
- Roles contextuales por proyecto
- Policies reutilizables

## Gestión de proyectos

- Creación de proyectos
- Equipos colaborativos
- Coordinadores de proyecto
- Gestión Kanban

## Realtime

- WebSockets por proyecto
- Timeline realtime
- Kanban sincronizado
- Presencia de usuarios

## Auditoría

- Logs centralizados
- Timeline visual
- Trazabilidad completa

---

# Estado actual

Actualmente el proyecto se encuentra en una fase avanzada de consolidación arquitectónica y ampliación funcional.

Las áreas más maduras son:

- IAM / Seguridad
- Gestión de usuarios
- Gestión de proyectos
- Tasks + Kanban
- Auditoría realtime

---

# Evolución futura prevista

- Integración SAML / SSO
- Dashboard avanzado
- Competiciones
- API pública
- Tests automatizados
- Dockerización
- CI/CD