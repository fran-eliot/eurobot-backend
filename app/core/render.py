# app/core/render.py
# Centraliza la lógica de renderizado de plantillas, incluyendo el contexto común para
# todas las vistas.

from app.core.templates import templates
from app.web.context import get_template_context


def render(request, template_name, extra=None):
    context = get_template_context(request)

    # Debug: mostrar claves del contexto
    print(f"Context Keys for render: {context.keys()}")

    if extra:
        context.update(extra)

    return templates.TemplateResponse(request, template_name, context)
