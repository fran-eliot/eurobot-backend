# app/core/deps/api_auth.py

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.authorization.roles import has_required_role
from app.core.deps.security_schemes import oauth2_scheme
from app.core.security import validate_access_token
from app.db.session import get_db
from app.modules.users.user_model import User


def get_current_user_api(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = validate_access_token(token)

    user_id = payload.get("sub")
    roles = payload.get("roles", [])

    if not user_id:
        raise HTTPException(status_code=401)

    user = db.query(User).filter(User.id_usuario == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=401)

    user.roles_token = roles
    return user


def require_roles_api(*allowed_roles: str):

    def role_checker(current_user: User = Depends(get_current_user_api)):

        if not has_required_role(current_user.roles_token, list(allowed_roles)):
            raise HTTPException(status_code=403)

        return current_user

    return role_checker


# shortcuts
require_admin_api = require_roles_api("admin")
require_profesor_api = require_roles_api("profesor")
require_estudiante_api = require_roles_api("estudiante")
