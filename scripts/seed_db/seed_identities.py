# scripts/seed_db/seed_identities.py
# Este archivo define la función para insertar datos de identidades en la base de
# datos.

from app.core.security import hash_password
from app.modules.identities.identity_model import Identity


def local_identity(user, email):
    return Identity(
        email=email,
        provider="local",
        password_hash=hash_password("1234"),
        user_id=user.id_usuario,
    )


def saml_identity(user, email):
    return Identity(
        email=email, provider="uah_saml", password_hash=None, user_id=user.id_usuario
    )


def seed_identities(db, users):
    identities = []

    admins = users["admins"]
    profesores = users["profesores"]
    alumnos = users["alumnos"]
    uah_users = users["uah_users"]

    identities.append(local_identity(admins[0], "admin1@robotica.es"))
    identities.append(local_identity(admins[1], "admin2@robotica.es"))

    for i, p in enumerate(profesores):
        identities.append(local_identity(p, f"profesor{i + 1}@uah.es"))

    for i, a in enumerate(alumnos):
        identities.append(local_identity(a, f"alumno{i + 1}@uah.es"))

    identities.append(saml_identity(uah_users[0], "user_uah@uah.es"))

    db.add_all(identities)
    db.commit()
