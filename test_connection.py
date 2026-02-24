import pymysql

# Configuración (ajusta contraseña si hace falta)
HOST = "localhost"
USER = "root"
PASSWORD = "admin"
DATABASE = "eurobot"
PORT = 3306

try:
    connection = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        port=PORT
    )

    print("✅ Conexión exitosa a MariaDB")

    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()
        print("Base de datos actual:", result[0])

    connection.close()

except Exception as e:
    print("❌ Error de conexión:")
    print(e)
