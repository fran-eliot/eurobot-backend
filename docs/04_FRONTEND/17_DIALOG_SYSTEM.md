# 17_DIALOG_SYSTEM.md

# Sistema Reutilizable de Dialogs

## Objetivo

La plataforma Aula Robótica implementa un sistema centralizado y reutilizable de dialogs modernos para reemplazar completamente el uso de:

- `window.confirm()`
- `alert()`
- confirmaciones nativas del navegador

La arquitectura actual proporciona:

- experiencia visual enterprise,
- consistencia UI,
- integración SSR,
- reutilización completa,
- desacoplamiento frontend,
- extensibilidad futura.

---

# Filosofía del sistema

El sistema de dialogs forma parte del mini design-system interno de la plataforma.

Objetivos:

- UX moderna
- confirmaciones consistentes
- menor deuda técnica
- centralización de comportamiento
- integración reusable con formularios SSR
- desacoplamiento entre HTML y lógica JS

---

# Arquitectura General

El sistema está dividido en:

```text
Templates SSR (Jinja2)
        ↓
Atributos data-*
        ↓
confirmations.js
        ↓
dialog.js
        ↓
SweetAlert2
        ↓
Modal visual reusable
```

# Componentes Principales

## 1. HTML SSR declarativo

Las confirmaciones se definen directamente desde templates Jinja2 mediante atributos:

```html
class="js-confirm-form"
data-confirm-title=""
data-confirm-text=""
data-confirm-button=""
data-confirm-icon=""
```

---

## 2. confirmAction()

Función global reusable.

### Responsabilidades

- construir dialogs,
- ejecutar confirmaciones,
- devolver resultado booleano,
- encapsular SweetAlert2.

### Definida en

```text
static/js/core/dialog.js
```

---

## 3. confirmations.js

### Responsable de

- detectar formularios confirmables,
- interceptar submit,
- ejecutar dialog,
- continuar submit si el usuario confirma.

### Definido en

```text
static/js/core/confirmations.js
```

---

# Flujo completo

## 1. Usuario pulsa acción peligrosa

### Ejemplo

- eliminar proyecto,
- eliminar actividad,
- eliminar tarea,
- borrar adjunto,
- eliminar usuario.

---

## 2. Intercepción JS

`confirmations.js` intercepta:

```javascript
submit
```

sobre:

```html
.js-confirm-form
```

---

## 3. Apertura del dialog

Se ejecuta:

```javascript
confirmAction()
```

---

## 4. Render SweetAlert2

Se genera modal moderno.

---

## 5. Confirmación

Si usuario confirma:

```javascript
form.submit()
```

---

# Integración Global

El sistema se carga globalmente desde:

```text
base.html
```

### Scripts registrados

```html
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>

<script src="{{ url_for('static', path='js/core/dialog.js') }}"></script>

<script src="{{ url_for('static', path='js/core/confirmations.js') }}"></script>
```

### Esto garantiza

- disponibilidad global,
- comportamiento consistente,
- inicialización automática.

---

# confirmAction()

## Objetivo

Centralizar toda la lógica de dialogs reutilizables.

---

## API

```javascript
confirmAction({
    title,
    text,
    confirmText,
    cancelText,
    icon
})
```

---

## Implementación actual

```javascript
window.confirmAction = async function ({
    title = "¿Estás seguro?",
    text = "",
    confirmText = "Sí",
    cancelText = "Cancelar",
    icon = "warning"
} = {}) {

    const result = await Swal.fire({
        title,
        text,
        icon,
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#6c757d",
        confirmButtonText: confirmText,
        cancelButtonText: cancelText,
        reverseButtons: true
    });

    return result.isConfirmed;
};
```

---

# Interceptor centralizado

## confirmations.js

Sistema automático reusable.

---

## Comportamiento

- detecta `.js-confirm-form`,
- intercepta submit,
- previene submit inmediato,
- ejecuta dialog,
- continúa si hay confirmación.

---

## Implementación

```javascript
document.querySelectorAll(".js-confirm-form")
```

---

# Declarative UI Pattern

La arquitectura usa un patrón declarativo SSR.

Los templates no contienen lógica JS.

Únicamente describen:

- intención,
- mensajes,
- configuración visual.

---

# Ejemplo real

## Eliminación de proyecto

```html
<form method="post"
      action="/projects/{{ project.id_project }}/delete"
      class="d-inline js-confirm-form"
      data-confirm-title="¿Eliminar Projecto?"
      data-confirm-text="Esta acción no se puede deshacer."
      data-confirm-button="Sí, eliminar">

    <button class="btn btn-sm btn-outline-danger">
        <i class="fas fa-trash"></i>
    </button>

</form>
```

---

# Casos actuales de uso

## CRUD administrativo

Implementado en:

- proyectos,
- tareas,
- actividades,
- usuarios,
- identidades,
- roles,
- adjuntos.

---

# Ejemplos reales

## Actividades

## Tareas

## Proyectos

---

# Arquitectura Reusable

## Patrón Base

```text
Template SSR
    ↓
data-attributes
    ↓
JS reusable
    ↓
Dialog centralizado
```

---

# Beneficios

## 1. UX enterprise

Sustituye dialogs nativos del navegador.

---

## 2. Consistencia visual

Toda la plataforma comparte:

- colores,
- layout,
- comportamiento,
- iconografía.

---

## 3. Desacoplamiento

HTML no contiene lógica JS compleja.

---

## 4. Reutilización

Una sola implementación sirve para todo el sistema.

---

## 5. Escalabilidad

Permite:

- nuevos dialogs,
- formularios complejos,
- confirmaciones multinivel,
- flujos async,
- dialogs AJAX.

---

## 6. SSR-friendly

Compatible completamente con arquitectura server-side Jinja2.

---

# Integración con el Design System

El sistema de dialogs forma parte del frontend reusable de Aula Robótica.

Integrado con:

- macros Jinja2,
- botones reutilizables,
- toast system,
- realtime notifications,
- contextual rendering,
- action bars,
- reusable rows.

---

# Integración con Macros

## btn_delete()

Macro reusable:

```jinja2
btn_delete()
```

### Implementa automáticamente

- dialog,
- confirmación,
- estilos,
- atributos `data-*`.

---

# Integración con Realtime UX

Los dialogs conviven con:

- dashboard realtime,
- websockets,
- feeds live,
- notifications,
- toast system.

La UX general busca comportamiento tipo:

```text
Enterprise Admin Console
```

---

# Arquitectura SweetAlert2

## Razones de adopción

SweetAlert2 aporta:

- dialogs modernos,
- accesibilidad,
- animaciones,
- theming,
- soporte async,
- integración sencilla.

---

# Sustitución completa de confirm()

El sistema reemplaza completamente:

```javascript
window.confirm()
```

El proyecto ya no utiliza confirmaciones nativas.

---

# Estado Actual

## Completamente implementado

Incluye:

- dialogs reutilizables,
- interceptores globales,
- macros integradas,
- integración SSR,
- configuración declarativa,
- UX moderna.

---

# Próximas Evoluciones

## Futuras mejoras previstas

### Confirmaciones async avanzadas

Ejemplo:

- loaders,
- validaciones previas,
- acciones múltiples.

---

### Dialogs de formularios

Posible soporte:

- edición inline,
- formularios rápidos,
- creación contextual.

---

### Dialogs contextualizados

Según:

- permisos,
- ownership,
- criticidad,
- tipo de entidad.

---

### Integración i18n

Preparación futura para:

- internacionalización,
- localización dinámica.

---

# Relación con otros documentos

Relacionado con:

- `03_ARCHITECTURE.md`
- `07_FRONTEND_ARCHITECTURE.md`
- `08_UI_ARCHITECTURE.md`
- `18_TOAST_SYSTEM.md`
- `19_COMPONENT_PATTERNS.md`
- `20_JS_ARCHITECTURE.md`
- `51_CODING_RULES.md`

---

# Conclusión

El sistema de dialogs actual representa una evolución importante respecto a un CRUD tradicional.

La plataforma ya dispone de:

- confirmaciones enterprise,
- arquitectura reusable,
- integración SSR madura,
- UX consistente,
- frontend desacoplado,
- base sólida para evolución futura.