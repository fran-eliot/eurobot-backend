# 17_CODING_RULES.md

## 🧠 Propósito

Definir normas de desarrollo para:

* Mantener consistencia en el código
* Facilitar mantenimiento y escalabilidad
* Reducir deuda técnica
* Asegurar calidad en nuevas funcionalidades

Estas reglas aplican a:

* Backend (FastAPI, SQLAlchemy)
* Templates (Jinja2)
* Organización del proyecto

---

# 🧱 1. PRINCIPIOS GENERALES

## 1.1 Separación de responsabilidades

Cada capa debe tener una responsabilidad clara:

* **Router** → entrada HTTP
* **Service** → lógica de negocio
* **Model** → persistencia
* **Template** → presentación

❌ Nunca mezclar lógica de negocio en templates
❌ Evitar lógica compleja en routers

---

## 1.2 Modularidad

Cada dominio debe vivir en su módulo:

```text
modules/
  users/
  roles/
  projects/
```

Cada módulo debe contener:

* `model.py`
* `service.py`
* `web.py`
* `schemas.py` (si aplica)
* `templates/`

---

## 1.3 DRY (Don't Repeat Yourself)

* Reutilizar funciones en services
* Usar macros Jinja2
* Evitar duplicación de queries

---

## 1.4 Claridad sobre “magia”

* Priorizar código explícito
* Evitar abstracciones innecesarias
* Nombres descriptivos

---

# ⚙️ 2. BACKEND (FastAPI)

## 2.1 Routers

### Reglas

* Deben ser **ligeros**
* No contener lógica de negocio compleja
* Usar servicios para operaciones

### Ejemplo correcto

```python
@router.post("/users")
def create_user(data: UserCreate):
    return user_service.create_user(data)
```

---

## 2.2 Services

### Responsabilidad

* Contener lógica de negocio
* Validaciones funcionales
* Orquestar operaciones

### Ejemplo

```python
def create_user(data):
    validate_user(data)
    return repository.save(data)
```

---

## 2.3 Models (SQLAlchemy)

### Reglas

* Un modelo por entidad
* Relaciones bien definidas
* Naming consistente

### Naming

* snake_case en campos
* FK → `*_id`

Ejemplo:

```python
user_id = Column(ForeignKey("users.id"))
```

---

## 2.4 Schemas (Pydantic)

* Separar input/output
* No exponer modelos ORM directamente

---

# 🗄️ 3. BASE DE DATOS

## 3.1 Convenciones

* Tablas en plural
* Campos en snake_case
* PK → `id` o `id_<entidad>`

---

## 3.2 Relaciones

* 1:N → Foreign Key
* N:M → tabla intermedia

---

## 3.3 Reglas clave

* No duplicar datos innecesarios
* Mantener normalización
* Evitar lógica en DB (usar servicios)

---

# 🔐 4. SEGURIDAD

## 4.1 Autenticación

* Siempre vía JWT
* Tokens en cookies HTTPOnly

---

## 4.2 Autorización

* Validar SIEMPRE en backend
* Nunca confiar solo en UI

---

## 4.3 Permisos

### Global

* RBAC (roles + permisos)

### Contextual (proyectos)

* Validar pertenencia
* Validar rol (coordinator / member)

---

## 4.4 Reglas críticas

❌ No exponer endpoints sin protección
❌ No asumir permisos sin validación

---

# 🎨 5. TEMPLATES (Jinja2)

## 5.1 Uso de macros

* Reutilizar:

  * botones
  * tablas
  * formularios

---

## 5.2 Lógica en templates

✔ Permitido:

* condicionales simples
* bucles

❌ No permitido:

* lógica compleja
* queries
* cálculos

---

## 5.3 Contexto

* Usar siempre macros con contexto:

```jinja
{% from "components/buttons.html" import button with context %}
```

---

## 5.4 Consistencia UI

* Mantener estilos AdminLTE
* Usar componentes existentes

---

# 📦 6. RUTAS

## 6.1 Convención Web

```text
/resource
/resource/form
/resource/{id}
/resource/{id}/edit
```

---

## 6.2 Convención API

```text
/api/resource
/api/resource/{id}
```

---

## 6.3 Reglas

* Evitar rutas ambiguas
* Definir rutas fijas antes que dinámicas

---

# 🧪 7. TESTING

## 7.1 Cobertura

* Mantener ≥ 85%

---

## 7.2 Qué testear

* Servicios
* Permisos
* Flujos principales

---

## 7.3 Tipos

* Unitarios
* Integración (prioritario a futuro)

---

# 🔄 8. REFACTORIZACIÓN

## 8.1 Cuándo refactorizar

* Código duplicado
* Lógica compleja
* Baja legibilidad

---

## 8.2 Reglas

* No romper funcionalidad
* Cambios pequeños
* Tests antes y después

---

# 🧠 9. NOMENCLATURA

## Variables

* `user_id`
* `project_id`

---

## Funciones

* `create_user`
* `assign_task`

---

## Clases

* PascalCase

---

# ⚠️ 10. ERRORES COMUNES A EVITAR

* Lógica en templates
* Validaciones solo en frontend
* Routers sobrecargados
* Duplicación de código
* Mezcla de naming

---

# 📌 11. REGLAS ESPECÍFICAS DEL PROYECTO

## Proyectos

* Usar `project_members` para roles
* No usar RBAC global para lógica de proyecto

---

## Tasks

* Siempre vinculadas a project
* Usar `assigned_to`
* Usar `status`

---

## Teams

* Organización, no ejecución
* No asignar tareas a equipos

---

# 🚀 12. REGLA DE ORO

👉 Si dudas dónde poner algo:

* ¿Es lógica? → Service
* ¿Es HTTP? → Router
* ¿Es visual? → Template

---

# 🧭 13. OBJETIVO FINAL

Código que sea:

* Legible
* Predecible
* Escalable
* Seguro

---
