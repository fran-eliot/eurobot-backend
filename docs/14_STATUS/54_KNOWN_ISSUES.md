# 54_KNOWN_ISSUES.md

# 🧠 Known Issues, Riesgos y Deuda Técnica

# 🎯 Propósito

Este documento recoge:

- problemas reales conocidos,
- deuda técnica actual,
- limitaciones arquitectónicas,
- riesgos futuros,
- decisiones pendientes.

Su objetivo es:

- evitar regresiones,
- priorizar refactors,
- mantener visión técnica realista,
- acelerar debugging,
- documentar riesgos enterprise.

---

# 📊 Estado General de Salud Técnica

| Área | Estado |
|---|---|
| IAM | Muy estable |
| UI Architecture | Estable |
| Realtime | Parcialmente estable |
| WebSockets | Necesita maduración |
| Frontend JS | En transición |
| Seguridad | Buena pero incompleta |
| Cache | Poco madura |
| Testing | Bueno pero incompleto |
| Performance | Correcta |
| UX consistency | Mejorable |

---

# 🚨 BLOQUE 1 — Riesgos Arquitectónicos Reales

# 1. Falta de autorización contextual madura por proyecto

# Problema

Actualmente el sistema posee:

- RBAC global sólido,
- helpers contextuales parciales.

Pero aún falta:

- project_members formal,
- roles contextuales completos,
- ownership avanzado.

---

# Impacto

- permisos parcialmente implícitos,
- lógica dispersa,
- difícil escalabilidad colaborativa.

---

# Estado

🟠 Alto

---

# 2. Arquitectura realtime aún parcialmente fragmentada

# Problema

Existen múltiples flujos websocket:

- dashboard,
- notifications,
- timelines,
- feeds.

Pero no existe aún:

```text 
Event Bus unificado
```

### Impacto
* duplicación de lógica
* handlers inconsistentes
* mayor complejidad de mantenimiento

**Estado:** 🟠 Alto

---

# 🟠 Estado
3. Falta de estrategia formal de cache invalidation
## Problema
Actualmente:
* no existe cache centralizada,
* no existe invalidación coordinada,
* algunos renders realizan queries redundantes.

## Impacto
* render costoso,
* posibles inconsistencias,
* escalabilidad limitada.

# 🟠 Estado
⚠️ BLOQUE 2 — Seguridad
4. CSRF no implementado formalmente
## Problema
El sistema usa:
* cookies HTTPOnly,
* JWT SSR,
* formularios POST.

Pero no existe protección CSRF formal.

## Impacto
* vulnerabilidad potencial en producción.

# 🔴 Crítico
5. Refresh Token Rotation pendiente
## Problema
Los refresh tokens actualmente:
* son persistentes,
* no rotan automáticamente.

## Impacto
* riesgo si el token es comprometido.

# 🟡 Medio
6. WebSocket authentication hardening incompleto
## Problema
La autenticación websocket funciona correctamente.
Pero faltan:
* refresh handling,
* reconexión segura,
* invalidación avanzada.

## Impacto
* posibles sesiones huérfanas,
* inconsistencias realtime.

# 🟠 Alto
🧩 BLOQUE 3 — Frontend Architecture
7. Frontend JS aún parcialmente no modularizado
## Problema
La arquitectura JS evolucionó mucho.
Pero aún persisten:
* scripts legacy,
* handlers inline,
* fragmentos acoplados.

## Impacto
* mantenimiento complejo,
* difícil testing frontend,
* riesgo de regresiones UI.

# 🟠 Alto
8. UX consistency parcial
## Problema
La UI moderna ya implementa:
* toasts,
* confirm dialogs,
* reusable actions.

Pero aún sobreviven fragmentos antiguos:
* alert(),
* confirm(),
* layouts legacy.

## Impacto
* UX inconsistente,
* experiencia visual desigual.

# 🟡 Medio
9. Inconsistencias visuales menores entre módulos
## Problema
Algunos módulos evolucionaron más rápido que otros.
Existen diferencias en:
* spacing,
* headers,
* detail layouts,
* action bars.

## Impacto
* pérdida de cohesión visual.

# 🟡 Medio
🔌 BLOQUE 4 — Realtime & WebSockets
10. Race conditions potenciales en realtime
## Problema
Múltiples eventos websocket podrían:
* llegar fuera de orden,
* sobrescribir estado visual,
* duplicar renderizados.

Casos posibles:
* timelines,
* notifications,
* dashboard updates,
* Kanban futuro.

## Impacto
* inconsistencias UI realtime.

# 🟠 Alto
11. Reconexión websocket incompleta
## Problema
Actualmente:
* websocket conecta correctamente,
* pero la reconexión automática es básica.

Faltan:
* retry strategy,
* exponential backoff,
* resync de estado.

## Impacto
* pérdida parcial de realtime.

# 🟠 Alto
12. Realtime no desacoplado completamente del DOM
## Problema
Algunas actualizaciones websocket:
* manipulan DOM directamente,
* mezclan lógica UI + eventos.

## Impacto
* difícil evolución,
* difícil testing.

# 🟡 Medio
🧱 BLOQUE 5 — Backend Architecture
13. Servicios aún parcialmente distribuidos
## Problema
Gran parte de la lógica ya está desacoplada.
Pero algunos routers aún contienen:
* validaciones,
* lógica contextual,
* render preparation.

## Impacto
* menor mantenibilidad,
* testing más difícil.

# 🟠 Alto
14. Naming inconsistency histórica
## Problema
Persisten mezclas históricas:
* id_user
* user_id
* id_usuario

## Impacto
* fricción cognitiva,
* errores sutiles.

# 🟡 Medio
15. Queries complejas en detail layouts
## Problema
Algunos detail views generan:
* múltiples joins,
* queries repetidas,
* eager loading costoso.

## Impacto
* performance degradable.

# 🟡 Medio
🧪 BLOQUE 6 — Testing
16. Cobertura realtime incompleta
## Problema
Faltan tests de:
* websockets,
* realtime flows,
* timeline sync.

## Impacto
* bugs difíciles de detectar.

# 🟠 Alto
17. Falta testing frontend real
## Problema
No existen aún:
* UI tests,
* interaction tests,
* visual regression tests.

## Impacto
* regresiones UX posibles.

# 🟡 Medio
🌐 BLOQUE 7 — API & Evolución
18. API aún no versionada
## Problema
No existe:
* /api/v1

## Impacto
* evolución futura compleja.

# 🟡 Medio
19. Mezcla parcial SSR/API responsibilities
## Problema
Algunos endpoints mezclan:
* render SSR,
* lógica API,
* preparación frontend.

## Impacto
* desacoplamiento incompleto.

# 🟡 Medio
📎 BLOQUE 8 — Attachments & Storage
20. Sistema de almacenamiento local
## Problema
Los attachments actualmente usan:
* filesystem local

## Limitaciones
* no distribuido,
* no cloud-native,
* no scalable storage.

# 🟡 Medio
21. Falta estrategia avanzada de limpieza
## Problema
No existe aún:
* cleanup automático,
* orphan detection,
* retention policies.

## Impacto
* crecimiento innecesario almacenamiento.

# 🟡 Medio
🔔 BLOQUE 9 — Notifications
22. Notifications parcialmente desacopladas
## Problema
El sistema funciona correctamente.
Pero aún falta:
* event bus central,
* queue architecture,
* batching.

## Impacto
* escalabilidad limitada.

# 🟡 Medio
🎨 BLOQUE 10 — UI Evolution
23. Sistema UI aún en transición hacia Design System formal
## Problema
La UI ya actúa como mini design system.
Pero aún faltan:
* tokens visuales,
* documentación formal,
* naming conventions completas.

## Impacto
* crecimiento frontend menos controlado.

# 🟡 Medio
24. Falta estrategia HTMX/Turbo
## Problema
Actualmente:
* SSR funciona muy bien,
* realtime parcial también.

Pero no existe aún estrategia híbrida clara.

## Impacto
* ciertas interacciones requieren reload completo.

# 🟡 Medio
📌 Problemas YA resueltos (importante)
Estos problemas YA NO deben considerarse pendientes:
✔ Resueltos:
* attachments implementados
* assigned_to implementado
* task status implementado
* activities maduras
* realtime audit timeline
* reusable macros
* toast system
* confirm dialogs
* detail layouts modernos
* notifications realtime
* dashboard avanzado

🚀 Riesgo Estratégico Principal Actual
## Riesgo real
El principal riesgo ya NO es IAM.
Ahora es:
* Escalabilidad arquitectónica del ecosistema realtime + frontend

🧠 Prioridades Técnicas Reales
## Corto plazo
* CSRF
* websocket reconnection
* contextual authorization
* JS modularization

## Medio plazo
* cache strategy
* realtime event bus
* frontend testing
* API versioning

## Largo plazo
* distributed architecture
* cloud storage
* hybrid SSR architecture
* collaborative realtime

📈 Estado Final Real
El sistema actualmente es:
* Arquitectónicamente sólido pero entrando en fase de complejidad enterprise

🎯 Conclusión
Los problemas actuales ya no son:
* CRUD básicos,
* autenticación,
* arquitectura inicial.

Ahora son problemas de:
* escalabilidad,
* realtime consistency,
* frontend architecture,
* evolución enterprise.

## Issues pendientes conocidos

- Integración SAML pendiente de coordinación con servicios informáticos UAH.
- Despliegue Docker planificado pero no finalizado.
- Coverage gate SonarCloud limitado por restricciones del plan gratuito.
- Persistencia definitiva de entorno productivo pendiente de despliegue VPS.