# conftest.py
# Este archivo se utiliza para definir fixtures de pytest que pueden ser utilizadas
# en múltiples archivos de prueba. En este caso, se define una fixture para crear
# un cliente de prueba de FastAPI que se puede usar en las pruebas para realizar
# solicitudes a la aplicación.

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.modules.identities.identity_model import Identity
from app.modules.roles.role_model import Permission, Role

# Importar modelos para registrar metadata
from app.modules.users.user_model import User

# =====================================================
# TEST DATABASE (SQLite en memoria)
# =====================================================

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


# =====================================================
# CREAR TABLAS UNA VEZ
# =====================================================

Base.metadata.create_all(bind=engine_test)


# =====================================================
# OVERRIDE get_db
# =====================================================


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# =====================================================
# FIXTURE CLIENT
# =====================================================


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


# =====================================================
# FIXTURE DB SESSION
# =====================================================


@pytest.fixture()
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================================================
# LIMPIEZA AUTOMÁTICA ENTRE TESTS
# =====================================================


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)


def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


@pytest.fixture(autouse=True)
def seed_data():
    db = TestingSessionLocal()

    # ===============================
    # PERMISOS
    # ===============================
    perms = [
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
        "dashboard:read",
    ]

    permissions = {}
    for p in perms:
        perm = Permission(nombre=p)
        db.add(perm)
        permissions[p] = perm

    db.flush()

    # ===============================
    # ROLES
    # ===============================
    admin_role = Role(nombre="admin")
    student_role = Role(nombre="student")

    admin_role.permissions = list(permissions.values())
    student_role.permissions = [permissions["dashboard:read"]]

    db.add_all([admin_role, student_role])
    db.flush()

    # ===============================
    # USERS
    # ===============================
    admin = User(nombre="Admin Principal", activo=True)
    alumno = User(nombre="Alumno UAH", activo=True)
    user_uah = User(nombre="Usuario UAH", activo=True)

    admin.roles.append(admin_role)
    alumno.roles.append(student_role)
    user_uah.roles.append(student_role)

    db.add_all([admin, alumno, user_uah])
    db.flush()

    # ===============================
    # IDENTITIES
    # ===============================
    identiy_uah = Identity(
        email="user_uah@uah.es",
        password_hash="",
        user_id=user_uah.id_usuario,
        provider="uah_saml",
    )
    db.add(identiy_uah)
    db.flush()

    db.add_all(
        [
            Identity(
                email="admin1@robotica.es",
                password_hash=hash_password("1234"),
                user_id=admin.id_usuario,
            ),
            Identity(
                email="alumno1@uah.es",
                password_hash=hash_password("1234"),
                user_id=alumno.id_usuario,
            ),
        ]
    )

    db.commit()
    db.close()
