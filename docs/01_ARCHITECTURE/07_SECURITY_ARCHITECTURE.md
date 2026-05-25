# 07_SECURITY_ARCHITECTURE.md

# Arquitectura de Seguridad

# 📌 Filosofía de Seguridad

La plataforma sigue un enfoque:

- backend-first security
- zero trust UI
- contextual authorization
- SSR-safe authentication

---

# 🔐 Autenticación

## JWT

El sistema utiliza:

- access tokens
- refresh tokens
- expiración controlada

---

## HTTPOnly Cookies

Los tokens se almacenan mediante cookies seguras.

Ventajas:

- protección XSS
- SSR compatibility
- seguridad backend

---

## SessionMiddleware

Usado para:

- flash messages
- temporary UI state
- toast persistence

---

# 🛡️ Autorización

# RBAC Global

Permisos clásicos:

```text
users:create
tasks:update
projects:delete
```
---

### Contextual Authorization
Validaciones dinámicas:
- ownership
- coordinadores
- permisos contextuales
- relaciones ORM

## 🧠 Permission Helpers

### can_user_action()
Motor centralizado de autorización.
Compatible con:
- JWT payload
- ORM users
- contextual roles
- effective permissions

## 🔒 Seguridad UI
Toda acción crítica:
- se valida backend
- no depende de frontend
- no confía en UI

## 📡 Seguridad Realtime
Validaciones websocket:
- JWT válido
- usuario activo
- room isolation
- project membership

## 🧾 Auditoría
Toda acción sensible genera:
- audit logs
- metadata
- timestamps
- actor tracking

## 🚀 Evolución futura
- SAML SSO
- OAuth2
- 2FA
- CSRF hardening
- session revocation
- centralized secrets