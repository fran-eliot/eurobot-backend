# app/modules/users/user_schemas.py
# 📦 Schemas para usuarios (validación y serialización)

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


# =========================================================
# 🧱 BASE
# =========================================================
class UserBase(BaseModel):
    """
    Schema base compartido para creación y actualización.
    """

    nombre: str = Field(
        ...,
        json_schema_extra={
            "example": "Laura García",
            "description": "Nombre completo del usuario",
        },
    )

    @field_validator("nombre")
    @classmethod
    def validate_nombre(cls, v: str) -> str:
        """
        Valida que el nombre no esté vacío y elimina espacios.
        """

        if not v or not v.strip():
            raise ValueError("El nombre es obligatorio")

        return v.strip()


# =========================================================
# ➕ CREATE
# =========================================================
class UserCreate(UserBase):
    """
    Schema para creación de usuario.
    Actualmente solo requiere nombre.
    """

    pass


# =========================================================
# ✏️ UPDATE
# =========================================================
class UserUpdate(UserBase):
    """
    Schema para actualización de usuario.
    Permite cambiar nombre y estado.
    """

    activo: bool | None = Field(
        default=None,
        json_schema_extra={
            "example": True,
            "description": "Estado del usuario (activo/inactivo)",
        },
    )


# =========================================================
# 📤 RESPONSE
# =========================================================
class UserResponse(BaseModel):
    """
    Schema de salida (API / serialización).
    """

    id_usuario: int = Field(
        json_schema_extra={"example": 1, "description": "ID único del usuario"}
    )

    nombre: str = Field(
        json_schema_extra={
            "example": "Laura García",
            "description": "Nombre completo del usuario",
        }
    )

    activo: bool = Field(
        json_schema_extra={
            "example": True,
            "description": "Estado del usuario (activo/inactivo)",
        }
    )

    fecha_creacion: datetime = Field(
        json_schema_extra={"example": "2024-01-01T00:00:00Z"}
    )

    model_config = ConfigDict(from_attributes=True)
