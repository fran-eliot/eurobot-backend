# app/db/init_db.py

from app.db.base import Base
from app.db.session import engine

# Importa todos los modelos para registrarlos en Base.metadata
# import app.db.models   Los importamos en main


def init_db():
    Base.metadata.create_all(bind=engine)
