# app/db/init_db.py

from app.db.session import engine
from app.db.base import Base

# Importar modelos
from app.models.user import User
from app.models.role import Role
from app.models.identity import Identity
from app.models.user_role import UserRole

def init_db():
    Base.metadata.create_all(bind=engine)
