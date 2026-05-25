# 16_UI_TEMPLATES.md

# 🎨 Frontend & UI Architecture

# 🧠 Propósito

Este documento define la arquitectura frontend actual de Aula Robótica Platform.

La plataforma ha evolucionado desde un conjunto simple de templates Jinja2 hacia un sistema UI modular reutilizable con características cercanas a un mini design system administrativo enterprise.

---

# Objetivos del sistema UI

- SSR enterprise-grade
- reutilización extrema
- coherencia visual
- UX moderna
- desacoplamiento visual
- autorización contextual integrada
- componentes reutilizables
- realtime-ready

---

# 🏗️ Arquitectura Frontend General

# Stack visual

```text id="v1n4zp"
Jinja2
+
AdminLTE
+
Bootstrap
+
Reusable Macros
+
Modular JavaScript
+
Realtime UI
```

# Filosofía principal
Si se repite → se componentiza[cite: 1]

# Arquitectura actual
```text
/templates
│
├── layouts/
├── components/
├── partials/
├── dashboard/
├── users/
├── roles/
├── identities/
├── projects/
├── tasks/
├── activities/
└── auth/
```

# 🧱 Layout System
## Layout Base
`layouts/base.html`  
**Responsabilidades:**
* shell principal
* navbar
* sidebar
* breadcrumbs
* scripts globales
* websocket bootstrap
* notifications UI
* toast system

## Layout Architecture
### Capas principales
```text
Base Layout
→ Page Layout
→ Components
→ Row Components
→ Micro Components
```

### Principios
* separación estricta
* páginas simples
* componentes inteligentes
* macros reutilizables

# 🧩 Component Architecture
## Sistema de Macros
El sistema frontend se basa en macros Jinja2 reutilizables.

### Objetivos
* eliminar duplicación
* mantener consistencia
* acelerar desarrollo
* reducir bugs visuales

## Componentes Principales
### Actions System
`actions.html`  
Sistema reusable de acciones CRUD.

**Funcionalidades:**
* botones consistentes
* permisos integrados
* confirmaciones
* variantes visuales
* iconografía homogénea

**Ejemplo conceptual:**
```jinja2
{{ actions.edit(...) }}
{{ actions.delete(...) }}
{{ actions.view(...) }}
```

### Buttons System
`buttons.html`  
Biblioteca reusable de botones.

**Variantes:**
* primary
* secondary
* success
* warning
* danger
* outline

**Funcionalidades:**
* iconos
* tamaños
* estados
* integración permisos

### Badges System
`badges.html`  
Sistema visual de estados.

**Uso:**
* status
* activity state
* roles
* permissions
* priorities[

**Colores homogéneos:**
* success
* warning
* danger
* info
* secondary

### Data Table System
`data_table.html`  
Sistema reusable de tablas administrativas.[

**Características:**
* filas reutilizables
* paginación
* acciones
* estados vacíos
* responsive

## Row Components
### Arquitectura por fila
Cada entidad compleja posee componentes dedicados:
* `user_row.html`
* `task_row.html`
* `project_row.html`
* `activity_row.html`

**Beneficios:**
* separación visual
* mantenimiento simple
* extensibilidad
* desacoplamiento

> **Regla crítica:** Cada entidad compleja debe tener su propio row component

# 🧬 Detail Layout System
## Detail Layout Architecture
Uno de los sistemas UI más evolucionados actualmente.

### Patrón principal
```text
Header
+ 
Action Bar
+ 
Info Grid
+ 
Left Panel
+ 
Right Context Panel
+ 
Timeline
+ 
Attachments
```

# Objetivos
* visualización enterprise
* información jerarquizada
* contexto rápido
* navegación clara

# Left / Right Panels
## Left Panel
**Información principal:**
* descripción
* contenido
* relaciones
* actividad

## Right Panel
**Contexto lateral:**
* metadata
* estado
* usuario
* acciones rápidas
* información secundaria

## Beneficios UX
* lectura rápida
* separación contextual
* diseño escalable

# 📎 Attachment UI System
## Activity Attachments
Integrado completamente en detail layouts.

**Funcionalidades:**
* upload inline
* listado visual
* metadata
* descarga
* eliminación contextual

**Características:**
* integración SSR
* acciones inline
* validación visual
* ownership

# 🔔 Toast & Flash System
## Flash Architecture
El sistema clásico de flashes evolucionó hacia:
```text
Flash Backend
+ 
Toast Frontend
```

# Arquitectura
## Backend
* `request.session["_flash_messages"]`

## Frontend
Toast renderer JS reutilizable.

### Características
* auto-dismiss
* categorías visuales
* múltiples tipos
* integración SSR
* persistencia post-redirect

### Tipos soportados
* success
* error
* warning
* info

# 🛡️ Confirm Dialog System
## Reemplazo de confirm()
El sistema antiguo basado en:
* `confirm()`
* `alert()`

Fue sustituido por diálogos modernos reutilizables.

## Sistema actual
### js-confirm-form
Arquitectura JS reusable para confirmaciones.

**Funcionalidades:**
* modal moderno
* confirmaciones async
* integración formularios
* UX homogénea
* eliminación segura

**Beneficios:**
* apariencia enterprise
* coherencia visual
* mejor UX
* desacoplamiento

# 📡 Realtime UI
## WebSocket UI Integration
El frontend soporta realtime parcial.

### Integraciones actuales
* notifications
* dashboard
* audit feed
* activity feed

# Arquitectura
```text
WebSocket
→ Event Dispatcher
→ DOM Update
→ Animated Render
```

# Dashboard Realtime
## Dashboard Cards
Sistema moderno de métricas visuales.

### Características
* cards reutilizables
* métricas live
* charts
* activity feed
* timeline realtime

### Tecnologías
* Chart.js
* AdminLTE cards
* realtime updates

# 🔍 Contextual Rendering
## Renderizado basado en permisos
La UI es completamente contextual.

### Helpers disponibles
* `can()`
* `has_role()`
* `is_owner()`
* `is_project_coordinator()`

### Objetivos
* ocultar acciones inválidas
* reducir ruido visual
* mejorar UX
* reforzar seguridad

> **Regla crítica:** La UI oculta acciones. El backend valida seguridad.

# 🧠 Audit Timeline System
## Audit Timeline
Uno de los componentes visuales más avanzados.

### Características
* timeline estilo AdminLTE
* agrupación temporal
* realtime updates
* iconografía contextual
* colores dinámicos

### Helpers UI
* `get_audit_icon()`
* `get_audit_color()`

### Etiquetas temporales
* Hoy
* Ayer
* Fecha completa

# 📜 Activity Feed System
## Activity Feed
Sistema visual contextual integrado en:
* dashboard
* proyectos
* tareas
* timelines

### Funcionalidades
* eventos live
* acciones usuario
* iconografía
* contexto visual

### Eventos comunes
* CREATE_PROJECT
* UPDATE_TASK
* UPLOAD_ATTACHMENT
* DELETE_ACTIVITY
* LOGIN

# 🧩 Form Architecture
## Form System
El sistema de formularios está completamente componentizado.

### Componentes
* `form.html`
* `form_layout.html`
* `field_wrapper.html`
* `input.html`
* `select.html`
* `textarea.html`
* `validation_summary.html`

### Objetivos
* validación homogénea
* consistencia
* reutilización
* mantenimiento simple

> **Regla obligatoria:** Nunca construir formularios manualmente

# 📋 Page Patterns
## Patrones UI Oficiales
### List Pages
**Incluyen:**
* data tables
* filters
* actions
* pagination

### Detail Pages
**Incluyen:**
* detail layout
* contextual panels
* actions
* timelines
* attachments

### Form Pages
**Incluyen:**
* form layout
* validation
* contextual actions

### Empty States
Uso obligatorio de: `empty_state.html`

# 🎨 Design Rules
## Reglas visuales
* mantener coherencia AdminLTE
* evitar estilos inline
* reutilizar componentes
* mantener espaciado consistente

### Iconografía
Estándar: **FontAwesome**

### Colores
Basados en: **Bootstrap/AdminLTE palette**

# ⚙️ JavaScript Architecture
## Modular JS
El frontend evolucionó hacia JS modular reusable.

### Sistemas actuales
* toast manager
* confirm dialogs
* websocket handlers
* dashboard realtime
* timeline updates

### Filosofía
JS pequeño + reusable + desacoplado

# 🔐 UI Security Integration
## Seguridad Visual
Toda acción visual está integrada con autorización contextual.

**Ejemplos:**
`{% if can("projects:update") %}`

### Capas
```text
RBAC
+
Context Authorization
+
Ownership
+
Project Scope
```

# 🚀 Estado Actual del Frontend
## El frontend actualmente ya implementa:
* SSR enterprise-grade
* reusable design system
* realtime UI parcial
* toast architecture
* contextual rendering
* reusable dialogs
* audit timelines
* modular components

## Nivel Arquitectónico Actual
La UI ya no es simplemente “templates Jinja2”.  
**Actualmente funciona como:**  
> Mini Frontend Framework SSR

# 🔮 Evolución Prevista
## Próximas mejoras:
* HTMX/Turbo exploration
* partial realtime rendering
* live collaborative UI
* Kanban interactivo
* richer charts
* SPA híbrida opcional

# 📌 Resumen
La arquitectura frontend actual proporciona:
* SSR moderno
* componentización avanzada
* reusable UI
* realtime integration
* contextual rendering
* enterprise UX patterns

Con una arquitectura ya cercana a plataformas administrativas profesionales enterprise.

