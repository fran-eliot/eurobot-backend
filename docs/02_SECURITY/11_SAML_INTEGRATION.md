# 12_SAML_INTEGRATION.md

# Integración SAML / SSO Institucional

## Propósito

Este documento describe la arquitectura de integración SAML/SSO de Aula Robótica Platform.

El objetivo es permitir autenticación institucional mediante la Universidad de Alcalá (UAH), integrando:

- Single Sign-On (SSO),
- identidades federadas,
- autenticación institucional,
- creación automática de usuarios,
- compatibilidad enterprise,
- futura integración OAuth2/OpenID Connect.

---

# Estado Actual

## Estado funcional

La integración SAML se encuentra:

```text
PARCIALMENTE IMPLEMENTADA
```

Actualmente existen:

- módulo SAML funcional,
- configuración dinámica,
- rutas SAML,
- generación de metadata,
- ACS endpoint,
- mock login funcional,
- integración JWT,
- integración Identity,
- creación automática de usuarios.

---

# Situación actual con UAH

Actualmente estamos pendientes de coordinación con el Servicio de Informática de la Universidad de Alcalá.

Falta confirmar:

- nombre oficial del aplicativo,
- entityId definitivo,
- IdP oficial,
- atributos SAML disponibles,
- certificado institucional,
- entorno producción,
- política de atributos,
- estrategia de logout institucional.

---

# Filosofía de Integración

La arquitectura SAML sigue varios principios:

## 1. Desacoplamiento

SAML no reemplaza el sistema IAM interno.

SAML únicamente proporciona autenticación.

El sistema interno sigue controlando:

- RBAC,
- permisos,
- autorización contextual,
- auditoría,
- ownership,
- sesiones funcionales.

---

## 2. Federation-ready Architecture

La plataforma está diseñada para:

```text
SAML
OAuth2
OpenID Connect
Google
GitHub
Azure AD
LDAP
```

---

## 3. Multi-provider Identity

Un usuario puede tener múltiples identidades.

Modelo:

```text
User
  ↕
Identity
```

:contentReference[oaicite:0]{index=0}
:contentReference[oaicite:1]{index=1}

---

# Arquitectura General

```text
UAH Identity Provider
            ↓
      SAML Response
            ↓
      ACS Endpoint
            ↓
    Identity Resolution
            ↓
      JWT Generation
            ↓
     SSR Auth Session
```

---

# Arquitectura de Módulos

## auth_saml/

Actualmente incluye:

```text
saml_config.py
saml_service.py
saml_web.py
```

---

# Configuración SAML

## saml_config.py

Centraliza la configuración del Service Provider (SP) y del Identity Provider (IdP). :contentReference[oaicite:2]{index=2}

---

# Configuración SP

El sistema actúa como:

```text
Service Provider (SP)
```

Configuración actual:

```python
"sp": {
    "entityId": ...,
    "assertionConsumerService": ...,
    "singleLogoutService": ...
}
```

:contentReference[oaicite:3]{index=3}

---

# Assertion Consumer Service (ACS)

Endpoint principal:

```text
/auth/saml/acs
```

Responsabilidad:

- recibir assertions SAML,
- validar autenticación,
- resolver usuario,
- generar JWT,
- crear sesión SSR.

---

# Metadata Endpoint

Endpoint:

```text
/auth/saml/metadata
```

Genera metadata XML del SP automáticamente. :contentReference[oaicite:4]{index=4}

Esto facilita integración con el IdP institucional.

---

# Configuración IdP

Actualmente configurable mediante variables de entorno:

```python
SAML_IDP_ENTITY_ID
SAML_IDP_SSO_URL
SAML_IDP_SLO_URL
SAML_IDP_CERT
```

:contentReference[oaicite:5]{index=5}

---

# OneLogin Toolkit

La integración utiliza:

```text
python3-saml
(OneLogin)
```

Actualmente mediante:

```python
OneLogin_Saml2_Auth
```

:contentReference[oaicite:6]{index=6}

---

# Flujo de Login SAML

## Paso 1 — Login

El usuario accede:

```text
/auth/saml/login
```

---

## Paso 2 — Redirect al IdP

El sistema redirige al proveedor institucional.

```python
return RedirectResponse(auth.login())
```

:contentReference[oaicite:7]{index=7}

---

## Paso 3 — Login institucional

El usuario autentica en la UAH.

---

## Paso 4 — Assertion SAML

La UAH devuelve assertion al ACS.

---

## Paso 5 — Validación

El sistema ejecuta:

```python
auth.process_response()
```

:contentReference[oaicite:8]{index=8}

---

## Paso 6 — Extracción de atributos

Actualmente se esperan:

```python
mail
displayName
```

:contentReference[oaicite:9]{index=9}

---

# Limitación Actual

Todavía NO sabemos oficialmente qué atributos enviará la UAH.

Actualmente los atributos están asumidos provisionalmente:

```python
email = attrs.get("mail", [""])[0]
name = attrs.get("displayName", [email])[0]
```

:contentReference[oaicite:10]{index=10}

Esto deberá ajustarse cuando el Servicio de Informática confirme el esquema real.

---

# Resolución de Usuario

El sistema busca:

```python
Identity.email == email
```

:contentReference[oaicite:11]{index=11}

---

# Auto-provisioning

Si el usuario no existe:

## Se crea User

```python
user = User(...)
```

---

## Se crea Identity

```python
provider="uah_saml"
```

:contentReference[oaicite:12]{index=12}

---

# Arquitectura Multi-Identity

Esto permite:

```text
1 usuario
N identidades
```

Ejemplos futuros:

```text
local
uah_saml
google
github
```

---

# Integración con JWT

Tras autenticación:

```python
payload = build_auth_payload(user)
token = create_access_token(payload)
```

:contentReference[oaicite:13]{index=13}

---

# Integración con SSR

La sesión se mantiene mediante:

```python
response.set_cookie(
    "access_token",
    token,
    httponly=True,
    samesite="lax"
)
```

:contentReference[oaicite:14]{index=14}

---

# Arquitectura Híbrida

Actualmente el sistema soporta:

```text
Local Login
+
Federated Login
```

---

# Mock Login Actual

Mientras la integración institucional no está disponible, existe un sistema fake funcional:

```text
/auth/saml/mock
```

:contentReference[oaicite:15]{index=15}

---

# Objetivo del Mock

Permitir:

- desarrollo frontend,
- pruebas SSR,
- validación RBAC,
- integración JWT,
- simulación SSO,
- testing funcional.

---

# Funcionamiento del Mock

El mock:

1. Busca usuario demo UAH,
2. Genera JWT,
3. Inserta cookie,
4. Redirige al dashboard.

---

# Botón Fake en Login

Actualmente el login incluye un botón visual SSO fake.

Objetivo:

```text
Simular futura integración institucional
```

Esto permite:

- validar UX,
- validar flujos,
- preparar transición real.

---

# Seguridad Actual

## JWT HttpOnly

La sesión SSR usa cookies HttpOnly.

---

## SAML Strict Mode

Actualmente:

```python
"strict": True
```

:contentReference[oaicite:16]{index=16}

---

## Certificados

La validación x509 está preparada.

Actualmente pendiente de:

```text
certificado oficial UAH
```

---

# Arquitectura Identity-Centric

El núcleo real de autenticación es:

```text
Identity
```

NO:

```text
User
```

Esto es extremadamente importante.

---

# Beneficios de la Arquitectura

## Federation-ready

Preparado para SSO institucional.

---

## Escalabilidad

Soporta múltiples providers.

---

## Enterprise-ready

Arquitectura compatible con organizaciones reales.

---

## Bajo acoplamiento

SAML desacoplado del RBAC.

---

## SSR-compatible

Compatible con render server-side.

---

## Seguridad

Separación clara:

```text
Authentication
≠
Authorization
```

---

# Limitaciones Actuales

## Logout SAML incompleto

Actualmente no existe Single Logout real institucional.

---

## Metadata pendiente

Faltan datos definitivos UAH.

---

## Atributos desconocidos

La UAH aún no confirmó:

- uid,
- email,
- displayName,
- grupos,
- roles institucionales,
- identificadores internos.

---

## No existe refresh token

Actualmente solo JWT clásico.

---

## No existe mapping avanzado

No hay sincronización automática de roles institucionales.

---

# Futuras Evoluciones

## SSO real UAH

Objetivo principal inmediato.

---

## Role Mapping Institucional

Mapear:

```text
profesor UAH
alumno UAH
PAS
investigador
```

a roles internos.

---

## OAuth2/OpenID Connect

Compatibilidad futura.

---

## Azure AD / Microsoft

Posible integración institucional futura.

---

## LDAP Federation

Compatibilidad potencial.

---

## Group-based Authorization

Autorización basada en grupos SAML.

---

## Auto-sync de usuarios

Sincronización periódica institucional.

---

## SCIM Provisioning

Provisioning enterprise avanzado.

---

# Arquitectura Objetivo

La visión final es:

```text
Institutional Enterprise Identity Platform
```

capaz de soportar:

- SSO universitario,
- identidad federada,
- múltiples providers,
- operaciones administrativas,
- seguridad enterprise,
- autorización contextual avanzada.

---

# Impacto Arquitectónico

La integración SAML cambia radicalmente el nivel del proyecto.

La plataforma deja de ser únicamente:

```text
Aplicación académica
```

y evoluciona hacia:

```text
Enterprise-ready institutional platform
```

---

# Resumen

Actualmente la integración SAML ya dispone de:

- arquitectura preparada,
- endpoints funcionales,
- ACS operativo,
- metadata XML,
- integración JWT,
- auto-provisioning,
- mock login,
- soporte SSR,
- modelo multi-identidad.

Pendiente únicamente de:

- coordinación final con UAH,
- configuración oficial,
- atributos definitivos,
- certificados institucionales,
- activación producción.