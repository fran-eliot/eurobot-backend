# 41_GITHUB_ACTIONS.md

# GitHub Actions Architecture

## Objetivo

Este documento describe la integración actual de GitHub Actions dentro de Aula Robótica Platform.

Actualmente GitHub Actions constituye el núcleo del sistema CI automatizado del proyecto.

---

# Estado Actual

# GitHub Actions implementado

Actualmente sí existe integración activa mediante:

```text
.github/workflows/tests.yml
```

---

# Objetivos actuales

La pipeline automatiza:

- testing,
- linting,
- coverage,
- quality gates,
- análisis SonarCloud.

---

# Filosofía

Cada push o Pull Request debe validar automáticamente:

```text
calidad + estabilidad + mantenibilidad
```

---

# Arquitectura Pipeline

```text
Push / PR
    ↓
GitHub Actions
    ↓
Install Dependencies
    ↓
Linting
    ↓
Pytest
    ↓
Coverage
    ↓
SonarCloud
    ↓
GitHub Status
```

---

# Capacidades Actuales

# Testing

La pipeline ejecuta:

```text
pytest
```

para validar backend y lógica funcional.

---

# Linting

La pipeline valida:

- estilo,
- consistencia,
- calidad base.

---

# Coverage

El sistema incluye:

```text
coverage gate
```

para impedir degradación progresiva.

---

# SonarCloud

Integración activa para:

- bugs,
- code smells,
- duplicación,
- maintainability,
- technical debt.

---

# Filosofía Quality Gate

El objetivo NO es solo "que compile".

La pipeline busca:

- proteger arquitectura,
- controlar deuda técnica,
- mantener calidad evolutiva.

---

# Runtime CI

# Dependency Management

La plataforma ya usa:

```text
uv
pyproject.toml
uv.lock
```

como stack moderno Python.

---

# Beneficios

- velocidad,
- reproducibilidad,
- resolución consistente.

---

# Integración SonarCloud

Archivo relacionado:

```text
sonar-project.properties
```

---

# Objetivos

## Static Analysis

Analizar:

- backend,
- arquitectura,
- mantenibilidad.

---

# Quality Trends

Permitir evolución sostenible del proyecto.

---

# GitHub Workflow Philosophy

La arquitectura sigue:

```text
automation-first development
```

---

# Beneficios

## Desarrollo más seguro

Errores detectados antes de merge.

---

## Refactor continuo

Mayor confianza al evolucionar arquitectura.

---

## Enterprise readiness

Base sólida DevOps.

---

# Pull Requests

La pipeline está preparada para actuar como:

```text
quality gate before merge
```

---

# Estrategia Evolutiva

Actualmente:

```text
CI only
```

---

# Futuro previsto

## CD

Deploy automático.

---

## Multi-environment

- dev,
- staging,
- production.

---

## Docker build

Build automático imágenes.

---

## Security scanning

- secrets,
- dependencies,
- vulnerabilities.

---

# Posibles futuras pipelines

# Backend Pipeline

- tests,
- lint,
- coverage,
- security.

---

# Frontend Pipeline

Futuro JS modular.

---

# Realtime Testing Pipeline

Futuro:

- websocket testing,
- realtime integration.

---

# Deployment Pipeline

Futuro:

```text
build
→ deploy
→ healthcheck
→ rollback
```

---

# Riesgos Actuales

## 1. Sin deploy

GitHub Actions todavía NO despliega.

---

## 2. Sin Docker build

Containerización aún pendiente.

---

## 3. Realtime testing limitado

Poca cobertura WebSockets.

---

## 4. Frontend testing parcial

JS architecture todavía evolucionando.

---

# Roadmap GitHub Actions

# Corto plazo

- mejorar cobertura,
- mejorar reporting,
- realtime tests.

---

# Medio plazo

- Docker build,
- staging deploy,
- security scanning.

---

# Largo plazo

- multi-env pipelines,
- observability checks,
- distributed deployment.

---

# Valor Arquitectónico

GitHub Actions ya representa uno de los pilares DevOps más maduros del proyecto.

Actualmente aporta:

- automatización,
- calidad continua,
- feedback rápido,
- control técnico,
- protección arquitectura.

---

# Relación con otros documentos

Relacionado con:

- `39_CI_CD.md`
- `40_DOCKER.md`
- `42_ENVIRONMENT.md`
- `16_TESTING_STATUS.md`
- `36_MONITORING.md`

---

# Conclusión

La integración actual con GitHub Actions proporciona una base moderna y profesional de integración continua.

Aunque todavía no existe despliegue automatizado, el proyecto ya dispone de:

- testing automatizado,
- linting,
- coverage,
- SonarCloud,
- pipelines reproducibles,
- quality gates.

La siguiente gran evolución será:

```text
full CI/CD + containerized deployment
```

## Workflow final implementado

El workflow definitivo incluye:

- cache de dependencias,
- creación automática de entorno,
- ejecución Ruff,
- pytest con cobertura,
- upload de artifacts,
- integración SonarCloud.

El pipeline permite validar automáticamente la calidad del proyecto en cada ejecución.

```yml
name: CI Pipeline

on:
#  push:
#  pull_request:
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install uv
        run: python -m pip install --upgrade pip uv

      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: |
            ~/.cache/uv
            .venv
          key: uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}
          restore-keys: |
            uv-${{ runner.os }}-

      - name: Install dependencies
        run: uv sync --dev

      - name: Create env
        run: |
          cat > .env <<EOF
          DATABASE_URL=sqlite:///./test.db
          SECRET_KEY=supersecretkey
          ACCESS_TOKEN_EXPIRE_MINUTES=60
          DEBUG=true
          APP_BASE_URL=http://localhost:8000
          SAML_ENTITY_ID=http://localhost:8000
          SAML_ACS_URL=http://localhost:8000/auth/saml/acs
          SAML_METADATA_URL=http://localhost:8000/auth/saml/metadata
          EOF

      - name: Run linter
        run: uv run ruff check app tests

      # Gate temporal. Luego subir a 90+
      - name: Run tests with coverage
        run: |
          uv run pytest \
            --cov=app \
            --cov-report=term-missing \
            --cov-report=xml \
            --cov-fail-under=75 \
            -v

      - name: Upload coverage artifact
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.xml
  sonar:
    name: SonarCloud Scan
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install uv
        run: python -m pip install --upgrade pip uv

      - name: Install dependencies
        run: uv sync --dev

      - name: Create env
        run: |
          cat > .env <<EOF
          DATABASE_URL=sqlite:///./test.db
          SECRET_KEY=supersecretkey
          EOF

      - name: Generate coverage
        run: uv run pytest --cov=app --cov-report=xml

      - name: SonarCloud Scan
        uses: SonarSource/sonarqube-scan-action@v6
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```
