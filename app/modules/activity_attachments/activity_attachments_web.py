# app/modules/activity_attachments/activity_attachments_web.py

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.authorization.activity_permissions import ensure_can_view_activity
from app.core.constants.actions import Actions
from app.core.constants.resources import Resources
from app.db.session import get_db
from app.modules.activities.activity_model import Activity
from app.modules.activity_attachments.activity_attachment_model import (
    ActivityAttachment,
)
from app.modules.auth.auth_dependencies_web import require_permission_web
from app.utils.flash import flash_success

router = APIRouter(prefix="/activity-attachments", tags=["Activity Attachments"])

UPLOAD_DIR = Path("storage/activity_attachments")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# SUBIR ARCHIVO
# =========================
@router.post("/upload")
async def upload_attachment(
    request: Request,
    activity_id: int = Form(...),
    file: UploadFile = File(...),
    description: str | None = Form(None),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission_web(
            Resources.ACTIVITIES,
            Actions.UPDATE,
        )
    ),
):

    activity = db.query(Activity).filter(Activity.id_activity == activity_id).first()

    if not activity:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    ensure_can_view_activity(db, current_user, activity)

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Nombre de archivo inválido",
        )

    extension = Path(file.filename).suffix
    unique_name = f"{uuid4()}{extension}"

    file_path = UPLOAD_DIR / unique_name

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="El archivo supera el tamaño máximo permitido",
        )

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    attachment = ActivityAttachment(
        activity_id=activity.id_activity,
        description=description,
        uploaded_by=current_user.id_usuario,
        original_filename=file.filename,
        stored_filename=unique_name,
        file_path=str(file_path),
        mime_type=file.content_type,
        size_bytes=len(content),
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    flash_success(request, "Archivo subido correctamente")

    print("SESSION DESPUÉS DE FLASH:", request.session)

    return RedirectResponse(
        f"/activities/{activity.id_activity}",
        status_code=303,
    )


# =========================
# DESCARGAR ARCHIVO
# =========================
@router.get("/{attachment_id}/download")
def download_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission_web(
            Resources.ACTIVITIES,
            Actions.READ,
        )
    ),
):

    attachment = (
        db.query(ActivityAttachment)
        .filter(ActivityAttachment.id_attachment == attachment_id)
        .first()
    )

    if not attachment:
        raise HTTPException(status_code=404, detail="Adjunto no encontrado")

    ensure_can_view_activity(db, current_user, attachment.activity)

    file_path = Path(attachment.file_path)

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Archivo no existe")

    return FileResponse(
        path=file_path,
        filename=attachment.original_filename,
        media_type=attachment.mime_type,
    )


# =========================
# ELIMINAR ARCHIVO
# =========================
@router.post("/{attachment_id}/delete")
def delete_attachment(
    request: Request,
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission_web(
            Resources.ACTIVITIES,
            Actions.DELETE,
        )
    ),
):

    attachment = (
        db.query(ActivityAttachment)
        .filter(ActivityAttachment.id_attachment == attachment_id)
        .first()
    )

    if not attachment:
        raise HTTPException(status_code=404, detail="Adjunto no encontrado")

    ensure_can_view_activity(db, current_user, attachment.activity)

    file_path = Path(attachment.file_path)

    if file_path.exists():
        file_path.unlink()

    activity_id = attachment.activity_id

    db.delete(attachment)
    db.commit()

    flash_success(request, "Adjunto eliminado correctamente")

    return RedirectResponse(
        f"/activities/{activity_id}",
        status_code=303,
    )
