# app/core/utils/audit_ui.py
# Utilidades para la interfaz de auditoría (iconos, etiquetas, etc.)


def get_audit_icon(action: str) -> str:

    action = action.upper()

    mapping = {
        # 👤 USERS
        "CREATE_USER": "fa-user-plus",
        "DELETE_USER": "fa-user-times",
        "ACTIVATE_USER": "fa-check",
        "DEACTIVATE_USER": "fa-ban",
        # 🔐 AUTH
        "LOGIN": "fa-sign-in-alt",
        "LOGOUT": "fa-sign-out-alt",
        # 📁 PROJECTS
        "CREATE_PROJECT": "fa-folder-plus",
        "UPDATE_PROJECT": "fa-folder-open",
        "DELETE_PROJECT": "fa-folder-minus",
        # ✅ TASKS
        "CREATE_TASK": "fa-plus-circle",
        "UPDATE_TASK": "fa-edit",
        "DELETE_TASK": "fa-trash",
        "TASK_STATUS_CHANGE": "fa-tasks",
    }

    return mapping.get(action, "fa-info-circle")


def get_audit_color(action: str) -> str:
    action = action.upper()

    if "DEACTIVATE" in action:
        return "bg-warning"
        
    if "ACTIVATE" in action:
        return "bg-success"

    if "DELETE" in action:
        return "bg-danger"

    if "CREATE" in action:
        return "bg-success"

    if "UPDATE" in action:
        return "bg-warning"

    if "STATUS" in action:
        return "bg-warning"

    if "LOGIN" in action:
        return "bg-success"

    if "LOGOUT" in action:
        return "bg-secondary"

    return "bg-primary"
