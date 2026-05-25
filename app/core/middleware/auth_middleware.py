# core/middleware/auth_middleware.py
# 🔐 Middleware de autenticación y refresh automático

from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.security import validate_access_token, validate_refresh_token
from app.db.session import SessionLocal
from app.modules.auth.auth_service import refresh_access_token

PUBLIC_PATHS = [
    "/login",
    "/logout",
    "/refresh",
    "/favicon.ico",
    "/static",
    "/auth/saml",
]


def redirect_to_login():
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return response


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        path = request.url.path

        # 0. Evitar llamadas a la API
        if path.startswith("/api"):
            return await call_next(request)

        # 🟢 1. Rutas públicas
        if any(path.startswith(p) for p in PUBLIC_PATHS):
            return await call_next(request)

        access_token = request.cookies.get("access_token")

        print("COOKIES EN MIDDLEWARE:", request.cookies)

        # 🟡 2. No token → login
        if not access_token:
            return RedirectResponse("/login", status_code=302)

        # 🔵 3. Validar access token
        try:
            payload = validate_access_token(access_token)

            request.state.user = payload

            return await call_next(request)

        except (JWTError, HTTPException) as e:
            print(f"Error al validar el token: {e}")
            # 🔴 4. Intentar refresh automático
            refresh_token = request.cookies.get("refresh_token")

            if not refresh_token:
                return redirect_to_login()

            try:
                # 🔥 validar refresh token
                refresh_payload = validate_refresh_token(refresh_token)

                with SessionLocal() as db:
                    # 🔒 validar usuario y permisos desde refresh token
                    new_access_token = refresh_access_token(refresh_payload, db)

                # 🔥 decodificar nuevo access token
                new_payload = validate_access_token(new_access_token)

                request.state.user = new_payload

                response = await call_next(request)

                response.set_cookie(
                    key="access_token",
                    value=new_access_token,
                    httponly=True,
                    samesite="lax",
                    secure=False,  # Cambiar a True en producción
                    path="/",
                )

                return response

            except (JWTError, HTTPException) as e:
                print(f"Error al refrescar el token: {e}")
                return redirect_to_login()
