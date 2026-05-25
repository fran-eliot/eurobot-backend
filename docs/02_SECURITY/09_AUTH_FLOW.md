# 09_AUTH_FLOW.md

# Flujo de Autenticación

## Propósito

Este documento describe el flujo completo de autenticación de Aula Robótica Platform.

Cubre:

- login SSR,
- generación de JWT,
- cookies HTTPOnly,
- refresh token,
- middleware de autenticación,
- inyección de usuario en `request.state`,
- contexto global SSR,
- dependencias de usuario autenticado,
- logout,
- autenticación WebSocket.

---

# Arquitectura General

La plataforma utiliza una arquitectura de autenticación basada en:

- email/password,
- JWT access token,
- JWT refresh token,
- cookies HTTPOnly,
- middleware FastAPI/Starlette,
- SSR con Jinja2,
- autorización posterior mediante RBAC.

---

# Flujo General

```text
Usuario
   ↓
GET /login
   ↓
POST /login
   ↓
authenticate_user()
   ↓
create_access_token()
create_refresh_token()
   ↓
Set-Cookie HTTPOnly
   ↓
Redirect /dashboard
   ↓
AuthMiddleware valida access_token
   ↓
request.state.user
   ↓
Context Injection SSR
   ↓
Render protegido
```

---

# 1. Login SSR

## Ruta

```text
GET /login
```

Renderiza el formulario de autenticación.

## Ruta de acción

```text
POST /login
```

Procesa:

- email,
- password,
- validación de credenciales,
- creación de tokens,
- auditoría de login,
- seteo de cookies,
- redirección al dashboard.

---

# 2. Validación de credenciales

El login delega la autenticación en:

```python
authenticate_user(db, email, password)
```

Este servicio debe validar:

- existencia de identity,
- password hash,
- usuario asociado,
- usuario activo,
- roles,
- permisos efectivos.

---

# 3. Password Hashing

La plataforma utiliza:

```python
CryptContext(schemes=["bcrypt"], deprecated="auto")
```

Funciones principales:

```python
hash_password(password)
verify_password(plain_password, hashed_password)
```

---

# 4. Access Token

El access token se genera mediante:

```python
create_access_token(data)
```

## Características

- firmado con `SECRET_KEY`,
- algoritmo `HS256`,
- expiración configurable,
- tipo interno `access`.

## Payload esperado

```json
{
  "sub": "1",
  "username": "Admin Principal",
  "roles": ["admin"],
  "permissions": [
    "users:read",
    "projects:create",
    "activities:update"
  ],
  "type": "access",
  "exp": 123456789
}
```

---

# 5. Refresh Token

El refresh token se genera mediante:

```python
create_refresh_token(data)
```

## Características

- firmado con `SECRET_KEY`,
- algoritmo `HS256`,
- expiración más larga,
- tipo interno `refresh`.

## Uso

Permite regenerar un nuevo access token sin obligar al usuario a iniciar sesión de nuevo.

---

# 6. Cookies HTTPOnly

Tras login correcto, el sistema crea dos cookies:

```text
access_token
refresh_token
```

## Configuración

```python
httponly=True
samesite="lax" if DEBUG else "strict"
secure=not DEBUG
path="/"
```

## Decisión arquitectónica

La plataforma no usa `localStorage`.

Los tokens viven en cookies HTTPOnly para reducir exposición frente a XSS.

---

# 7. Auditoría de Login

En cada login correcto se registra auditoría:

```text
LOGIN
```

Incluye:

- usuario,
- recurso,
- IP,
- User-Agent,
- timestamp,
- descripción.

---

# 8. Middleware de Autenticación

El middleware principal es:

```python
AuthMiddleware
```

Responsabilidades:

- ignorar rutas públicas,
- leer `access_token`,
- validar token,
- inyectar payload en `request.state.user`,
- intentar refresh automático si el access token falla,
- redirigir a login si no hay sesión válida.

---

# 9. Rutas públicas

El middleware permite acceso sin autenticación a:

```text
/login
/logout
/refresh
/favicon.ico
/static
/auth/saml
```

También evita interceptar rutas API:

```text
/api/*
```

---

# 10. Validación del Access Token

El middleware usa:

```python
validate_access_token(token)
```

Esta función:

- decodifica el JWT,
- valida firma,
- valida expiración,
- comprueba que `type == "access"`.

Si es válido:

```python
request.state.user = payload
```

---

# 11. Refresh Automático

Si el access token no es válido, el middleware intenta recuperar la sesión usando:

```text
refresh_token
```

## Flujo

```text
Access token inválido
   ↓
Leer refresh_token
   ↓
validate_refresh_token()
   ↓
refresh_access_token()
   ↓
Nuevo access_token
   ↓
request.state.user actualizado
   ↓
Set-Cookie access_token
```

---

# 12. Endpoint Manual de Refresh

## Ruta

```text
GET /refresh
```

Permite regenerar manualmente un access token desde el refresh token.

## Flujo

- leer cookie `refresh_token`,
- validar refresh token,
- generar nuevo access token,
- guardar nueva cookie `access_token`,
- redirigir a `/dashboard`.

---

# 13. Logout

## Ruta

```text
POST /logout
```

Responsabilidades:

- registrar auditoría `LOGOUT`,
- eliminar cookie `access_token`,
- eliminar cookie `refresh_token`,
- redirigir a `/login`.

## Cookies eliminadas

```python
response.delete_cookie("access_token", path="/")
response.delete_cookie("refresh_token", path="/")
```

---

# 14. Usuario actual en rutas web

Las rutas protegidas pueden obtener el usuario autenticado mediante:

```python
get_current_user_web()
```

Esta dependencia:

- lee `request.state.user`,
- extrae `sub`,
- busca el usuario en base de datos,
- valida existencia,
- enriquece el objeto `User` con roles y permisos del token.

---

# 15. Guards de autorización web

Sobre el usuario autenticado se aplican guards como:

```python
require_roles_web()
require_permission_web()
require_owner_or_permission_web()
require_permission_and_not_self_web()
```

Estos pertenecen ya a la fase de autorización, pero dependen directamente del flujo de autenticación.

---

# 16. Context Injection SSR

Una vez autenticado el usuario, el sistema construye el contexto global de plantillas mediante:

```python
get_template_context(request)
```

Este contexto incluye:

- usuario actual,
- roles,
- permisos,
- helpers de autorización,
- menú dinámico,
- breadcrumbs,
- flash messages,
- notifications,
- helpers visuales.

---

# 17. Fallback Context

Si no hay usuario o falla el contexto, se devuelve un contexto seguro:

```python
get_fallback_context()
```

Este contexto evita romper el render SSR y devuelve helpers seguros que siempre deniegan permisos.

---

# 18. Flash Messages y SessionMiddleware

La autenticación convive con `SessionMiddleware`, pero solo para estado temporal SSR.

Se usa para:

- flash messages,
- toasts,
- feedback visual tras redirects.

Importante:

```text
La autenticación NO depende de sesión server-side.
```

La autenticación real depende de JWT en cookies HTTPOnly.

---

# 19. Autenticación WebSocket

Los WebSockets validan usuario mediante cookie:

```python
websocket.cookies.get("access_token")
```

## Flujo

```text
WebSocket connection
   ↓
Leer access_token cookie
   ↓
validate_access_token()
   ↓
Extraer sub
   ↓
Buscar User en DB
   ↓
Aceptar o rechazar conexión
```

## Helper principal

```python
get_current_user_ws(websocket, db)
```

Si no hay token válido, devuelve `None`.

---

# 20. Diferencia entre Auth HTTP y Auth WebSocket

## HTTP SSR

- gestionado por `AuthMiddleware`,
- inyecta `request.state.user`,
- permite refresh automático,
- redirige a `/login`.

## WebSocket

- valida cookie manualmente,
- no redirige,
- no refresca automáticamente,
- debe cerrar o rechazar conexión si no hay usuario válido.

---

# 21. Seguridad actual

## Fortalezas

- tokens en cookies HTTPOnly,
- separación access/refresh,
- expiración de tokens,
- validación de tipo de token,
- middleware centralizado,
- integración SSR limpia,
- auditoría de login/logout,
- autenticación WebSocket por cookie.

---

# 22. Riesgos o mejoras pendientes

## CSRF

Pendiente protección formal CSRF para formularios POST.

Especialmente relevante porque se usan cookies.

---

## Refresh Token Rotation

Pendiente rotación avanzada de refresh tokens.

---

## Revocación de sesiones

Pendiente invalidar tokens activos desde servidor.

---

## WebSocket Refresh

Los WebSockets aún no tienen refresh automático.

---

## Cookies en producción

En producción debe garantizarse:

```text
secure=True
samesite=strict
https obligatorio
```

---

# 23. Checklist de flujo correcto

## Login

- [x] Validar credenciales
- [x] Crear access token
- [x] Crear refresh token
- [x] Guardar cookies HTTPOnly
- [x] Registrar auditoría
- [x] Redirigir a dashboard

## Request protegido

- [x] Leer access token
- [x] Validar token
- [x] Inyectar `request.state.user`
- [x] Construir contexto SSR
- [x] Render protegido

## Refresh

- [x] Leer refresh token
- [x] Validar tipo refresh
- [x] Generar nuevo access token
- [x] Guardar nueva cookie

## Logout

- [x] Registrar auditoría
- [x] Borrar cookies
- [x] Redirigir a login

## WebSocket

- [x] Leer access token desde cookie
- [x] Validar token
- [x] Resolver usuario
- [ ] Añadir reconnect seguro
- [ ] Añadir estrategia de expiración/refresh

---

# 24. Resumen

El flujo de autenticación actual es sólido y coherente con una arquitectura SSR enterprise:

```text
JWT + HTTPOnly Cookies + AuthMiddleware + SSR Context + RBAC
```

La siguiente evolución natural es reforzar:

- CSRF,
- refresh rotation,
- session revocation,
- websocket auth hardening,
- observabilidad de sesiones.