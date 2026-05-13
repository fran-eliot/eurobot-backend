# scripts/seed_db/seed_users.py

from app.modules.users.user_model import User


def seed_users(db, roles):
    print("👥 Seeding users...")

    if db.query(User).count() > 0:
        print("⚠️ Users ya inicializados")
        return {
            "admins": db.query(User).filter(User.nombre.like("Admin%")).all(),
            "profesores": db.query(User).filter(User.nombre.like("Profesor%")).all(),
            "alumnos": db.query(User).filter(User.nombre.like("Alumno%")).all(),
            "uah_users": db.query(User).filter(User.nombre.like("%UAH%")).all(),
        }

    admins = [
        User(nombre="Admin Principal", activo=True),
        User(nombre="Admin Secundario", activo=True),
    ]

    profesores = [
        User(nombre="Profesor García", activo=True),
        User(nombre="Profesor López", activo=True),
        User(nombre="Profesor Martínez", activo=True),
    ]

    alumnos = [
        User(nombre=f"Alumno {i}", activo=True)
        for i in range(1, 21)
    ]

    uah_users = [
        User(nombre="Usuario UAH Demo", activo=True)
    ]

    all_users = admins + profesores + alumnos + uah_users

    db.add_all(all_users)
    db.flush()

    for user in admins:
        user.roles.append(roles["admin"])

    for user in profesores:
        user.roles.append(roles["profesor"])

    for user in alumnos:
        user.roles.append(roles["estudiante"])

    for user in uah_users:
        user.roles.append(roles["uah_user"])

    db.commit()

    print(f"✅ {len(all_users)} usuarios creados")

    return {
        "admins": admins,
        "profesores": profesores,
        "alumnos": alumnos,
        "uah_users": uah_users,
    }