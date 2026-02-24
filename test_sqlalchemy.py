from sqlalchemy import create_engine, text

# Ajusta tu contraseña aquí
DATABASE_URL = "mysql+pymysql://root:admin@localhost:3306/eurobot"

try:
    # Crear engine
    engine = create_engine(DATABASE_URL, echo=True)

    # Conectar
    with engine.connect() as connection:
        print("✅ Conexión exitosa con SQLAlchemy")

        result = connection.execute(text("SELECT DATABASE();"))
        db_name = result.scalar()
        print("Base de datos actual:", db_name)

except Exception as e:
    print("❌ Error con SQLAlchemy:")
    print(e)
