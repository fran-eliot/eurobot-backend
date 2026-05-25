# 18_TOAST_SYSTEM.md

# Sistema Centralizado de Toasts

## Objetivo

La plataforma Aula Robótica implementa un sistema centralizado de notificaciones toast reutilizables para proporcionar:

- feedback visual moderno,
- UX consistente,
- compatibilidad SSR,
- desacoplamiento frontend,
- integración global con toda la plataforma.

El sistema reemplaza completamente:

- alerts visuales tradicionales,
- mensajes inline inconsistentes,
- feedback disperso.

---

# Filosofía del sistema

El sistema toast forma parte del mini design-system interno de la plataforma.

Objetivos:

- UX moderna tipo enterprise,
- feedback contextual consistente,
- arquitectura reusable,
- integración SSR-first,
- desacoplamiento backend/frontend,
- reutilización transversal.

---

# Arquitectura General

```text
Backend Action
        ↓
Flash Service
        ↓
SessionMiddleware
        ↓
Context Injection
        ↓
base.html
        ↓
toasts.js
        ↓
Toast render dinámico
```

---

# Componentes Principales

## 1. Flash Backend Service

Sistema reusable de mensajes flash persistentes vía sesión.

Definido en:

```text
app/utils/flash.py
```

:contentReference[oaicite:0]{index=0}

---

## 2. SessionMiddleware

El sistema depende de:

```python
SessionMiddleware
```

para mantener mensajes flash entre redirects SSR.

---

## 3. Context Injection

Los flash messages se integran automáticamente en:

```python
get_template_context()
```

mediante:

```python
flash_messages = get_flash(request)
```

:contentReference[oaicite:1]{index=1}

---

## 4. Render SSR Global

Los mensajes se renderizan globalmente desde:

```html
base.html
```

:contentReference[oaicite:2]{index=2}

---

## 5. Toast Manager JS

Responsable de:

- render visual,
- animaciones,
- auto-dismiss,
- stacking,
- lifecycle.

Definido en:

```text
static/js/core/toasts.js
```

:contentReference[oaicite:3]{index=3}

---

# Arquitectura SSR-first

La arquitectura actual está completamente orientada a SSR.

El flujo principal funciona así:

---

# Flujo completo

## 1. Acción backend

Ejemplo:

- crear proyecto,
- subir adjunto,
- eliminar tarea,
- actualizar actividad,
- login/logout.

---

## 2. Flash persistente

Backend ejecuta:

```python
flash_success(request, "Archivo subido correctamente")
```

o:

```python
flash_error(request, "No tienes permisos")
```

:contentReference[oaicite:4]{index=4}

---

## 3. Persistencia en sesión

El mensaje se almacena en:

```python
request.session["_flash_messages"]
```

:contentReference[oaicite:5]{index=5}

---

## 4. RedirectResponse

El mensaje sobrevive al redirect SSR.

---

## 5. Context Injection

El contexto global consume:

```python
get_flash(request)
```

:contentReference[oaicite:6]{index=6}

---

## 6. Render dinámico

`base.html` genera automáticamente:

```javascript
showToast()
```

por cada flash message.

:contentReference[oaicite:7]{index=7}

---

## 7. Render visual

`toasts.js` crea dinámicamente:

- toast DOM,
- animación,
- estilos,
- auto-dismiss.

---

# Backend Flash Service

## add_flash()

Core principal.

```python
add_flash(request, message, category)
```

Responsabilidades:

- persistencia,
- acumulación,
- serialización session-safe.

---

## Helpers disponibles

### Success

```python
flash_success()
```

---

### Error

```python
flash_error()
```

---

### Warning

```python
flash_warning()
```

---

### Info

```python
flash_info()
```

:contentReference[oaicite:8]{index=8}

---

# Cache Protection

Uno de los problemas solucionados recientemente fue:

```text
duplicación de toasts
```

---

## Problema original

El contexto SSR se reconstruía múltiples veces por request.

Resultado:

- mensajes repetidos,
- múltiples toasts idénticos,
- comportamiento inconsistente.

---

## Solución implementada

Cache temporal request-scoped:

```python
request.state._cached_flash_messages
```

:contentReference[oaicite:9]{index=9}

---

# Toast Container

## Contenedor global

```html
<div id="toast-container"></div>
```

:contentReference[oaicite:10]{index=10}

---

# showToast()

## API pública global

```javascript
showToast({
    title,
    message,
    type,
    duration
})
```

:contentReference[oaicite:11]{index=11}

---

# Render dinámico

Cada toast se construye dinámicamente:

```javascript
document.createElement("div")
```

:contentReference[oaicite:12]{index=12}

---

# Auto-dismiss

Sistema automático:

```javascript
setTimeout()
```

:contentReference[oaicite:13]{index=13}

---

# Toast Types

Actualmente soportados:

| Tipo | Uso |
|---|---|
| success | acciones correctas |
| danger | errores |
| warning | advertencias |
| primary | información |

---

# Integración Global

## Scripts registrados globalmente

```html
<script src="{{ url_for('static', path='js/core/toasts.js') }}"></script>
```

:contentReference[oaicite:14]{index=14}

---

# Integración con Context Injection

El sistema toast está completamente integrado con:

- contexto SSR,
- helpers globales,
- render universal,
- navegación completa.

---

# Arquitectura Reusable

## Patrón Base

```text
Backend action
    ↓
Flash helper
    ↓
Session
    ↓
Context injection
    ↓
Render SSR
    ↓
Toast JS
    ↓
UI visual
```

---

# Beneficios

## 1. UX enterprise

Feedback visual moderno y consistente.

---

## 2. SSR-compatible

Funciona perfectamente con arquitectura server-side.

---

## 3. Desacoplamiento

Backend no depende de implementación visual.

---

## 4. Reutilización

Un único sistema sirve para toda la plataforma.

---

## 5. Escalabilidad

Permite:

- nuevos tipos,
- realtime toasts,
- prioridad,
- agrupación,
- persistencia.

---

## 6. Consistencia visual

Toda la plataforma comparte:

- colores,
- animaciones,
- duración,
- layout,
- comportamiento.

---

# Integración con el Design System

El sistema toast forma parte del frontend reusable.

Integrado con:

- dialogs,
- reusable buttons,
- timelines,
- notifications,
- contextual rendering,
- dashboard realtime.

---

# Relación con Notifications

## Diferencia conceptual

### Toast

Feedback efímero inmediato.

Ejemplos:

- "Proyecto creado"
- "Archivo subido"
- "Actividad eliminada"

---

### Notification

Evento persistente del sistema.

Ejemplos:

- asignaciones,
- eventos realtime,
- actividad colaborativa,
- alertas del sistema.

---

# Integración con Realtime

Actualmente los toasts son:

```text
SSR-triggered
```

Pero la arquitectura está preparada para:

```text
WebSocket-triggered realtime toasts
```

---

# Problemas solucionados recientemente

## 1. Toast duplication

Solucionado mediante:

```python
request.state._cached_flash_messages
```

---

## 2. Persistencia accidental

Corregido mediante:

```python
session.pop()
```

:contentReference[oaicite:15]{index=15}

---

## 3. Orden incorrecto

Solucionado mediante:

```javascript
container.prepend(toast)
```

:contentReference[oaicite:16]{index=16}

---

# Estado Actual

## Completamente implementado

Incluye:

- flash backend,
- persistencia SSR,
- render global,
- toast manager,
- auto-dismiss,
- stacking,
- reusable architecture.

---

# Futuras Evoluciones

## Realtime Toasts

Integración WebSocket:

- dashboard,
- kanban,
- colaboración live.

---

## Toast Queue

Sistema de prioridad y cola.

---

## Toast Groups

Agrupación automática.

---

## Toast Actions

Botones inline:

- deshacer,
- abrir,
- navegar.

---

## Persistencia configurable

Toasts críticos persistentes.

---

## Sound notifications

Opcional para eventos críticos.

---

# Relación con otros documentos

Relacionado con:

- `03_ARCHITECTURE.md`
- `07_FRONTEND_ARCHITECTURE.md`
- `08_UI_ARCHITECTURE.md`
- `17_DIALOG_SYSTEM.md`
- `19_COMPONENT_PATTERNS.md`
- `20_JS_ARCHITECTURE.md`
- `15_AUDIT_SYSTEM.md`

---

# Conclusión

El sistema toast actual representa una arquitectura madura y reusable propia de plataformas enterprise modernas.

La plataforma ya dispone de:

- feedback SSR consistente,
- arquitectura desacoplada,
- render global,
- integración contextual,
- UX moderna,
- base sólida para evolución realtime futura.