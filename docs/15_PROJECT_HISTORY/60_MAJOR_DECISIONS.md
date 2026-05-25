# 60_MAJOR_DECISIONS.md

## 1. Separar Usuario e Identidad
Decisión clave para permitir:
- múltiples métodos login,
- OAuth futuro,
- roles contextuales,
- desacoplamiento autenticación/autorización.

## 2. SSR en lugar de SPA
Se optó por:
- Jinja2,
- AdminLTE,
- SSR.

**Motivos:**
- mantenibilidad,
- continuidad académica,
- facilidad para futuros estudiantes.

## 3. Separación Web/API Routers
Decisión tomada desde el inicio.
Permitió:
- desacoplar frontend SSR y API,
- reutilización futura,
- escalabilidad.

## 4. Arquitectura modular
Refactor importante desde estructura CRUD tradicional hacia arquitectura desacoplada.

## 5. Sistema RBAC contextual
Decisión avanzada que permitió granularidad y flexibilidad superior al RBAC clásico.

## 6. Incorporar auditoría transversal
La auditoría dejó de ser una feature auxiliar para convertirse en parte estructural del sistema.

## 7. Evolución hacia plataforma completa
El proyecto dejó de ser exclusivamente IAM para convertirse en:
`Plataforma operativa del Aula de Robótica`