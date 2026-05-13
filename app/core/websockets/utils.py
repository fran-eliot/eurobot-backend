# app/core/websockets/utils.py
# 📋 Utilidades para WebSockets: funciones auxiliares que facilitan el manejo de 
# eventos relacionados con WebSockets, como emitir eventos a los clientes conectados 
# sin bloquear el flujo principal. Estas funciones se utilizan en los servicios para 
# enviar notificaciones en tiempo real a los usuarios cuando ocurren eventos 
# importantes, como la creación o actualización de tareas, sin necesidad de que los 
# usuarios tengan que refrescar la página.

import asyncio

from app.core.websockets.manager import manager


def emit_project_event(project_id: int, payload: dict):
    """
    Emite evento WS sin bloquear el flujo principal.
    """
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(
            manager.broadcast_to_project(project_id, payload)
        )
    except RuntimeError:
        # fallback si no hay loop (muy raro en FastAPI)
        asyncio.run(
            manager.broadcast_to_project(project_id, payload)
        )


def emit_dashboard_event(payload: dict):
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(
            manager.broadcast_dashboard(payload)
        )
    except RuntimeError:
        asyncio.run(
            manager.broadcast_dashboard(payload)
        )


def emit_user_event(user_id: int, payload: dict):
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(
            manager.broadcast_to_user(user_id, payload)
        )
    except RuntimeError:
        asyncio.run(
            manager.broadcast_to_user(user_id, payload)
        )