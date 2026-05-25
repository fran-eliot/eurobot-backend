# 19_COMPONENT_PATTERNS.md

# Frontend Component Patterns

## Objetivo

La plataforma Aula Robótica implementa una arquitectura frontend basada en patrones reutilizables SSR utilizando:

- Jinja2,
- macros reutilizables,
- layouts composables,
- componentes desacoplados,
- rendering contextual,
- UI declarativa.

La evolución actual ya se aproxima a un mini design-system enterprise interno.

---

# Filosofía Arquitectónica

La UI se construye siguiendo principios:

- DRY,
- SSR-first,
- reusable-first,
- consistency-first,
- contextual rendering,
- enterprise admin UX.

Objetivos:

- acelerar desarrollo,
- reducir duplicación,
- mantener consistencia visual,
- desacoplar lógica visual,
- facilitar evolución futura.

---

# Estructura de Templates

La arquitectura frontend está organizada por:

```text
templates/
```

con separación clara entre:

- páginas,
- componentes,
- módulos,
- layouts,
- macros reutilizables.

:contentReference[oaicite:0]{index=0}

---

# Arquitectura General de Componentes

```text
Pages
    ↓
Reusable Layouts
    ↓
Reusable Components
    ↓
Macros
    ↓
Context Helpers
    ↓
Visual Rendering
```

---

# Tipos de Componentes

## 1. Layout Components

Responsables de:

- estructura,
- distribución,
- columnas,
- navegación visual.

Ejemplos:

- `detail_layout.html`
- `form_layout.html`
- `section_card.html`
- `tabs.html`

---

## 2. Row Components

Responsables de:

- renderizado homogéneo de entidades,
- tablas reutilizables,
- acciones contextuales.

Ejemplos:

- `activity_row.html`
- `project_row.html`
- `task_row.html`
- `user_row.html`
- `role_row.html`

:contentReference[oaicite:1]{index=1}
:contentReference[oaicite:2]{index=2}

---

## 3. Action Components

Responsables de:

- botones,
- acciones CRUD,
- navegación contextual,
- dialogs.

Ejemplos:

- `buttons.html`
- `actions.html`
- `identity_actions.html`
- `role_actions.html`

:contentReference[oaicite:3]{index=3}
:contentReference[oaicite:4]{index=4}

---

## 4. Data Components

Responsables de:

- tablas,
- estados vacíos,
- paginación,
- render dinámico.

Ejemplos:

- `table.html`
- `data_table.html`
- `audit_table.html`

:contentReference[oaicite:5]{index=5}
:contentReference[oaicite:6]{index=6}

---

## 5. Visual Components

Responsables de:

- badges,
- iconografía,
- estados visuales,
- feedback UI.

Ejemplos:

- `badges.html`
- `metric_card.html`
- `empty_state.html`

:contentReference[oaicite:7]{index=7}

---

## 6. Feed & Timeline Components

Responsables de:

- realtime feeds,
- activity streams,
- timelines,
- auditoría visual.

Ejemplos:

- `project_feed.html`
- `audit_table.html`

:contentReference[oaicite:8]{index=8}

---

# Pattern — Reusable Macros

## Filosofía

La mayor parte de la UI reusable se implementa mediante:

```jinja2
{% macro ... %}
```

---

# Beneficios

## DRY

Reduce duplicación masiva.

---

## Consistencia visual

Todos los módulos comparten:

- estilos,
- spacing,
- iconografía,
- comportamiento.

---

## Escalabilidad

Nuevos módulos reutilizan patrones existentes.

---

## Evolución centralizada

Cambios globales desde un único punto.

---

# Pattern — Detail Layout

Uno de los patrones más maduros actualmente.

---

## Arquitectura

Distribución:

```text
LEFT PANEL
    Perfil / resumen / acciones

RIGHT PANEL
    Tabs / contenido principal
```

---

# Uso actual

Implementado en:

- usuarios,
- roles,
- identidades.

:contentReference[oaicite:9]{index=9}
:contentReference[oaicite:10]{index=10}
:contentReference[oaicite:11]{index=11}

---

# Beneficios

## UX enterprise

Se aproxima a paneles administrativos modernos.

---

## Jerarquía visual

Separación clara entre:

- perfil,
- navegación,
- contenido,
- auditoría.

---

## Escalabilidad

Permite:

- nuevas tabs,
- side panels,
- widgets,
- realtime blocks.

---

# Pattern — Section Card

## Objetivo

Contenedor reusable estándar.

Definido en:

```text
section_card.html
```

:contentReference[oaicite:12]{index=12}

---

# Patrón Base

```jinja2
{% call section_card() %}
    contenido
{% endcall %}
```

---

# Beneficios

- spacing consistente,
- visual homogéneo,
- reutilización total,
- desacoplamiento layout/UI.

---

# Pattern — Contextual Rendering

Uno de los pilares del frontend actual.

---

# Filosofía

La UI se adapta dinámicamente según:

- permisos,
- ownership,
- roles,
- contexto proyecto,
- autorización contextual.

---

# Helpers utilizados

```jinja2
can()
has_perm()
has_role()
is_owner()
is_project_coordinator()
```

---

# Ejemplo real

```jinja2
{% if can("update", "projects", project) %}
```

:contentReference[oaicite:13]{index=13}

---

# Beneficios

## Seguridad visual

Oculta acciones no autorizadas.

---

## UX contextual

Reduce ruido visual.

---

## Reutilización

Los componentes ya incluyen autorización integrada.

---

# Pattern — Reusable Action Buttons

## Arquitectura

Los botones reutilizables centralizan:

- iconos,
- tamaños,
- estilos,
- confirmaciones,
- comportamiento.

---

# btn_delete()

Macro reusable moderna.

Incluye:

- dialog integration,
- confirm system,
- estilos consistentes,
- data attributes.

:contentReference[oaicite:14]{index=14}

---

# Beneficios

## Eliminación de lógica duplicada

---

## Integración automática con dialogs

---

## Consistencia UX

---

# Pattern — Row Renderer

## Filosofía

Las tablas no renderizan directamente entidades.

Utilizan:

```jinja2
row_renderer()
```

:contentReference[oaicite:15]{index=15}

---

# Beneficios

## Separación de responsabilidades

---

## Reutilización

---

## Escalabilidad

---

## Uniformidad visual

---

# Pattern — Empty States

## Objetivo

Evitar tablas vacías o layouts rotos.

---

# Arquitectura

Integrado directamente en:

```jinja2
data_table()
```

:contentReference[oaicite:16]{index=16}

---

# Beneficios

- UX consistente,
- mejor feedback,
- interfaz más limpia.

---

# Pattern — Feed Components

## Arquitectura realtime-ready

Los feeds están preparados para:

- updates live,
- WebSockets,
- streaming incremental.

---

# Ejemplo

`project_feed.html`

:contentReference[oaicite:17]{index=17}

---

# Características

- iconografía contextual,
- timestamps,
- render desacoplado,
- soporte realtime.

---

# Pattern — Kanban Components

Implementado en:

```text
projects_detail.html
```

:contentReference[oaicite:18]{index=18}

---

# Características

- drag & drop,
- realtime,
- estados visuales,
- columnas reutilizables,
- counters dinámicos.

---

# Pattern — Attachment Components

Implementado en:

```text
activities_detail.html
```

:contentReference[oaicite:19]{index=19}

---

# Características

- iconografía MIME-aware,
- uploader metadata,
- acciones contextuales,
- integración permisos,
- reusable visual patterns.

---

# Pattern — Timeline Components

Implementado actualmente en:

- auditoría,
- feeds,
- dashboard.

---

# Características

- agrupación temporal,
- iconografía contextual,
- rendering reusable,
- visualización enterprise.

:contentReference[oaicite:20]{index=20}

---

# Pattern — Tabs Architecture

## Filosofía

Separación funcional mediante:

```jinja2
tabs()
```

---

# Uso actual

- usuarios,
- roles,
- identidades.

---

# Beneficios

## Navegación limpia

---

## Separación funcional

---

## Escalabilidad

---

# Pattern — Hero Components

Implementado especialmente en:

- users,
- roles.

:contentReference[oaicite:21]{index=21}
:contentReference[oaicite:22]{index=22}

---

# Objetivo

Crear páginas con estética:

```text
Enterprise Admin Platform
```

---

# Pattern — Realtime-aware Components

Los componentes modernos están preparados para:

- updates parciales,
- re-render incremental,
- websocket events,
- live counters.

---

# Pattern — Declarative UI

La UI SSR utiliza patrones declarativos:

```html
data-*
```

Especialmente en:

- dialogs,
- confirmaciones,
- realtime hooks.

---

# Pattern — Smart Tables

## Arquitectura

Las tablas modernas soportan:

- paginación,
- filtros,
- search,
- estados vacíos,
- render dinámico.

:contentReference[oaicite:23]{index=23}

---

# Estado Actual

## Arquitectura madura

La plataforma ya dispone de:

- reusable layouts,
- reusable cards,
- reusable rows,
- reusable actions,
- reusable tables,
- contextual rendering,
- enterprise detail views,
- realtime-aware components.

---

# Problemas actuales

## 1. Algunos componentes legacy

Persisten patrones antiguos mezclados con nuevos.

---

## 2. CSS todavía parcialmente disperso

---

## 3. Algunos módulos aún no usan macros modernas

---

## 4. Algunas tablas siguen siendo manuales

---

# Futuras Evoluciones

## Component Registry

Documentación centralizada de componentes.

---

## Design Tokens

Variables globales:

- spacing,
- typography,
- colors,
- sizing.

---

## Theme System

Dark mode / branding.

---

## Component Playground

Entorno visual interno para UI reusable.

---

## Fully realtime components

Actualización parcial sin reload.

---

## Advanced reusable forms

Inputs declarativos enterprise.

---

# Relación con otros documentos

Relacionado con:

- `03_ARCHITECTURE.md`
- `07_FRONTEND_ARCHITECTURE.md`
- `08_UI_ARCHITECTURE.md`
- `17_DIALOG_SYSTEM.md`
- `18_TOAST_SYSTEM.md`
- `20_JS_ARCHITECTURE.md`
- `51_CODING_RULES.md`

---

# Conclusión

La arquitectura frontend actual ya supera ampliamente un CRUD SSR tradicional.

La plataforma dispone actualmente de:

- patrones reutilizables maduros,
- rendering contextual,
- layouts enterprise,
- macros desacopladas,
- realtime-ready UI,
- base sólida para evolución futura tipo internal admin platform.