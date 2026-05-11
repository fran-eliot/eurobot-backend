# app/modules/projects/projects_service.py
# 📋 Servicio de proyectos: lógica de negocio relacionada con proyectos, tareas y 
# actividades.


from sqlalchemy.orm import Session
from app.modules.projects.project_member_model import ProjectMember
from app.modules.projects.project_model import Project
from app.modules.users.user_model import User


def search_projects(
    db: Session,
    search: str = "",
    status: str = "all",
    page: int = 1,
    per_page: int = 10,
):
    query = db.query(Project)

    # 🔎 Buscar por nombre
    if search:
        query = query.filter(
            Project.name.ilike(f"%{search}%")
        )

    # 📊 Filtrar estado
    if status != "all":
        query = query.filter(
            Project.status == status
        )

    total = query.count()

    projects = (
        query.order_by(Project.id_project.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return projects, total


def get_available_users(db, project_id):
    subquery = db.query(ProjectMember.user_id).filter_by(project_id=project_id)
    return db.query(User).filter(~User.id_usuario.in_(subquery)).all()



def remove_member(db, project_id, user_id):
    member = db.query(ProjectMember).filter_by(
        project_id=project_id,
        user_id=user_id
    ).first()

    if member:
        db.delete(member)
        db.commit()