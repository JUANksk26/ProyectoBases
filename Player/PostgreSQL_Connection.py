import psycopg2 # libreria para conectarse y usar PostgreSQL
import yt_dlp # libreria para bajar la musica con URL
import os # libreria que permite sacar el nombre del SO usado
from pathlib import Path # libreria para manejar archivos y directorios del sistema con python
from psycopg2 import OperationalError

# pagina tutorial de pathlib
# https://escueladeprogramacion.net/blog/como-trabajar-con-archivos-en-python-leer-escribir-y-modificar-ficheros

# HAY QUE HACER OTRA CLASE PARA ABSTRAER LAS FUNCIONES DE MANEJO DE LA BASE DE DATOS Y NO REDUNDAR EN LA ESCALADA DE METODOS

# se crea una nueva instancia de conexion
try:
    conn = psycopg2.connect( # creacion de la variable de CONNections
        database = "Reproductor", # base de datos externa en Neon
        user = "neondb_owner",
        host = "ep-withered-pine-bej5jofc-pooler.c-9.us-east-2.aws.neon.tech",
        password = 'npg_h0LUcYuEMn1K',
        port = 5432
    )
    print("Conexion exitosa")
except OperationalError as e:
    print(f"No se pudo conectar a la base de datos, error: {e}")

# funcion para bajar musica de la web a partir de una url dada por el usuario
def descargarMusica(URL):
    ruta_descarga = str(Path.home() / "dejelaSonar")
    Path(ruta_descarga).mkdir(parents=True, exist_ok=True)

    ydl_opts = { # esto se saco de https://pypi.org/project/yt-dlp/#user-content-embedding-examples
        "format": "mp3/bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
        "paths": {
            "home" : ruta_descarga,
            "temp" : ruta_descarga
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # crea un objeto de la clase YoutubeDL con las configuraciones (ydl_opts) y se lo asigna a 'ydl'
        registrarRespuesta(ydl.download(URL), ruta_descarga, ydl.extract_info(URL, download=False)["title"])
        registrarMusica(ydl.extract_info(URL, download=False), ruta_descarga)# algunas claves comunes de extract_info son: id, title, url, duration, formats.

# Actualiza la base de datos con la nueva cancion
def registrarMusica(info, ubicacion):
    nombre = info["title"]
    duracion = info["duration"]
    ruta = ubicacion + nombre
    # la tabla canciones en la base de datos tiene los campos:
    # id_cancion (PK), titulo (NOT NULL), duracion_segundos(NOT NULL)
    # ruta_archivo(NOT NULL), formato (NOT NULL), id_album, numero_pista

    cur = conn.cursor()

    #hay que mirar si se puede volver variable la direccion de descarga, con eso se vuelve innecesario el if/else
    cur.execute("""INSERT INTO cancion
                    (titulo, duracion_segundos, ruta_archivo, formato)
                    VALUES (%s, %s, %s, 'mp3')""", (nombre, duracion, ruta)) # por ahora dejar el formato de descarga estatico
    print("se guardo en la base de datos")
    conn.commit()

    cur.close()

# metodo para guardar canciones que fallaron al descargar (como un control de fallas) y tenerlas documentadas
def registrarRespuesta(codigoError, ruta, titulo):
    if codigoError == 0: #quiere decir que no hubo ningun problema, no hay necesidad de documentarlo
        return 0
    else: #si hay problemas se documenta
        cur = conn.cursor()
        cur.execute("""INSERT INTO errores
                        (codigo_error, titulo, ruta_archivo)
                        VALUES (%s, %s, %s)""", (codigoError, titulo, ruta_archivo)) # por ahora dejar el formato de descarga estatico
        print("se registro el error en la base de datos")
        conn.commit()

        cur.close()

def listar_canciones():
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_cancion, titulo FROM cancion")
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"No existen canciones: {e}")
        return []
    finally:
        if cur:
            cur.close()

def eliminar_cancion(id_cancion):
    cur = None
    try:
        cur = conn.cursor()

        # 1. Obtener la ruta guardada
        cur.execute("SELECT ruta_archivo FROM cancion WHERE id_cancion = %s;", (id_cancion,))
        fila = cur.fetchone()

        if fila is None:
            print(f"No se encontró ninguna canción con el ID {id_cancion}.")
            return

        ruta = os.path.expanduser(fila[0])


        # 3. Eliminar el archivo solo si existe y es un archivo
        if os.path.isfile(ruta):
            os.remove(ruta)

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error al eliminar la canción: {e}")

    finally:
        if cur:
            cur.close()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


deseo = input()

while True:

    print("\n--- MENÚ DE OPCIONES ---")
    print("1. Descargar canción")
    print("2. Eliminar canción")
    print("3. Salir")

    deseo = input("Seleccione una opción: ")


    match int(deseo):
        case 1:
            url = input("URL de la cancion: ")
            descargarMusica(url)


        case 2:
            print(listar_canciones())
            id_cancion = input("Ingrese el ID de la canción a eliminar: ")
            eliminar_cancion(id_cancion)

        case 3:
            print("Déjela sonar")
            break

        case _:
            print("Opción no válida. Intente de nuevo.")

conn.close()