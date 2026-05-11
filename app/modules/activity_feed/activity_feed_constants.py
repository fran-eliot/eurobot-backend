# aapp/modules/activity_feed/activity_feed_constants.py
# 📋 Constantes de feed de actividad: define los tipos de eventos que pueden ocurrir
# en el sistema y que se registran en los feeds de actividad, como creación de tareas,
# actualización de tareas, cambios de estado, comentarios, etc. Estas constantes se
# utilizan para categorizar y organizar las actividades en los historiales de actividad
# y en los feeds de actividad de los proyectos, facilitando la comprensión y seguimiento
# de las acciones realizadas por los usuarios dentro de la plataforma.

class FeedEvent:
    TASK_CREATED = "TASK_CREATED"
    TASK_UPDATED = "TASK_UPDATED"
    TASK_DELETED = "TASK_DELETED"
    TASK_STATUS_CHANGED = "TASK_STATUS_CHANGED"

    ACTIVITY_CREATED = "ACTIVITY_CREATED"
    ACTIVITY_UPDATED = "ACTIVITY_UPDATED"
    ACTIVITY_DELETED = "ACTIVITY_DELETED"

    PROJECT_CREATED = "PROJECT_CREATED"
    PROJECT_UPDATED = "PROJECT_UPDATED"
    PROJECT_DELETED = "PROJECT_DELETED"

    MEMBER_JOINED = "MEMBER_JOINED"
    MEMBER_REMOVED = "MEMBER_REMOVED"