# app/core/authorization/project_permissions.py

# 📋 Permisos específicos para proyectos: funciones que verifican si un usuario tiene
# permisos específicos relacionados con proyectos, como ser coordinador o tener
# permisos de gestión. Estas funciones se utilizan en las dependencias de autorización
# para controlar el acceso a las rutas relacionadas con proyectos, asegurando que solo
# los usuarios autorizados puedan acceder.


def is_project_member(user, project):
    return any(
        m.user_id == user.id_usuario
        for m in project.members
    )


def is_project_coordinator(user, project):
    if not user or not project:
        return False

    return any(
        m.user_id == user.id_usuario
        and (
            m.role == "coordinator"
            or getattr(m.role, "value", None) == "coordinator"
        )
        for m in project.members
    )


def can_manage_project(user, project):
    # admin global
    if "admin" in [r.name for r in user.roles]:
        return True

    return is_project_coordinator(user, project)


def can_view_tasks(user, project):
    return is_project_member(user, project)


def can_manage_tasks(user, project):
    return is_project_coordinator(user, project)


def can_view_tasks(user, project):
    return is_project_member(user, project)


def can_manage_tasks(user, project):
    return is_project_coordinator(user, project)


def user_in_project(user, project):
    return any(m.user_id == user.id_usuario for m in project.members)


def can_update_own_task(user, task):
    return task.assigned_to == user.id_usuario