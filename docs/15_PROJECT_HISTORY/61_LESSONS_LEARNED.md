# 61_LESSONS_LEARNED.md

## 1. La arquitectura importa desde el inicio
Las decisiones tempranas condicionan enormemente la evolución futura.

## 2. Separar responsabilidades simplifica escalabilidad
Separar:
- autenticación,
- autorización,
- lógica,
- persistencia,

reduce complejidad futura.

## 3. Un buen modelo de datos cambia todo el sistema
El modelo Usuario–Identidad–Rol permitió evolucionar el sistema sin rehacer arquitectura.

## 4. La seguridad debe diseñarse desde el principio
JWT, hashing, permisos y control contextual no deben añadirse al final.

## 5. Los proyectos reales cambian constantemente
El cambio desde Eurobot hacia Aula de Robótica obligó a replantear:
- alcance,
- arquitectura,
- objetivos.

## 6. El realtime introduce complejidad adicional
WebSockets y sincronización añaden retos:
- concurrencia,
- consistencia,
- actualización visual,
- auditoría.

## 7. La mantenibilidad es tan importante como las funcionalidades
El sistema debía poder mantenerse por futuros estudiantes y desarrolladores.