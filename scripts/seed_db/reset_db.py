# scripts/reset_db.py
# Reinicia la base de datos de desarrollo

# Importa todos los modelos antes de drop_all/create_all
from app.db.base import Base
from app.db.session import engine
from scripts.seed_db.seed_run import run as seed_run


def reset_db():
    print("⚠ Reiniciando base de datos...")

    Base.metadata.drop_all(bind=engine)
    print("🗑 Tablas eliminadas")

    Base.metadata.create_all(bind=engine)
    print("🏗 Tablas creadas")

    seed_run()

    print("✅ Base reiniciada correctamente")


if __name__ == "__main__":
    reset_db()
