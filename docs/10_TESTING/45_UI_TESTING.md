# 45_UI_TESTING.md

# UI Testing Architecture

## Objetivo

Este documento describe la estrategia actual y futura de testing UI/SSR de Aula Robótica Platform.

Actualmente el frontend SSR ya dispone de una cobertura bastante relevante mediante:

- FastAPI TestClient,
- validación render SSR,
- testing formularios,
- testing permisos UI,
- testing redirects,
- testing context injection.

---

# Filosofía UI Testing

La plataforma usa una arquitectura:

```text
SSR-first
```

por tanto gran parte del testing UI se realiza validando:

- responses HTML,
- redirecciones,
- permisos,
- render contextual.

---

# Estrategia Actual

# SSR Route Testing

Actualmente se prueban rutas web como:

- login,
- users,
- roles,
- identities,
- dashboard.



---

# Validación HTML

Muchos tests validan:

```python
assert "texto" in response.text
```



---

# Formularios

Cobertura actual sobre:

- create,
- edit,
- delete,
- validation errors.

---

# Ejemplos

# Users



---

# Roles



---

# Identities



---

# Auth



---

# Redirect Testing

Muy usado actualmente.

Ejemplos:

```python
assert response.status_code in (302, 303)
```

---

# Objetivo

Validar:

- auth flows,
- permisos,
- redirects SSR.

---

# Contextual Rendering

El frontend SSR implementa rendering contextual.

Actualmente existe testing sobre:

- menús,
- breadcrumbs,
- permisos,
- helpers,
- flash messages.

:contentReference[oaicite:20]{index=20}

---

# Menu Testing

Existe cobertura sobre:

- filtrado permisos,
- activación menús,
- breadcrumbs dinámicos.



---

# RBAC UI Testing

Actualmente se prueban:

- acceso admin,
- restricciones student,
- permisos visuales SSR.

:contentReference[oaicite:22]{index=22}

---

# Filosofía Seguridad UI

La estrategia actual valida:

```text
render contextual + backend authorization
```

---

# Testing Validation Errors

Existen tests para:

- formularios inválidos,
- duplicados,
- validaciones.



---

# Helpers UI

Existe cobertura sobre:

- audit_ui,
- menu_service,
- context helpers.



---

# Frontend JS Actual

Actualmente NO existe testing formal JS.

No existen:

- Jest,
- Vitest,
- Cypress,
- Playwright.

---

# Estado JS Actual

El JS actual se valida mediante:

- testing manual,
- debugging browser,
- consola,
- integración SSR.

---

# Componentes JS actuales

# Dashboard

:contentReference[oaicite:25]{index=25}

---

# Notifications

:contentReference[oaicite:26]{index=26}

---

# Kanban Realtime

:contentReference[oaicite:27]{index=27}

---

# Filosofía Actual

La UI se encuentra en transición desde:

```text
SSR clásico
```

hacia:

```text
SSR + realtime enterprise UI
```

---

# Gaps Actuales

## 1. Sin browser automation

No existe testing navegador real.

---

## 2. Sin JS unit tests

No existe framework frontend testing.

---

## 3. Sin visual regression

No existe snapshot/visual testing.

---

## 4. Sin accessibility testing

Aún no implementado.

---

## 5. Realtime UI poco cubierto

Dashboard/Kanban todavía dependen mucho de testing manual.

---

# Roadmap UI Testing

# Corto plazo

- ampliar SSR coverage,
- testing dashboard,
- testing notifications.

---

# Medio plazo

- Playwright,
- testing dialogs,
- testing toasts,
- testing realtime UI.

---

# Largo plazo

- visual regression,
- accessibility testing,
- E2E collaborative flows.

---

# Arquitectura Objetivo

La visión futura es:

```text
Enterprise Realtime SSR Testing Platform
```

---

# Relación con otros documentos

Relacionado con:

- `44_TESTING_STRATEGY.md`
- `46_REALTIME_TESTING.md`
- `07_FRONTEND_ARCHITECTURE.md`
- `08_UI_ARCHITECTURE.md`
- `20_JS_ARCHITECTURE.md`

---

# Conclusión

Actualmente el proyecto ya posee una cobertura SSR bastante madura:

- formularios,
- permisos,
- redirects,
- contexto,
- menús,
- RBAC UI.

La siguiente gran evolución será:

```text
frontend realtime automated testing
```