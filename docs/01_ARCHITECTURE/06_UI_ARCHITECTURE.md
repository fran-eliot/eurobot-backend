# 06_UI_ARCHITECTURE.md

# Arquitectura UI

# 📌 Filosofía UI

La plataforma utiliza una arquitectura UI reusable y consistente.

Objetivos:

- coherencia visual
- reutilización
- simplicidad
- mantenibilidad
- UX administrativa moderna

---

# 🧩 Reusable Components

La UI utiliza componentes reutilizables mediante macros Jinja2.

Ejemplos:

- buttons
- badges
- tables
- cards
- actions
- alerts

---

# 📋 Row Architecture

Filas reutilizables desacopladas:

- project_row
- task_row
- activity_row
- notification_row

---

# 🧠 Detail View System

Los detail layouts modernos incluyen:

- contextual headers
- metadata sections
- timelines
- action toolbars
- attachment sections

---

# 🔔 Toast Architecture

Sistema centralizado de notificaciones visuales.

Soporta:

- success
- error
- warning
- info

Integrado con:

- SessionMiddleware
- flash messages
- JS reusable handlers

---

# ⚠️ Confirm Dialog Architecture

Sistema moderno de confirmación visual.

Basado en:

- reusable modals
- centralized JS
- data-confirm attributes

---

# 🎨 Visual Consistency

La plataforma utiliza:

- spacing consistente
- iconografía homogénea
- reusable buttons
- unified cards
- status badges

---

# 🔐 Contextual UI

La UI se adapta dinámicamente según:

- roles
- permissions
- ownership
- project context

---

# 📊 Dashboard UI

Componentes:

- stats cards
- charts
- timelines
- feeds
- realtime indicators

---

# 📈 Evolución UI

La arquitectura UI está evolucionando hacia:

- component-driven SSR
- reusable layouts
- interactive dashboards
- richer realtime UX