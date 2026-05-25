# 57_PROJECT_EVOLUTION.md

## 1. Contexto inicial del proyecto

El proyecto se desarrolla durante la Formación en Centro de Trabajo (FCT) del CFGS de Desarrollo de Aplicaciones Multiplataforma (DAM) en el Aula de Robótica de la Escuela Politécnica Superior de la Universidad de Alcalá (EPS-UAH).

Antes del inicio formal de las prácticas se realizó un análisis previo del ecosistema tecnológico asociado al Aula de Robótica y a la competición Eurobot Spain, estudiando tanto la web pública como las necesidades operativas derivadas de la organización de competiciones, gestión de equipos y administración de usuarios.

A partir de dicho análisis se elaboró una primera propuesta de valor centrada inicialmente en el desarrollo de una infraestructura de autenticación y autorización para Eurobot Spain.

---

## 2. Objetivo inicial del proyecto

El alcance inicial del proyecto consistía en desarrollar una API REST para la gestión de usuarios y autenticación del sistema Eurobot Spain.

El sistema debía proporcionar:

- gestión de usuarios,
- autenticación segura,
- control de acceso basado en roles,
- persistencia estructurada,
- seguridad mediante JWT,
- base tecnológica reutilizable.

Desde las primeras fases se adoptaron decisiones arquitectónicas avanzadas:

- separación entre Usuario, Identidad y Rol,
- autenticación basada en JWT,
- arquitectura FastAPI,
- persistencia mediante MariaDB,
- uso de SQLAlchemy ORM,
- interfaz SSR mediante Jinja2 y AdminLTE.

El modelo conceptual inicial ya incorporaba un enfoque claramente escalable y desacoplado.

---

## 3. Cambio de alcance del proyecto

Durante las primeras semanas de desarrollo se produjo una redefinición importante del alcance funcional y arquitectónico del sistema.

Tras reuniones y coordinación con el equipo técnico y responsables del Aula de Robótica, se decidió evolucionar desde un sistema centrado exclusivamente en Eurobot Spain hacia una plataforma transversal para el Aula de Robótica completa.

La motivación principal fue:

- construir una infraestructura reutilizable,
- desacoplar la autenticación de módulos concretos,
- permitir reutilización futura,
- facilitar crecimiento modular,
- crear una base sólida de seguridad.

Este cambio transformó completamente la naturaleza del proyecto:

```text
De:
Sistema IAM para competición robótica

A:
Plataforma modular para el Aula de Robótica
```

---

## 4. Evolución arquitectónica

### 4.1 Arquitectura inicial
Desde el inicio se definió una arquitectura separada entre:
- Web Routers (SSR),
- API Routers,
- capa de servicios,
- capa de seguridad,
- persistencia ORM.

La separación entre rutas web y API fue una decisión deliberada desde el principio, permitiendo desacoplar:
- renderizado SSR,
- consumo API,
- lógica de negocio,
- autenticación,
- autorización.

La arquitectura final quedó estructurada en capas claramente diferenciadas:
- Browser/AdminLTE
- FastAPI
- Web Routers
- API Routers
- Service Layer
- Security Layer
- SQLAlchemy ORM

### 4.2 Evolución hacia arquitectura modular
En las primeras versiones existía una organización más cercana a un CRUD tradicional.
Posteriormente se realizó un refactor importante para evolucionar hacia una arquitectura modular y reutilizable basada en:
- separación por dominios,
- servicios desacoplados,
- permisos reutilizables,
- dependencias de seguridad,
- helpers contextuales,
- middleware de autenticación.

Este cambio permitió:
- reducir acoplamiento,
- facilitar escalabilidad,
- mejorar mantenibilidad,
- reutilizar lógica de permisos y seguridad.

### 4.3 Evolución del sistema IAM
Uno de los elementos más importantes del proyecto fue el diseño del modelo:
`Usuario → Identidad → Rol`

El sistema separa:
- actor lógico,
- credencial,
- autorización.

Esto permitió soportar:
- múltiples métodos de autenticación,
- roles globales,
- roles contextuales,
- futura integración OAuth/SSO.

La arquitectura evolucionó posteriormente hacia un RBAC híbrido/contextual.

---

## 5. Evolución funcional

### 5.1 Sistema IAM inicial
Las primeras funcionalidades implementadas fueron:
- login JWT,
- hashing bcrypt,
- gestión de usuarios,
- gestión de identidades,
- gestión de roles,
- panel administrativo SSR,
- control RBAC.

### 5.2 Incorporación del sistema de auditoría
Aunque inicialmente no estaba previsto, el crecimiento del dashboard administrativo hizo necesaria la incorporación de:
- trazabilidad,
- logging estructurado,
- registro de acciones,
- auditoría de eventos críticos.

El sistema de auditoría pasó a convertirse en un componente transversal de la plataforma.

### 5.3 Gestión de proyectos
Posteriormente el sistema dejó de ser únicamente un IAM y evolucionó hacia una plataforma operativa completa.
Se incorporaron nuevos dominios:
- proyectos,
- equipos,
- tareas,
- actividades,
- adjuntos,
- seguimiento temporal.

Esto supuso un salto importante de complejidad funcional.

### 5.4 Sistema Kanban y tiempo real
A petición del supervisor se incorporó posteriormente un sistema Kanban para la gestión visual de tareas.
La necesidad de sincronización entre usuarios llevó a implementar:
- WebSockets,
- actualización en tiempo real,
- notificaciones,
- sincronización de estados,
- auditoría realtime.

El sistema realtime apareció en fases avanzadas del proyecto, aproximadamente a finales de abril de 2026.

---

## 6. Estado final del proyecto
El resultado final es una plataforma modular compuesta por:
- sistema IAM avanzado,
- backend FastAPI,
- autenticación JWT segura,
- RBAC contextual,
- dashboard SSR,
- sistema de auditoría,
- gestión de proyectos,
- Kanban realtime,
- arquitectura desacoplada,
- servicios reutilizables.

El sistema está diseñado para evolucionar hacia:
- OAuth2,
- SSO institucional,
- permisos avanzados,
- multi-tenant,
- módulos funcionales adicionales.