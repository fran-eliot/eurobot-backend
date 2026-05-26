# app/core/websockets/ws_auth.py

# =========================================================
# 👤 CURRENT USER WEBSOCKET
# =========================================================
from fastapi import WebSocket
from sqlalchemy.orm import Session

from app.core.security import validate_access_token
from app.modules.users.user_model import User


def get_current_user_ws(websocket: WebSocket, db: Session):
    token = websocket.cookies.get("access_token")

    if not token:
        return None

    try:
        payload = validate_access_token(token)
    except Exception:
        return None

    user_id = payload.get("sub")

    return db.query(User).get(user_id)
