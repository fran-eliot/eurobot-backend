# app/modules/auth_saml/saml_web.py
# Este módulo define las rutas web para la autenticación SAML.

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.session import get_db
from app.modules.auth.auth_service import build_auth_payload
from app.modules.auth_saml.saml_config import get_saml_settings
from app.modules.auth_saml.saml_service import get_saml_auth
from app.modules.identities.identity_model import Identity
from app.modules.users.user_model import User
from app.utils.flash import flash_error

router = APIRouter(prefix="/auth/saml", tags=["SAML"])


@router.get("/login")
def saml_login(request: Request):
    auth = get_saml_auth(request, get_saml_settings())
    return RedirectResponse(auth.login())


@router.get("/mock")
def mock_login(db: Session = Depends(get_db)):

    identity = db.query(Identity).filter(Identity.email == "user_uah@uah.es").first()

    if not identity:
        raise HTTPException(status_code=404, detail="Usuario demo UAH no encontrado")

    user = identity.usuario

    payload = build_auth_payload(user)
    token = create_access_token(payload)

    response = RedirectResponse("/dashboard", status_code=302)

    response.set_cookie("access_token", token, httponly=True, samesite="lax")

    return response


@router.get("/metadata")
def metadata():
    auth = get_saml_auth
    print("Obteniendo metadata SAML con settings:", auth)
    settings = get_saml_settings()

    from onelogin.saml2.settings import OneLogin_Saml2_Settings

    saml_settings = OneLogin_Saml2_Settings(settings)

    metadata = saml_settings.get_sp_metadata()
    return Response(content=metadata, media_type="text/xml")


@router.post("/acs")
def acs(request: Request, db: Session = Depends(get_db)):
    auth = get_saml_auth(request, get_saml_settings())

    auth.process_response()
    errors = auth.get_errors()

    if errors:
        flash_error(request, "Error autenticando con UAH")
        return RedirectResponse("/login", status_code=302)

    if not auth.is_authenticated():
        flash_error(request, "No autenticado")
        return RedirectResponse("/login", status_code=302)

    attrs = auth.get_attributes()

    email = attrs.get("mail", [""])[0]
    name = attrs.get("displayName", [email])[0]

    identity = db.query(Identity).filter(Identity.email == email).first()

    if identity:
        user = identity.usuario
    else:
        user = User(nombre=name, activo=True)
        db.add(user)
        db.flush()

        identity = Identity(
            email=email,
            provider="uah_saml",
            user_id=user.id_usuario,
            password_hash=None,
        )
        db.add(identity)
        db.commit()

    payload = build_auth_payload(user)

    token = create_access_token(payload)

    response = RedirectResponse("/dashboard", status_code=302)

    response.set_cookie("access_token", token, httponly=True, samesite="lax")

    return response
