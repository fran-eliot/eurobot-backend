# app/modules/notifications/notifications_web.py

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.render import render
from app.db.session import get_db
from app.modules.auth.auth_dependencies_web import get_current_user_web
from app.modules.notifications.notification_service import (
    count_unread_notifications,
    get_user_notifications,
    mark_all_notifications_as_read,
    mark_notification_as_read,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/")
def notifications_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_web),
):
    notifications = get_user_notifications(
        db,
        current_user.id_usuario,
        limit=50,
    )

    unread_count = count_unread_notifications(
        db,
        current_user.id_usuario,
    )

    return render(
        request,
        "notifications/notifications_list.html",
        {
            "notifications": notifications,
            "unread_count": unread_count,
        },
    )


@router.post("/{notification_id}/read")
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_web),
):
    notification = mark_notification_as_read(
        db,
        notification_id,
        current_user.id_usuario,
    )

    if not notification:
        raise HTTPException(404, "Notificación no encontrada")

    db.commit()

    return JSONResponse({"ok": True})


@router.post("/read-all")
def read_all_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_web),
):
    marked = mark_all_notifications_as_read(
        db,
        current_user.id_usuario,
    )

    db.commit()

    return JSONResponse(
        {
            "ok": True,
            "marked": marked,
        }
    )


@router.get("/{notification_id}/open")
def open_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_web),
):
    notification = mark_notification_as_read(
        db,
        notification_id,
        current_user.id_usuario,
    )

    if not notification:
        raise HTTPException(404, "Notificación no encontrada")

    db.commit()

    return RedirectResponse(
        notification.url or "/dashboard",
        status_code=303,
    )
