# scripts/init_db.py
# Script para inicializar la base de datos creando las tablas necesarias.

from app.db.base import Base
from app.db.session import engine

print("📦 Creando tablas...")
Base.metadata.create_all(bind=engine)
print("✔ Tablas creadas")
