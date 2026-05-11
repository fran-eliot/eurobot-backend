# aapp/modules/activity_feed/activity_feed_utils.py
# 🛠️ Utilidades para feed de actividad: funciones auxiliares para formatear mensajes 
# de actividad, obtener íconos y colores para diferentes tipos de eventos, y otras 
# tareas relacionadas. Estas utilidades ayudan a mantener el código organizado y 
# reutilizable, facilitando la generación de mensajes de actividad consistentes y la 
# personalización de la apariencia de los feeds de actividad en la interfaz de usuario.


def get_feed_icon(event_type: str) -> str:
    mapping = {
        "TASK_CREATED": "fa-plus-circle",
        "TASK_UPDATED": "fa-pen",
        "TASK_DELETED": "fa-trash",
        "TASK_STATUS_CHANGED": "fa-exchange-alt",
        "ACTIVITY_CREATED": "fa-layer-group",
        "ACTIVITY_UPDATED": "fa-pen-to-square",
        "ACTIVITY_DELETED": "fa-trash",
        "PROJECT_UPDATED": "fa-diagram-project",
        "MEMBER_JOINED": "fa-user-plus",
        "MEMBER_REMOVED": "fa-user-minus",
    }

    return mapping.get(event_type, "fa-info-circle")


def get_feed_color(event_type: str) -> str:
    if not event_type:
        return "bg-secondary"

    if "DELETED" in event_type or "REMOVED" in event_type:
        return "bg-danger"

    if "CREATED" in event_type or "JOINED" in event_type:
        return "bg-success"

    if "STATUS" in event_type:
        return "bg-warning"

    if "UPDATED" in event_type:
        return "bg-primary"

    return "bg-secondary"



