# 56_TECHNICAL_DEBT.md

# Technical Debt

# Objetivo

Este documento describe la deuda técnica actual de Aula Robótica Platform.

La deuda técnica NO se considera únicamente un problema.

En muchos casos representa:

- decisiones conscientes,
- trade-offs estratégicos,
- velocidad de iteración,
- priorización arquitectónica,
- evolución incremental.

---

# Filosofía

La plataforma sigue una estrategia:

```text
architecture-first incremental evolution
```

Esto implica aceptar temporalmente ciertas deudas para priorizar:

- arquitectura,
- realtime,
- IAM,
- modularidad,
- UX,
- validación conceptual.

---

# Estado General

La plataforma ya posee una arquitectura sorprendentemente madura en múltiples áreas:

- RBAC,
- SSR architecture,
- realtime foundations,
- reusable UI,
- dashboards,
- activity feed,
- contextual authorization.

Sin embargo, también existen áreas donde la complejidad ha crecido rápidamente y requieren consolidación.

---

# Tipos de Deuda Técnica

La deuda actual puede dividirse en:

# Deuda Consciente

Aceptada deliberadamente para avanzar más rápido.

---

# Deuda Arquitectónica

Resultado del crecimiento de complejidad.

---

# Deuda Operacional

Pendientes DevOps/infraestructura.

---

# Deuda Realtime

Asociada a sincronización y colaboración live.

---

# Deuda Frontend

Principalmente relacionada con modularización JS y SSR híbrido.

---

# Áreas Más Frágiles Actualmente

# 1. JS Inline

Actualmente todavía existe JavaScript inline distribuido en:

- templates,
- formularios,
- realtime handlers,
- dialogs,
- interactions contextuales.

---

# Problemas

- duplicación,
- mantenimiento complejo,
- coupling template/JS,
- testing difícil.

---

# Impacto

Especialmente visible en:

- project_detail,
- attachments,
- realtime handlers.

---

# Estado Arquitectónico

Actualmente considerado:

```text
technical debt prioritaria
```

---

# 2. Realtime Sync

La sincronización realtime es una de las áreas más complejas actualmente.

---

# Problemas potenciales

- eventos duplicados,
- race conditions,
- reconnections,
- estado inconsistente,
- optimistic UI parcial.

---

# Áreas sensibles

## Kanban

Especialmente drag & drop realtime.

---

## Dashboard

Activity feed live.

---

## Notifications

Unread counters y sync multi-tab.

---

# Estado actual

Funcionalmente sólido pero arquitectónicamente sensible.

---

# 3. Permissions Complejos

El sistema RBAC + contextual authorization ha evolucionado mucho.

---

# Complejidad actual

La autorización mezcla:

- RBAC global,
- ownership,
- contexto proyecto,
- roles contextuales,
- rendering SSR.

---

# Riesgos

- reglas duplicadas,
- inconsistencias,
- lógica dispersa,
- edge cases.

---

# Importante

Aun así, el sistema RBAC actual NO se considera deuda mala.

La arquitectura conceptual es muy sólida.

La deuda reside más en:

```text
crecimiento de complejidad
```

que en mal diseño.

---

# Áreas que Necesitan Refactor

# notifications.js

Actualmente mezcla:

- WebSocket,
- DOM updates,
- counters,
- toasts,
- reconnect logic.

---

# Problemas

- demasiadas responsabilidades,
- acoplamiento UI/realtime,
- difícil testing.

---

# Refactor previsto

Separación futura:

```text
socket layer
state layer
render layer
toast layer
```

---

# dashboard.js

Actualmente concentra:

- websocket handling,
- feed rendering,
- duplicate prevention,
- reconnect logic,
- DOM manipulation.

---

# Problemas

- monolítico,
- poco reusable,
- difícil testing.

---

# project_detail.js

Actualmente es probablemente el JS más complejo del proyecto.

---

# Incluye

- Kanban,
- realtime,
- drag & drop,
- online users,
- activity feed,
- audit timeline,
- optimistic UI,
- sync visual.

---

# Riesgo principal

Concentración excesiva de responsabilidad.

---

# Deuda Técnica Consciente

# 1. Uso de prints

Actualmente se usan:

```python
print()
console.log()
```

durante desarrollo activo.

---

# Razón

Velocidad de iteración.

---

# Estado

Aceptado conscientemente.

---

# 2. Sin Docker

Actualmente el despliegue sigue siendo local.

---

# Razón

Prioridad actual:

- arquitectura,
- funcionalidad,
- realtime.

---

# Impacto

La deuda DevOps todavía es aceptable en esta fase.

---

# 3. Sin Observability Real

Actualmente no existen:

- tracing,
- metrics reales,
- observabilidad distribuida,
- dashboards operacionales técnicos.

---

# Estado

Conocido y aceptado temporalmente.

---

# 4. Sin Async Uploads

El sistema attachments todavía usa:

```text
upload tradicional SSR
```

---

# Limitaciones

- UX,
- progress feedback,
- escalabilidad.

---

# Riesgos Estratégicos Futuros

# 1. Escalabilidad Realtime

Principal preocupación arquitectónica futura.

---

# Riesgos

- múltiples usuarios,
- múltiples rooms,
- broadcasts masivos,
- sync distribuido.

---

# Posibles necesidades futuras

- Redis pub/sub,
- websocket scaling,
- distributed realtime.

---

# 2. Race Conditions

Especialmente en:

- Kanban,
- reconnects,
- optimistic UI,
- concurrent updates.

---

# 3. Frontend Complexity

El frontend SSR híbrido ha crecido mucho.

---

# Riesgos

- duplicación,
- JS disperso,
- coupling template/logic.

---

# 4. Technical Consistency

El crecimiento rápido puede provocar:

- estilos inconsistentes,
- patterns mixtos,
- diferentes estrategias UI.

---

# 5. JS Modularization

Actualmente una de las prioridades técnicas más importantes.

---

# Objetivo futuro

Evolucionar hacia:

```text
modular frontend architecture
```

---

# Deuda Buena vs Deuda Mala

# Buena Deuda

## Realtime Complexity

Es consecuencia de evolución funcional valiosa.

---

## RBAC avanzado

La complejidad proviene de capacidad real.

---

## UI reusable systems

La arquitectura reusable compensa enormemente.

---

# Mala Deuda

## JS inline excesivo

Necesita refactor.

---

## Testing realtime insuficiente

Actualmente gap importante.

---

## Falta observabilidad

Necesaria a medio plazo.

---

# Áreas Sorprendentemente Sólidas

Importante reconocer también las áreas arquitectónicamente maduras.

---

# 1. UI Reusable Patterns

Actualmente uno de los mayores activos del proyecto.

---

# Incluye

- dialogs,
- toasts,
- cards,
- timelines,
- layouts,
- macros,
- action systems.

---

# Beneficios

- consistencia,
- escalabilidad UI,
- UX homogénea.

---

# 2. RBAC Architecture

Aunque compleja, la arquitectura RBAC es sólida.

---

# Incluye

- permisos granulares,
- ownership,
- contexto,
- SSR authorization.

---

# 3. SSR Architecture

La arquitectura SSR ha demostrado ser muy estable.

---

# Beneficios

- rapidez,
- integración backend,
- seguridad,
- render contextual,
- bajo acoplamiento frontend.

---

# Deuda Operacional

# Monitoring

Actualmente muy básico.

---

# Logging

Todavía híbrido:

- prints,
- logs parciales,
- browser console.

---

# CI/CD

Existe CI sólido, pero todavía falta:

- CD,
- Docker,
- staging.

---

# Testing Debt

# Realtime Testing

Principal gap actual.

---

# Frontend Testing

Muy limitado.

---

# E2E Testing

Todavía inexistente.

---

# Estrategia de Mitigación

# Prioridad Alta

## Modularización JS

---

## Realtime stabilization

---

## WebSocket testing

---

# Prioridad Media

## Docker

---

## Observability

---

## Async uploads

---

# Prioridad Baja

## Mobile

---

## Analytics avanzados

---

# Filosofía Evolutiva

La deuda actual es coherente con la fase del proyecto.

La plataforma ha priorizado correctamente:

```text
arquitectura
+
funcionalidad
+
realtime
```

antes de optimización total.

---

# Estado Global de la Deuda

Actualmente la deuda técnica es:

```text
moderada pero controlada
```

---

# Importante

Gran parte de la complejidad actual proviene de:

```text
features avanzadas reales
```

y no de mala arquitectura base.

---

# Relación con otros documentos

Relacionado con:

- `03_ARCHITECTURE.md`
- `20_JS_ARCHITECTURE.md`
- `21_WEBSOCKET_SYSTEM.md`
- `39_CI_CD.md`
- `46_REALTIME_TESTING.md`
- `54_KNOWN_ISSUES.md`

---

# Conclusión

Aula Robótica Platform ya ha superado el nivel típico de complejidad de un proyecto académico simple.

La deuda técnica actual refleja principalmente:

- crecimiento rápido,
- realtime avanzado,
- evolución incremental,
- ambición arquitectónica.

Las prioridades más importantes actualmente son:

```text
modularización JS
+
estabilización realtime
+
observabilidad
+
testing realtime
```

mientras se preservan las áreas ya muy sólidas:

- RBAC,
- SSR architecture,
- reusable UI patterns,
- dashboards,
- activity feeds.