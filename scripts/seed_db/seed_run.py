# scripts/seed_db/seed_run.py

from app.db.session import SessionLocal

# Importante si no lo haces ya en main/reset:
# asegura que los modelos estén registrados en Base.metadata
# import app.db.models 

from scripts.seed_db.seed_audit import seed_audit
from scripts.seed_db.seed_identities import seed_identities
from scripts.seed_db.seed_roles import seed_roles
from scripts.seed_db.seed_users import seed_users
from scripts.seed_db.seed_projects import seed_projects
from scripts.seed_db.seed_notifications import seed_notifications


def run():
    db = SessionLocal()

    try:
        print("🌱 Iniciando seed...")

        roles, permissions = seed_roles(db)
        users = seed_users(db, roles)
        seed_identities(db, users)
        seed_audit(db, users)
        seed_projects(db)
        seed_notifications(db)

        print("✅ Seed completado correctamente")

    finally:
        db.close()


if __name__ == "__main__":
    run()