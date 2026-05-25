# app/core/utils/validation.py
# Utilidades para validación de datos, especialmente errores de Pydantic.


def format_pydantic_errors(errors):
    formatted = {}

    for err in errors:
        field = err["loc"][-1]
        msg = err["msg"]

        if field not in formatted:
            formatted[field] = []

        formatted[field].append(msg)

    return formatted
