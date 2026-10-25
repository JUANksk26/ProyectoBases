import psycopg2
<<<<<<< HEAD
DB_config = {
    'host': 'localhost', # Espero que sea la funcion definitiva para conectarse a la base desde el reproductor, en este archivo ya se pueden hacer las consultas y las funciones para agregar y eliminar registros
    'database': 'postgres',
    'user': 'postgres',
    'password': 'k3){"3SFQ7/n', 
    'port': 5432
}
def get_connection():
    try:
        connection = psycopg2.connect(**DB_config)
        return connection
    except Exception as e:
        print(f"No se pudo conectar a la base de datos: {e}")
        return None
=======
from psycopg2 import OperationalError

#se crea una nueva instancia de conexion
try:
    conn = psycopg2.connect( #creacion de la variable de CONNections
        database = "letit",
        user = "postgres",
        host = "localhost",
        password = 'postgres',
        port = 5432
    )
    print("Conexion exitosa")
except OperationalError as e:
    print(f"No se pudo conectar a la base de datos, error: {e}")
>>>>>>> c83fbe866551e4f209e2da3a8ea6317b99a64eef

# Podemos dejar el nombre por defecto de la base de datos en 'postgres'. O cambiarlo por el del proyecto en cuyo caso necesitaríamos cambiar esta funcion y crear una que defina una nueva base de datos.
# Por facilidad, prefiriblemente solo leeremos las canciones guardadas en una carpeta seleccionada, sin tener que descubir como funciona la appi
# Dejare un documento sobre como instalar el servidor de PostgreSQL para que pueda iniciar con lo suyo.
    