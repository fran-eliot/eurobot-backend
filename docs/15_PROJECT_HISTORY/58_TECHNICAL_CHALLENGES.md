# 58_TECHNICAL_CHALLENGES.md

## 1. JWT + Cookies HTTPOnly + SSR

### Problema
Integrar autenticación segura basada en JWT en un entorno SSR con Jinja2 y AdminLTE.

### Dificultad
La mayoría de ejemplos y arquitecturas modernas trabajan con SPA y localStorage.
El sistema requería:
- SSR,
- cookies seguras,
- protección CSRF,
- expiración controlada,
- compatibilidad FastAPI.

### Solución aplicada
Se implementó:
- JWT firmado,
- cookies HTTPOnly,
- middleware de autenticación,
- dependencias FastAPI,
- resolución contextual de usuario.

### Aprendizajes
- SSR requiere estrategias distintas a SPA.
- Seguridad y usabilidad deben equilibrarse.
- JWT no implica necesariamente frontend SPA.

---

## 2. RBAC contextual

### Problema
Un mismo usuario podía necesitar distintos permisos según el método de autenticación.

### Dificultad
El RBAC clásico no cubría este escenario.

### Solución aplicada
Separación conceptual:
- Usuario,
- Identidad,
- Rol.

Y creación de:
`Rol contextual asociado a identidad`

### Resultado
Sistema híbrido:
- RBAC global,
- RBAC contextual.

---

## 3. Evolución desde CRUD tradicional

### Problema
La estructura inicial comenzaba a generar acoplamiento.

### Solución
Refactor completo hacia:
- routers desacoplados,
- service layer,
- security layer,
- helpers reutilizables.

### Resultado
Arquitectura más mantenible y escalable.

---

## 4. Sistema realtime con WebSockets

### Problema
Sincronizar cambios Kanban entre múltiples usuarios.

### Solución
Implementación de:
- rooms por proyecto,
- eventos realtime,
- actualización dinámica,
- auditoría sincronizada.

---

## 5. Gestión de permisos complejos

### Problema
Los permisos dejaron de ser únicamente globales.

### Solución
Sistema contextual basado en:
- ownership,
- roles,
- contexto de proyecto,
- permisos dinámicos.
