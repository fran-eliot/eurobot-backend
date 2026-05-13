# app/utils/flash.py

from fastapi import Request


FLASH_KEY = "_flash_messages"


def add_flash(request: Request, message: str, category: str = "success"):
    """
    Guarda mensajes flash en sesión para sobrevivir a RedirectResponse.
    """
    flashes = request.session.get(FLASH_KEY, [])

    flashes.append({
        "message": message,
        "category": category,
    })

    request.session[FLASH_KEY] = flashes


def get_flash(request: Request):
    """
    Recupera y consume los mensajes flash una sola vez por request.
    Si el contexto se construye varias veces, reutiliza el mismo resultado.
    """
    if hasattr(request.state, "_cached_flash_messages"):
        return request.state._cached_flash_messages

    flashes = request.session.pop(FLASH_KEY, [])

    request.state._cached_flash_messages = flashes

    return flashes


def flash_success(request: Request, msg: str):
    add_flash(request, msg, "success")


def flash_error(request: Request, msg: str):
    add_flash(request, msg, "danger")


def flash_warning(request: Request, msg: str):
    add_flash(request, msg, "warning")


def flash_info(request: Request, msg: str):
    add_flash(request, msg, "primary")