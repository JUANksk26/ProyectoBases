import psycopg2
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

# Podemos dejar el nombre por defecto de la base de datos en 'postgres'. O cambiarlo por el del proyecto en cuyo caso necesitaríamos cambiar esta funcion y crear una que defina una nueva base de datos.
# Por facilidad, prefiriblemente solo leeremos las canciones guardadas en una carpeta seleccionada, sin tener que descubir como funciona la appi
# Dejare un documento sobre como instalar el servidor de PostgreSQL para que pueda iniciar con lo suyo.
    