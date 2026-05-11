# 00_MASTER_CONTEXT.md

## 🧠 Identidad del Proyecto

**Nombre:** Aula Robótica Platform
**Tipo:** Plataforma web administrativa (arquitectura centrada en IAM)
**Dominio:** Universidad / Aula de Robótica
**Propósito:** Sistema centralizado de identidad, control de acceso y gestión interna

---

## 🎯 Objetivo Principal

Proporcionar una plataforma **segura, escalable y modular** para gestionar:

* Usuarios
* Identidades de autenticación
* Roles y permisos (RBAC)
* Operaciones administrativas
* Módulos futuros (académicos y de robótica)

---

## 🧱 Alcance Actual

El sistema está centrado en el **núcleo IAM**, incluyendo:

* Autenticación (JWT + cookies HTTPOnly)
* Autorización (RBAC + permisos)
* Gestión de usuarios
* Gestión de roles
* Gestión de identidades
* Auditoría
* Dashboard administrativo (render server-side)

⚠️ Los módulos de negocio están en fase de integración.

---

## 🧩 Módulos Existentes

### Core (estables)

* auth
* auth_saml
* users
* roles
* identities
* dashboard
* audit

### Módulos emergentes

* students
* projects
* tasks
* activities

### Pendientes

* teams
* attachments

---

## 🏗️ Arquitectura

Arquitectura modular por capas:

Cliente → Jinja2 → FastAPI → Servicios → ORM → MariaDB

Principios:

* Separación de responsabilidades
* Modularidad por dominio
* Reutilización
* Seguridad por diseño

---

## 🔐 Seguridad

* JWT (access + refresh)
* Cookies HTTPOnly
* RBAC + permisos granulares
* Validación en backend
* Render condicional en frontend
* Auditoría de acciones

---

## 🗄️ Modelo de Datos (Resumen)

### Core IAM

* User
* Identity
* Role
* Permission
* AuditLog

### Gestión de proyectos

* Project
* Task
* Activity
* Team (pendiente)
* Attachment (pendiente)
* ProjectMember (nuevo)

---

## ⚙️ Stack Tecnológico

* Python
* FastAPI
* SQLAlchemy
* MariaDB
* Jinja2
* AdminLTE
* JWT
* bcrypt

---

## 📊 Estado del Proyecto

### Completado

* Sistema IAM completo
* Panel administrativo funcional
* RBAC operativo
* Auditoría

### En progreso

* Integración módulo proyectos
* Refactor de templates y routers
* Alineación arquitectónica

### Reciente

* Modelo de gestión de proyectos
* Testing (~85% cobertura)
* CI/CD (GitHub Actions + SonarQube)

---

## 🚧 Foco Actual

* Completar Teams y Attachments
* Refactor de módulos nuevos
* Unificación de UI (macros Jinja)
* Integración completa de proyectos

---

## ⚠️ Riesgos

* Inconsistencias entre módulos nuevos y antiguos
* Divergencia en templates
* Integración parcial del sistema de proyectos
* Huecos en permisos contextuales

---

## 🔮 Visión

Evolucionar hacia una plataforma completa:

* Gestión académica
* Proyectos de robótica
* Equipos y competiciones
* Inventario y reservas
* OAuth / SSO
* Despliegue en producción

---

## 📌 Decisiones clave

* Separación Usuario / Identidad
* JWT en cookies (no localStorage)
* RBAC + permisos
* Render server-side
* Arquitectura modular

---

## 🧭 Uso de este documento

Este archivo sirve como:

* Contexto global del proyecto
* Punto de entrada para desarrollo
* Base para asistencia técnica (IA)
* Resumen de arquitectura

Mantenerlo **actualizado y conciso**
