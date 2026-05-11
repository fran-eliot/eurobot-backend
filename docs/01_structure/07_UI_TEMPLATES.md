# 07_UI_TEMPLATES.md

## 🧠 Propósito

Definir la arquitectura, convenciones y funcionamiento del sistema de templates basado en **Jinja2 + AdminLTE**.

Este documento cubre:

* Estructura de templates
* Uso de macros
* Layouts reutilizables
* Contexto global
* Integración con permisos
* Buenas prácticas

---

# 🏗️ 1. ARQUITECTURA DE TEMPLATES

## 1.1 Estructura general

```text 
/templates
│
├── base.html
│
├── components/
│   ├── actions.html
│   ├── badges.html
│   ├── buttons.html
│   ├── data_table.html
│   ├── detail_layout.html
│   ├── empty_state.html
│   ├── filters_bar.html
│   ├── form.html
│   ├── form_layout.html
│   ├── field_wrapper.html
│   ├── input.html
│   ├── select.html
│   ├── textarea.html
│   ├── page_header.html
│   ├── section_card.html
│   ├── tabs.html
│   └── validation_summary.html
│
├── users/
├── roles/
├── identities/
├── projects/
├── tasks/
├── activities/
├── dashboard/
└── auth/
```

---

## 1.2 Principio clave

👉 **Separar vistas de componentes**

* Vistas → páginas completas
* Componentes → macros reutilizables

---

# 🧱 2. LAYOUT BASE

## 2.1 base.html

Responsabilidades:

* Layout global
* Navbar
* Sidebar
* Scripts
* Usuario autenticado

---

## 2.2 Uso

```jinja 
{% extends "layouts/base.html" %}

{% block content %}
  ...
{% endblock %}
```

---

## 2.3 Responsabilidades

* Estructura general
* Carga de CSS/JS
* Menú dinámico
* Usuario autenticado

---

# 🧩 3. COMPONENTES (MACROS)

## 3.1 Objetivo

Reducir duplicación y mantener consistencia.

Regla clave: 👉 Si se repite → se convierte en macro

---

## 3.2 Componentes principales

### Buttons

* Botones estándar
* Acciones CRUD

---

### Data Table

* Tablas administrativas
* Acciones por fila

---

### Page Header

* Título
* Breadcrumbs
* Botones de acción

---

### Section Card

* Contenedor visual reutilizable

---

### Detail Layout

* Vista de detalle estructurada

---

### Badges

* Estados (activo, inactivo, etc.)

---

### Actions

* Botones de editar/eliminar/ver

### Tabs

---

## 3.3 🧬 Micro-componentes (Row Components)

Componentes diseñados para representar entidades dentro de tablas:

- user_row.html
- task_row.html
- project_row.html
- activity_row.html

Beneficios:
- Reutilización extrema
- Separación de lógica de render por entidad
- Facilita mantenimiento: Código Limpio

Regla:
👉 Cada entidad compleja debería tener su propio *_row.html

---

## 3.4 Uso correcto

```jinja id="b1qk3f"
{% from "components/buttons.html" import primary_button with context %}
```

👉 Siempre usar `with context`

---

# 🌐 4. CONTEXTO GLOBAL

## 4.1 Variables disponibles

En todas las plantillas:

* `current_user`
* `roles`
* `permissions`
* `menu`
* `breadcrumbs`
* `can()` (helper de permisos)

---

## 4.2 Uso de permisos

```jinja 
{% if can("users:create") %}
  {{ button("Crear usuario") }}
{% endif %}
```

---

## 4.3 Objetivo

* Evitar lógica duplicada
* Controlar UI según permisos
* Mejorar UX

---

# 🧾 5. SISTEMA DE FORMULARIOS

Componentes:

* form.html
* form_layout.html
* field_wrapper.html
* input.html
* select.html
* textarea.html

---

## Regla crítica

❌ No crear formularios manuales
✔ Siempre usar componentes

---

# 🧭 6. MENÚ DINÁMICO

## 6.1 Funcionamiento

```text 
Definición → Filtrado por permisos → Render
```

---

## 6.2 Características

* Basado en permisos
* Marca opción activa
* Soporta submenús

---

## 6.3 Beneficios

* Seguridad visual
* Navegación limpia
* Escalable

---

# 📊 7. PATRONES DE VISTAS

## 7.1 Listado

* Tabla con acciones
* Filtros (opcional)
* Botón crear

---

## 7.2 Formulario

* Crear / editar
* Reutilización del mismo template

---

## 7.3 Detalle

* Información estructurada
* Tabs (si aplica)
* Acciones contextuales

---

## 7.4 Estado vacío

Uso de:

```jinja 
empty_state.html
```
---

## 7.5. Sistema de formularios

El sistema de formularios está completamente componentizado:

- form.html
- form_layout.html
- field_wrapper.html
- input.html
- select.html
- textarea.html

Objetivo:
- Consistencia
- Validación homogénea
- Reutilización

Regla:
👉 Nunca construir formularios “a mano”
👉 Siempre usar componentes existentes

---

# 🎨 8. ESTILO Y DISEÑO

## 8.1 Framework

* AdminLTE
* Bootstrap
* Consistencia obligatoria

---

## 8.2 Reglas

* No romper estilo base
* Usar clases existentes
* Mantener consistencia visual

---

## 8.3 Componentización

* Todo lo repetido → macro
* Evitar HTML duplicado

---

# 🔐 9. PERMISOS EN UI

## 9.1 Regla

👉 UI oculta acciones
👉 Backend valida seguridad

---

## 9.2 Ejemplo

```jinja 
{% if can("users:delete") %}
  {{ delete_button() }}
{% endif %}
```

---

# ⚠️ 10. PROBLEMAS COMUNES

## 10.1 Macros sin contexto

❌ Error:

```jinja
{% from "..." import button %}
```

✔ Correcto:

```jinja
{% from "..." import button with context %}
```

---

## 10.2 Lógica excesiva

❌ No hacer:

* cálculos
* queries
* lógica compleja

---

## 10.3 Duplicación

* copiar templates en lugar de reutilizar macros

---

## 10.4 Inconsistencia visual

* usar estilos distintos sin necesidad

---

# 🧠 11. BUENAS PRÁCTICAS

* Reutilizar macros siempre
* Mantener templates simples
* Delegar lógica al backend
* Usar nombres claros
* Mantener coherencia visual

---

# 🧱 12. INTEGRACIÓN CON MÓDULOS

Cada módulo debe tener:

```text 
/modules/<modulo>/templates/
```

Ejemplo:

* users/templates/
* projects/templates/

---

# 🔮 13. EVOLUCIÓN FUTURA

* Vista Kanban (tasks)
* Componentes interactivos JS
* Posible SPA parcial
* Mejora UX

---

# 📌 14. RESUMEN

El sistema de templates es:

* Modular
* Reutilizable
* Basado en macros
* Integrado con permisos
* Adaptado a AdminLTE

---

# 🚀 15. REGLA CLAVE

👉 Si repites HTML → crea macro
👉 Si dudas → lógica en backend

---

## Timeline de Auditoría

### Ubicación

Implementado en:
- `tasks/tasks_detail.html`

### Características

- Diseño tipo AdminLTE Timeline
- Agrupación por fecha
- Etiquetas amigables:
  - Hoy
  - Ayer
  - Fecha completa

### Realtime

El timeline se actualiza dinámicamente mediante WebSockets:

- Inserción automática de nuevos eventos
- Prevención de duplicado de grupos de fecha
- Animación visual de nuevos eventos

### Helpers UI

Uso de:
- `get_audit_icon()`
- `get_audit_color()`