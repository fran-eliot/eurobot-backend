# app/core/websockets/router.py

# 📋 Router de WebSockets: define el endpoint para las conexiones WebSocket
# relacionadas con los proyectos. Este router se encarga de manejar las conexiones
# entrantes, verificar la autenticidad del usuario a través de JWT, y gestionar la
# suscripción a las salas de proyectos para enviar notificaciones en tiempo real a
# los usuarios cuando ocurren eventos importantes, como la creación o actualización
# de tareas.

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.authorization.project_permissions import user_in_project
from app.core.websockets.manager import manager
from app.core.websockets.ws_auth import get_current_user_ws
from app.db.session import get_db
from app.modules.projects.project_model import Project

router = APIRouter(prefix="/ws", tags=["WebSockets"])


# =========================================================
# 🔔 WEBSOCKET
# =========================================================
@router.websocket("/projects/{project_id}")
async def websocket_endpoint(
    websocket: WebSocket, project_id: int, db: Session = Depends(get_db)
):

    # ⚠️ recuperar usuario desde cookie JWT
    user = await get_current_user_ws(websocket, db)

    project = db.query(Project).get(project_id)

    if not user or not project or not user_in_project(user, project):
        await websocket.close(code=1008)
        return

    await manager.connect(websocket, project_id, user)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, project_id, user)


@router.websocket("/dashboard")
async def dashboard_websocket_endpoint(
    websocket: WebSocket,
    db: Session = Depends(get_db),
):
    user = await get_current_user_ws(websocket, db)

    if not user:
        await websocket.close(code=1008)
        return

    await manager.connect_dashboard(websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect_dashboard(websocket)


@router.websocket("/notifications")
async def notifications_websocket_endpoint(
    websocket: WebSocket,
    db: Session = Depends(get_db),
):
    user = await get_current_user_ws(websocket, db)

    if not user:
        await websocket.close(code=1008)
        return

    await manager.connect_user(websocket, user)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect_user(websocket, user)
