from app.db.session import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.identity import Identity
from app.models.user_role import UserRole

db = SessionLocal()

try:
    # 1️⃣ Crear roles
    admin_role = Role(nombre="administrador", descripcion="Acceso total")
    participant_role = Role(nombre="participante", descripcion="Acceso limitado")

    db.add_all([admin_role, participant_role])
    db.commit()

    # 2️⃣ Crear usuario
    user = User(nombre="Laura García")
    db.add(user)
    db.commit()
    db.refresh(user)

    # 3️⃣ Asignar rol global (N:M)
    user.roles.append(participant_role)
    db.commit()

    # 4️⃣ Crear identidad con rol contextual
    identity = Identity(
        email="laura_admin",
        provider="local",
        password_hash="fakehash",
        user_id=user.id_usuario,
        rol_id=admin_role.id_rol
    )

    db.add(identity)
    db.commit()

    # 5️⃣ Recuperar y mostrar relaciones
    user_db = db.query(User).filter_by(nombre="Laura García").first()

    print("\nUsuario:", user_db.nombre)
    print("Roles globales:", [r.nombre for r in user_db.roles])

    for ident in user_db.identidades:
        print("Identidad:", ident.email, "Rol contextual:", ident.rol.nombre if ident.rol else None)

finally:
    db.close()
