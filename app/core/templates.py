# app/core/templates.py
# Configuración de templates Jinja2 y contexto global

from fastapi.templating import Jinja2Templates
from jinja2 import pass_context

from app.web.context import get_template_context

templates = Jinja2Templates(directory="app/templates")


@pass_context
def can(ctx, action, resource, target=None):
    request = ctx.get("request")

    if not request:
        return False

    context = get_template_context(request)
    return context["can"](action, resource, target)


templates.env.globals["can"] = can

templates.env.globals["get_template_context"] = get_template_context

# templates.env.globals.update({
#     "get_template_context": get_template_context,
#     "can": can,
# })
