# Eurobot Backend API

Backend desarrollado en FastAPI para la gestión de autenticación y autorización del sistema de competición robótica Eurobot Spain.

## Tecnologías

- Python 3.12
- FastAPI
- SQLAlchemy
- MariaDB
- uv (gestión de dependencias)
- JWT

## Estructura

Arquitectura modular con separación de:
- Modelos ORM
- Esquemas Pydantic
- Servicios
- Repositorios
- API routers

## Configuración

1. Crear base de datos `eurobot` en MariaDB
2. Configurar variables en `.env`
3. Ejecutar:

```bash
uv run python -m app.db.init_db
