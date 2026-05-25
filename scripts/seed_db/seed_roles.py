# scripts/seed_db/seed_roles.py
# Este archivo define la función para insertar datos de roles y permisos en la
# base de datos.

from app.modules.roles.role_model import Permission, Role


def seed_roles(db):
    if db.query(Role).count() > 0:
        print("⚠ Base ya inicializada")
        exit()

    admin = Role(nombre="admin")
    profesor = Role(nombre="profesor")
    estudiante = Role(nombre="estudiante")
    uah_user = Role(nombre="uah_user")

    db.add_all([admin, profesor, estudiante, uah_user])
    db.commit()

    perms_data = [
        "users:read",
        "users:create",
        "users:update",
        "users:delete",
        "roles:read",
        "roles:create",
        "roles:update",
        "roles:delete",
        "identities:read",
        "identities:create",
        "identities:update",
        "identities:delete",
        "projects:read",
        "projects:create",
        "projects:update",
        "projects:delete",
        "tasks:read",
        "tasks:create",
        "tasks:update",
        "tasks:delete",
        "activities:read",
        "activities:create",
        "activities:update",
        "activities:delete",
        "dashboard:read",
        "students:read",
        "audit:read",
        "activity_feed:read",
    ]

    perms = {}

    for name in perms_data:
        p = Permission(nombre=name)
        db.add(p)
        db.flush()
        perms[name] = p

    admin.permissions = list(perms.values())

    profesor.permissions = [
        perms["users:read"],
        perms["users:update"],
        perms["dashboard:read"],
        perms["students:read"],
        perms["projects:read"],
        perms["projects:create"],
        perms["projects:update"],
        perms["tasks:read"],
        perms["tasks:create"],
        perms["tasks:update"],
        perms["activities:read"],
        perms["activities:create"],
        perms["activity_feed:read"],
    ]

    estudiante.permissions = [
        perms["dashboard:read"],
        perms["students:read"],
        perms["projects:read"],
        perms["tasks:read"],
        perms["activities:read"],
        perms["activities:create"],
        perms["activities:update"],
        perms["activity_feed:read"],
    ]

    uah_user.permissions = [
        perms["dashboard:read"],
        perms["students:read"],
        perms["projects:read"],
        perms["tasks:read"],
        perms["activities:read"],
        perms["activities:create"],
        perms["activities:update"],
        perms["activity_feed:read"],
    ]

    db.commit()

    return {
        "admin": admin,
        "profesor": profesor,
        "estudiante": estudiante,
        "uah_user": uah_user,
    }, perms
