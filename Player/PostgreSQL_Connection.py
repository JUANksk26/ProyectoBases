import psycopg2
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

# Podemos dejar el nombre por defecto de la base de datos en 'postgres'. O cambiarlo por el del proyecto en cuyo caso necesitaríamos cambiar esta funcion y crear una que defina una nueva base de datos.
# Por facilidad, prefiriblemente solo leeremos las canciones guardadas en una carpeta seleccionada, sin tener que descubir como funciona la appi
# Dejare un documento sobre como instalar el servidor de PostgreSQL para que pueda iniciar con lo suyo.
    