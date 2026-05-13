# app/main.py

# Este es el punto de entrada principal de la aplicación. 
# Aquí se configura FastAPI, se incluyen los routers y se monta 
# el directorio de archivos estáticos.

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from app.core.middleware.auth_middleware import AuthMiddleware
from app.modules.activities import activities_web
from app.modules.auth.auth_router import router as auth_router
from app.modules.auth_saml import saml_web
from app.modules.dashboard import dashboard_web
from app.modules.identities import identities_web
from app.modules.projects import projects_web
from app.modules.roles import roles_web
from app.modules.tasks import tasks_web
from app.modules.users import users_web
from app.modules.users.user_router import router as users_router
from app.web import auth_web
from app.core.websockets import router as ws_router
from app.modules.notifications import notifications_web
from app.modules.activity_attachments import activity_attachments_web
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
import app.db.models  # Importar modelos para que SQLAlchemy los reconozca

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Introduce el token JWT obtenido en /auth/login"
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(
    title="Aula de Robótica EPS-UAH Backend API",
    description="""
API REST para la gestión de autenticación, autorización y usuarios
del Aula de Robótica de la Escuela Politécnica Superior (Universidad de Alcalá).

### Funcionalidades principales:

- Autenticación basada en JWT (HS256)
- Autorización jerárquica basada en roles (RBAC)
- Gestión administrativa de usuarios (CRUD)
- Persistencia con MariaDB
- Arquitectura modular con FastAPI y SQLAlchemy
- Documentación automática OpenAPI

### Seguridad:
Todos los endpoints (excepto login) requieren autenticación mediante Bearer Token.

""",
    version="1.0.0",
    contact={
        "name": "Francisco Ramírez Martín",
        "email": "ramirez.martin.francisco@gmail.com"
    }
)

# Middleware de sesión PRIMERO
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
)

# Middleware de autenticación DESPUÉS
app.add_middleware(AuthMiddleware)

# 🔐 API
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])

# 🌐 WEB
app.include_router(auth_web.router, tags=["Authentication Web"])
app.include_router(saml_web.router, tags=["SAML Authentication Web"])
app.include_router(dashboard_web.router, tags=["Dashboard Web"])
app.include_router(users_web.router, tags=["Users Web"])
app.include_router(identities_web.router, tags=["Identities Web"])
app.include_router(roles_web.router, tags=["Roles Web"])
app.include_router(projects_web.router, tags=["Projects Web"])
app.include_router(tasks_web.router, tags=["Tasks Web"])
app.include_router(activities_web.router, tags=["Activities Web"])
app.include_router(ws_router.router, tags=["WebSockets"])
app.include_router(notifications_web.router,tags=["Notifications"])
app.include_router(activity_attachments_web.router,tags=["Activity Attachments"])

# Montar directorio de archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar redirección de rutas sin barra al final
app.router.redirect_slashes = False

# Personalizar esquema OpenAPI para incluir seguridad JWT
app.openapi = custom_openapi



