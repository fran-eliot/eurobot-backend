# 31_ATTACHMENTS_MODULE.md

# Módulo de Adjuntos

## Objetivo

El módulo de adjuntos permite asociar archivos y evidencias a actividades dentro de Aula Robótica Platform.

Actualmente el sistema soporta:

- subida de archivos,
- almacenamiento persistente,
- descarga segura,
- eliminación controlada,
- metadatos enriquecidos,
- ownership tracking,
- validación de tamaño,
- integración visual avanzada.

---

# Filosofía del módulo

El sistema de adjuntos NO está diseñado como un simple upload aislado.

Actualmente funciona como:

```text
Evidence & Documentation System
```

integrado dentro del flujo operativo de actividades.

---

# Casos de Uso

## Evidencias técnicas

- fotos,
- PDFs,
- documentación,
- diseños,
- resultados.

---

## Seguimiento de trabajo

Permite demostrar:

- trabajo realizado,
- progreso,
- entregables,
- resultados parciales.

---

## Operación académica

Preparado para:

- competiciones,
- entregas,
- proyectos colaborativos,
- trazabilidad futura.

---

# Arquitectura General

```text
Activity Detail View
        ↓
Upload Form
        ↓
Activity Attachments Router
        ↓
Filesystem Storage
        ↓
Attachment Metadata
        ↓
SSR Rendering
```

---

# Componentes Principales

## Backend

```text
app/modules/activity_attachments/
├── activity_attachment_model.py
└── activity_attachments_web.py
```

---

## Frontend SSR

El sistema se integra principalmente en:

```text
activities_detail.html
```

:contentReference[oaicite:0]{index=0}

---

## Integración indirecta

También aparece contextualizado en:

```text
tasks_detail.html
projects_detail.html
```

mediante navegación desde actividades. 

---

# Arquitectura de Almacenamiento

# Filesystem Storage

Los archivos físicos se almacenan en:

```python
storage/activity_attachments/
```

:contentReference[oaicite:2]{index=2}

---

# Metadata Persistente

La base de datos almacena:

```text
original_filename
stored_filename
file_path
mime_type
size_bytes
uploaded_by
description
created_at
```

---

# Separación importante

## Archivo físico

```text
filesystem
```

## Metadata

```text
database
```

Esto desacopla:

- almacenamiento,
- render,
- ownership,
- auditoría futura.

---

# Router Principal

Archivo:

```text
activity_attachments_web.py
```

:contentReference[oaicite:3]{index=3}

---

# Rutas Principales

## Upload

```text
POST /activity-attachments/upload
```

---

## Download

```text
GET /activity-attachments/{attachment_id}/download
```

---

## Delete

```text
POST /activity-attachments/{attachment_id}/delete
```

---

# Seguridad del módulo

El módulo reutiliza permisos de Activities.

---

## Upload

Requiere:

```python
require_permission_web(
    Resources.ACTIVITIES,
    Actions.UPDATE
)
```

:contentReference[oaicite:4]{index=4}

---

## Download

Requiere:

```python
require_permission_web(
    Resources.ACTIVITIES,
    Actions.READ
)
```

:contentReference[oaicite:5]{index=5}

---

## Delete

Requiere:

```python
require_permission_web(
    Resources.ACTIVITIES,
    Actions.DELETE
)
```

:contentReference[oaicite:6]{index=6}

---

# Autorización Contextual

Además de RBAC global, se valida:

```python
ensure_can_view_activity()
```

:contentReference[oaicite:7]{index=7}

---

# Upload Pipeline

## Flujo completo

```text
POST upload
    ↓
validar actividad
    ↓
ensure_can_view_activity()
    ↓
validar filename
    ↓
leer contenido
    ↓
validar tamaño
    ↓
generar UUID filename
    ↓
persistir archivo
    ↓
crear metadata DB
    ↓
flash_success()
    ↓
redirect detalle actividad
```

:contentReference[oaicite:8]{index=8}

---

# UUID Filenames

El sistema NO almacena usando el nombre original.

Usa:

```python
uuid4()
```

más extensión original. :contentReference[oaicite:9]{index=9}

---

# Beneficios

## Seguridad

Evita:

- colisiones,
- path guessing,
- sobrescrituras.

---

## Escalabilidad

Permite múltiples archivos iguales.

---

# Validación de tamaño

Actualmente:

```python
MAX_FILE_SIZE = 10 * 1024 * 1024
```

```text
10 MB
```

:contentReference[oaicite:10]{index=10}

---

# MIME Tracking

El sistema registra:

```python
file.content_type
```

:contentReference[oaicite:11]{index=11}

---

# Metadata enriquecida

El sistema registra:

## Archivo original

```text
original_filename
```

---

## Archivo almacenado

```text
stored_filename
```

---

## Tamaño

```text
size_bytes
```

---

## MIME

```text
mime_type
```

---

## Uploader

```text
uploaded_by
```

---

## Descripción funcional

```text
description
```

---

# Download Pipeline

## Flujo

```text
GET download
    ↓
buscar attachment
    ↓
ensure_can_view_activity()
    ↓
validar existencia física
    ↓
FileResponse()
```

:contentReference[oaicite:12]{index=12}

---

# Descarga segura

La descarga usa:

```python
FileResponse()
```

con:

```python
filename=attachment.original_filename
media_type=attachment.mime_type
```

:contentReference[oaicite:13]{index=13}

---

# Delete Pipeline

## Flujo

```text
POST delete
    ↓
buscar attachment
    ↓
ensure_can_view_activity()
    ↓
eliminar archivo físico
    ↓
eliminar metadata DB
    ↓
flash_success()
    ↓
redirect detalle actividad
```

:contentReference[oaicite:14]{index=14}

---

# Eliminación física

El sistema elimina realmente el archivo:

```python
file_path.unlink()
```

:contentReference[oaicite:15]{index=15}

---

# Vista de Detalle de Actividad

Archivo:

```text
activities_detail.html
```

:contentReference[oaicite:16]{index=16}

---

# Arquitectura Visual

La sección de adjuntos funciona como submódulo embebido.

---

# Componentes visuales

## Upload Box

```text
attachment-upload-box
```

---

## Attachment List

```text
attachment-list
```

---

## Attachment Icon

```text
attachment-icon
```

---

# Upload Form

El formulario usa:

```html
enctype="multipart/form-data"
```

:contentReference[oaicite:17]{index=17}

---

# Campos soportados

## Archivo

```html
<input type="file">
```

---

## Descripción

```html
<input type="text">
```

---

## activity_id

```html
<input type="hidden">
```

---

# Render de Adjuntos

Cada adjunto muestra:

- icono contextual,
- nombre original,
- descripción,
- tamaño,
- uploader,
- fecha,
- botones de acción.

:contentReference[oaicite:18]{index=18}

---

# MIME-aware UI

La UI selecciona icono según tipo MIME.

## PDFs

```text
fa-file-pdf
```

---

## Imágenes

```text
fa-file-image
```

---

## Word

```text
fa-file-word
```

---

## Excel

```text
fa-file-excel
```

---

## ZIP

```text
fa-file-archive
```

---

## Texto

```text
fa-file-alt
```

:contentReference[oaicite:19]{index=19}

---

# Empty State

Si no existen adjuntos:

```text
Esta actividad aún no tiene adjuntos.
```

:contentReference[oaicite:20]{index=20}

---

# Confirm Dialog Integration

El borrado usa dialogs modernos mediante:

```javascript
confirmAction()
```

:contentReference[oaicite:21]{index=21}

---

# Declarative Pattern

Los forms usan:

```text
.delete-attachment-form
```

interceptados desde JS inline. :contentReference[oaicite:22]{index=22}

---

# Integración con Activities

El módulo depende completamente de Activities.

Toda navegación parte de:

```text
Activity Detail
```

---

# Integración con Tasks

Las tareas muestran actividades y sus evidencias indirectamente. :contentReference[oaicite:23]{index=23}

---

# Integración con Projects

Los proyectos muestran actividades recientes, conectando indirectamente con evidencias documentales. :contentReference[oaicite:24]{index=24}

---

# Integración con Flash/Toast

El módulo usa:

```python
flash_success()
```

para:

- upload,
- delete.

:contentReference[oaicite:25]{index=25}

---

# Estado Actual

## Implementado

- upload funcional,
- almacenamiento persistente,
- metadata enriquecida,
- download seguro,
- delete físico,
- UUID filenames,
- MIME-aware UI,
- integración SSR,
- dialogs modernos,
- ownership tracking,
- tamaño máximo,
- uploader tracking.

---

# Limitaciones actuales

## 1. Sin service layer

Toda la lógica vive en:

```text
activity_attachments_web.py
```

---

## 2. Sin validación MIME whitelist

Actualmente cualquier MIME es aceptado.

---

## 3. Sin antivirus/scanning

No existe validación avanzada de seguridad.

---

## 4. Sin thumbnails

Las imágenes no generan preview.

---

## 5. Sin drag & drop upload

La subida es tradicional.

---

## 6. Sin versionado

No hay historial de revisiones.

---

## 7. JS inline

La confirmación de borrado vive inline en template.

Debería migrarse a:

```text
js-confirm-form
```

---

# Mejoras Futuras

## Corto plazo

- MIME whitelist,
- refactor JS inline,
- logging de uploads,
- validación extensión.

---

## Medio plazo

- previews,
- thumbnails,
- drag & drop,
- progress bars,
- uploads async.

---

## Largo plazo

- cloud storage,
- versionado,
- OCR,
- tagging,
- búsqueda documental,
- antivirus,
- almacenamiento distribuido.

---

# Valor Arquitectónico

El módulo de adjuntos transforma Activities en un sistema real de evidencias operativas.

Permite evolucionar desde:

```text
simple tracking
```

hacia:

```text
documented operational workflow
```

---

# Conclusión

El sistema de adjuntos ya posee una arquitectura sorprendentemente madura para el estado actual del proyecto.

Actualmente incluye:

- almacenamiento desacoplado,
- metadata enriquecida,
- ownership,
- integración SSR,
- seguridad contextual,
- UI moderna,
- confirm dialogs,
- feedback visual,
- render inteligente por MIME.

El siguiente gran salto arquitectónico será:

```text
async uploads + cloud-ready architecture
```