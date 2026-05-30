# 51_CODING_RULES.md

# 🧠 Reglas de Desarrollo

# 🎯 Propósito

Este documento define normas de desarrollo para mantener Aula Robótica Platform:

- consistente,
- mantenible,
- segura,
- escalable,
- fácil de extender,
- alineada con arquitectura enterprise SSR.

Estas reglas aplican a:

- backend FastAPI,
- SQLAlchemy,
- Jinja2,
- JavaScript,
- WebSockets,
- UI reusable,
- testing,
- documentación técnica.

---

# 🧱 1. Principios Generales

## 1.1 Separación de responsabilidades

Cada capa debe tener una responsabilidad clara.

| Capa | Responsabilidad |
|---|---|
| Router | Entrada HTTP / request-response |
| Service | Lógica de negocio |
| Model | Persistencia |
| Schema | Validación |
| Template | Presentación |
| JavaScript | Interacción UI |
| WebSocket | Comunicación realtime |

---

## Regla

```text
No mezclar lógica de negocio con presentación.
```

---

### 1.2 Modularidad
Cada dominio debe vivir en su propio módulo.

```text
modules/
├── users/
├── roles/
├── identities/
├── projects/
├── tasks/
├── activities/
├── notifications/
└── audit/
```

### Cada módulo debe tener:
* **model**
* **service**
* **web/router**
* **schemas** (si aplica)
* **templates**
* **JS/CSS** (si aplica)

---

### 1.3 DRY
Evitar duplicación mediante:
* services
* helpers
* macros
* row components
* JS utilities
* shared UI patterns

---

### 1.4 Claridad antes que magia
**Preferir:**
* código explícito
* nombres descriptivos
* abstracciones pequeñas
* helpers reutilizables

**Evitar:**
* sobreingeniería
* helpers demasiado genéricos
* lógica oculta difícil de seguir

---

### ⚙️ 2. Backend FastAPI

#### 2.1 Routers
Los routers deben ser ligeros.

**Responsabilidades permitidas:**
* recibir request
* validar dependencias
* llamar servicios
* devolver response
* preparar contexto mínimo

**No permitido:**
* lógica de negocio compleja
* queries largas
* reglas de autorización manual dispersas
* cálculos pesados

**Ejemplo correcto:**
```python
@router.post("/users")
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(db, data)
    return RedirectResponse("/users", status_code=303)
```
### 2.2 Services
Los services contienen:
* lógica de negocio
* validaciones funcionales
* autorización contextual
* operaciones transaccionales
* emisión de eventos
* auditoría

> [!IMPORTANT]
> **Regla:** Si una regla importa para el negocio, debe vivir en el service.

---

### 2.3 Models SQLAlchemy
**Reglas:**
* un modelo por entidad principal
* relaciones explícitas
* `back_populates` cuando sea posible
* cascadas controladas
* naming consistente

**Foreign Keys**  
Usar patrón:
```python
user_id = Column(Integer, ForeignKey("usuarios.id_usuario"))
```

### 2.4 Schemas Pydantic
**Reglas:**
* separar input y output
* no exponer ORM directamente
* validar datos de entrada
* mantener schemas pequeños

---

### 🗄️ 3. Base de Datos
#### 3.1 Convenciones
* tablas en plural
* campos en `snake_case`
* FK con sufijo `_id`
* timestamps consistentes

#### 3.2 Relaciones
| Relación | Implementación |
| :--- | :--- |
| **1:N** | Foreign Key |
| **N:M** | Tabla intermedia |
| **ownership** | FK explícita |
| **contexto** | tabla relacional |

#### 3.3 Reglas clave
* no duplicar datos innecesariamente
* mantener normalización razonable
* evitar lógica de negocio en DB
* documentar nuevas relaciones

---

### 🔐 4. Seguridad
#### 4.1 Autenticación
**Reglas:**
* JWT como mecanismo principal
* tokens en cookies `HTTPOnly`
* no usar `localStorage`
* validar usuario activo

#### 4.2 Autorización
* Toda autorización real debe validarse en backend.
* **No permitido:** Confiar únicamente en botones ocultos en UI.

#### 4.3 RBAC
Permisos globales con formato: `resource:action`

**Ejemplos:**
* `users:create`
* `projects:update`
* `activities:delete`

#### 4.4 Autorización contextual
Usar helpers y policies para:
* ownership
* project membership
* project coordinator
* resource scope

#### 4.5 UI contextual
* La UI puede ocultar acciones, pero nunca sustituye al backend.

### 🎨 5. Templates Jinja2

#### 5.1 Uso obligatorio de macros
Si se repite HTML, debe convertirse en:
* macro
* partial
* row component
* layout reusable

---

#### 5.2 Importar con contexto
Siempre que la macro necesite permisos, usuario o helpers:

```jinja2
{% from "components/buttons.html" import btn_delete with context %}
```

#### 5.3 Lógica permitida
* **Permitido:**
    * condicionales simples
    * bucles
    * render contextual
* **No permitido:**
    * queries
    * cálculos complejos
    * reglas de negocio
    * autorización crítica

---

### 🧩 6. Patrones Frontend Reutilizables

#### 6.1 Row components
Cada entidad compleja debe tener su propio componente de fila.

**Ejemplos:**
* `user_row.html`
* `project_row.html`
* `task_row.html`
* `activity_row.html`

#### 6.2 Detail layouts
Las vistas detail deben seguir un patrón consistente:
* Header
* Action bar
* Left panel
* Right panel
* Timeline / Feed
* Attachments (si aplica)

---

#### 6.3 Action systems
* Las acciones CRUD deben usar componentes reutilizables.
* **Evitar:** botones manuales duplicados.

---

#### 6.4 Empty states
* Usar siempre un componente reusable para estados vacíos.

---

### 🔔 7. Flash System y Toasts

#### 7.1 Regla principal
* **No usar:** `alert()` nativo.
* **Usar:** `showToast()` o el sistema flash backend + toast frontend.

---

#### 7.2 Flash messages
El backend debe usar helpers centralizados:
* `flash_success(request, "Operación completada")`
* `flash_error(request, "No se pudo completar la acción")`

---

#### 7.3 Consumo de flashes
Los mensajes flash deben:
* persistir tras redirects.
* consumirse una sola vez.
* no duplicarse.
* no reaparecer en páginas posteriores.

---

#### 7.4 No acceder directamente a sesión
Evitar fuera del helper:
* `request.session["_flash_messages"]`

**Usar helper centralizado.**

---

### ⚠️ 8. Confirm Dialogs

#### 8.1 Regla principal
**No usar:**
* `confirm()`
* `onsubmit="return confirm(...)"`

---

#### 8.2 Usar js-confirm-form
**Ejemplo:**
```html
<form method="post"
      action="/tasks/1/delete"
      class="js-confirm-form"
      data-confirm-title="¿Eliminar tarea?"
      data-confirm-text="Esta acción no se puede deshacer."
      data-confirm-button="Sí, eliminar">
```
---

#### 8.3 Beneficios
* **UX consistente**
* **confirmaciones modernas**
* **menos JS inline**
* **comportamiento reusable**

---

### ⚡ 9. JavaScript

#### 9.1 Filosofía
JavaScript debe ser:
* **modular**
* **pequeño**
* **desacoplado**
* **reutilizable**
* **progresivo**

#### 9.2 Organización recomendada
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

#### 9.3 Core JS
Debe contener:
* toasts
* dialogs
* confirmations
* helpers
* websocket base clients

---

#### 9.4 No permitido
* scripts inline largos
* lógica duplicada por template
* manipulación DOM dispersa
* `alert()` o `confirm()` nativos

---

#### 9.5 Realtime JS
Los handlers websocket deben:
* estar desacoplados
* evitar duplicados
* manejar reconnect
* validar payloads
* no mezclar demasiada lógica visual

---

### 🌐 10. Context Helpers

#### 10.1 Helpers globales disponibles
En templates pueden existir:
* `has_role()`
* `has_perm()`
* `can()`
* `is_owner()`
* `is_project_coordinator()`

#### 10.2 Regla
**Usar helpers globales** en lugar de repetir lógica.

---

#### 10.3 Ejemplo correcto
```jinja2
{% if can("update", "projects", project) %}
    ...
{% endif %}
```

#### 10.4 Backend obligatorio

**Aunque la UI oculte acciones, el backend debe volver a validar.

---

### 📡 11. WebSockets

#### 11.1 Reglas
Cada conexión debe validar:
* **JWT**
* **usuario activo**
* **acceso contextual**
* **room autorizada**

---

#### 11.2 Eventos
Los eventos realtime deben tener un formato consistente:

```json
{
  "type": "task_updated",
  "payload": {}
}
```

#### 11.3 No bloquear requests HTTP
Para emisiones realtime desde rutas HTTP:
* Usar `asyncio.create_task(...)` cuando proceda.

---

### 📦 12. Rutas

#### 12.1 Convención Web
* `/resource`
* `/resource/form`
* `/resource/{id}`
* `/resource/{id}/edit`
* `/resource/{id}/delete`

#### 12.2 Convención API
* `/api/resource`
* `/api/resource/{id}`

---

#### 12.3 Regla importante
Definir **rutas fijas antes que dinámicas**.

**Correcto:**
* `/activities/form`
* `/activities/{activity_id}`

---

### 🧪 13. Testing

#### 13.1 Coverage mínimo
* **>= 85%**

#### 13.2 Prioridad de testing
Testear especialmente:
* services
* permisos
* auth
* middleware
* ownership
* attachments
* flash system
* context helpers
* websocket flows

#### 13.3 Realtime
Pendiente ampliar con:
* `pytest-asyncio`
* websocket tests
* room isolation
* reconnect flows

---

### 🔄 14. Refactorización

#### 14.1 Cuándo refactorizar
Refactorizar si aparece:
* duplicación
* lógica compleja
* naming confuso
* template demasiado grande
* router sobrecargado
* JS inline repetido

#### 14.2 Cómo refactorizar
* cambios pequeños
* sin romper funcionalidad
* tests antes/después
* mantener compatibilidad visual

---

### 🧠 15. Nomenclatura

**Variables:**
* `user_id`
* `project_id`
* `task_id`
* `activity_id`

**Funciones**
* `create_user()`
* `assign_task()`
* `upload_attachment()`

**Clases**
* `ProjectService`
* `ActivityAttachment`

**Templates**
* `entity_list.html`
* `entity_detail.html`
* `entity_form.html`
* `entity_row.html`

---

### 📌 16. Reglas Específicas del Proyecto

#### Projects
* El proyecto es la **unidad operativa principal**.
* No mezclar **RBAC global** con rol contextual.
* Validar siempre el **acceso por proyecto**.

#### Tasks
* Siempre pertenecen a un **Project**.
* Usan `assigned_to`.
* Usan `status`.
* Pueden generar eventos de **auditoría/feed**.

#### Activities
* Siempre pertenecen a una **Task**.
* Pueden tener **attachments**.
* Pueden **registrar horas**.
* Deben respetar el **ownership**.

#### Attachments
* Siempre asociados a una **Activity**.
* Validar **uploader**.
* Validar **acceso**.
* Registrar **metadata**.

#### Notifications
* Deben ser **contextuales**.
* No enviar eventos a usuarios **no autorizados**.

---

### 🚀 17. Regla de Oro
Si dudas dónde poner algo:

| Pregunta | Lugar |
| :--- | :--- |
| ¿Es lógica de negocio? | **Service** |
| ¿Es entrada HTTP? | **Router** |
| ¿Es persistencia? | **Model** |
| ¿Es validación de datos? | **Schema** |
| ¿Es visual? | **Template** |
| ¿Es interacción UI? | **JS modular** |
| ¿Es reusable? | **Helper / Macro / Component** |

---

### 🏁 Objetivo Final
El código debe ser: **legible, predecible, seguro, modular, testeable, reusable** y estar **preparado para crecer**.


## Calidad y análisis estático

El proyecto utiliza Ruff y SonarCloud para mantener consistencia, detectar code smells y reforzar buenas prácticas de desarrollo backend y SSR.
  

