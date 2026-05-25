# 04_FRONTEND_ARCHITECTURE.md

# Arquitectura Frontend

# 📌 Filosofía Frontend

La plataforma sigue una estrategia:

- SSR-first
- backend-driven UI
- reusable components
- lightweight JavaScript
- progressive enhancement

El frontend está diseñado para:

- rapidez
- mantenibilidad
- seguridad
- coherencia visual
- reutilización masiva

---

# 🏗️ Arquitectura SSR

La UI se renderiza principalmente mediante:

- FastAPI
- Jinja2
- server-side rendering

Ventajas:

- menor complejidad frontend
- SEO interno
- seguridad
- menor dependencia JS
- integración directa con permisos

---

# 🧩 Arquitectura de Templates

## Organización

```text
templates/
├── base/
├── components/
├── dashboard/
├── projects/
├── tasks/
├── activities/
├── audit/
└── notifications/
```

## Layout System
La plataforma utiliza layouts reutilizables:
- base layout
- dashboard layout
- detail layouts
- cards
- tables

### Detail Layout Architecture
Los detail views modernos siguen estructura consistente:
- header contextual
- metadata cards
- action toolbars
- timelines
- sections desacopladas

**Ejemplos:**
- project_detail
- task_detail
- activity_detail

## 🎨 Arquitectura CSS
### Layered CSS Architecture

**Foundation Layer**
- base.css
- layout.css
- utilities.css

**Design System Layer**
- components.css
- forms.css
- tables.css
- buttons.css

**Feature-oriented CSS**
- dashboard.css
- projects.css
- tasks.css
- activities.css
- notifications.css

## ⚡ Arquitectura JavaScript
La plataforma utiliza JavaScript modular ligero.

### Organización JS
```text
static/js/
├── core/
├── dashboard/
├── projects/
├── tasks/
├── activities/
├── notifications/
└── realtime/
```

---

### Core JS
Contiene:
- toast system
- confirm dialogs
- websocket clients
- flash handlers
- reusable utilities

### Toast System
Sistema centralizado para:
- success
- warning
- error
- info

**Características:**
- autoclose
- SSR integration
- flash message integration
- centralized rendering

### Dialog System
Sistema reutilizable de confirmaciones.
Reemplaza:
`confirm()`
por modales visuales reutilizables.

## 🧠 Context Rendering
La plataforma utiliza template context centralizado.
Incluye:
- permisos
- usuario actual
- breadcrumbs
- notifications
- flash messages
- helpers reutilizables

## 🔐 UI Contextual Authorization
La interfaz se adapta dinámicamente según permisos.
**Ejemplos:**
- botones visibles/invisibles
- acciones contextuales
- ownership rendering
- menus dinámicos

## 📊 Dashboard Frontend
Dashboard moderno con:
- cards
- charts
- realtime updates
- timelines
- activity feeds

## 📈 Filosofía Frontend
Objetivos principales:
- simplicidad
- coherencia
- SSR robustness
- reusable UI
- maintainability