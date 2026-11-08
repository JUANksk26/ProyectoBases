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

def descargarMusicaDefault(id_cancion, y):
    cur = conn.cursor()
    cur.execute("SELECT url FROM cancion WHERE id_cancion = %s;", (id_cancion,))
    fila = cur.fetchone()

    if fila is None:
        print(f"No se encontró ninguna canción con el ID {id_cancion}.")
        return

    url = fila[0]
    descargarMusica(url, y)

# funcion para bajar musica de la web a partir de una url dada por el usuario
def descargarMusica(URL,y):
    
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
    if y == True:
        return
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # crea un objeto de la clase YoutubeDL con las configuraciones (ydl_opts) y se lo asigna a 'ydl'
        registrarRespuesta(ydl.download(URL), ruta_descarga, ydl.extract_info(URL, download=False)["title"])#habria que registar el codigo de error tambien
        registrarMusica(ydl.extract_info(URL, download=False), ruta_descarga)# algunas claves comunes de extract_info son: id, title, url, duration, formats.

# Actualiza la base de datos con la nueva cancion
def registrarMusica(info, ubicacion):
    nombre = info["title"]
    duracion = info["duration"]
    ruta = ubicacion + '\\' + nombre + ".mp3"  # le falto el mp3, lo agrego yotas
    # la tabla canciones en la base de datos tiene los campos:
    # id_cancion (PK), titulo (NOT NULL), duracion_segundos(NOT NULL)
    # ruta_archivo(NOT NULL), formato (NOT NULL), id_album, numero_pista

    cur = conn.cursor()

    #hay que mirar si se puede volver variable la direccion de descarga, con eso se vuelve innecesario el if/else
    cur.execute("""INSERT INTO cancion
                        (titulo, duracion_segundos, ruta_archivo, formato, url)
                        VALUES (%s, %s, %s, 'mp3', %s)""", (nombre, duracion, ruta, url)) 
    print("Se guardó en la base de datos.")
    conn.commit()
#habria que agregar try, except y finally para cerrar el cursor y la conexion, pero por ahora lo dejo asi para que se vea que funciona
    cur.close()

# metodo para guardar canciones que fallaron al descargar (como un control de fallas) y tenerlas documentadas
def registrarRespuesta(codigoError, ruta, titulo):
    if codigoError == 0: #quiere decir que no hubo ningun problema, no hay necesidad de documentarlo
        return 0
    else: #si hay problemas se documenta
        cur = conn.cursor()
        cur.execute("""INSERT INTO errores
                        (codigo_error, titulo, ruta_archivo)
                        VALUES (%s, %s, %s)""", (codigoError, titulo, ruta)) # por ahora dejar el formato de descarga estatico
        print("se registro el error en la base de datos")
        conn.commit()
#lo mismo del anterior
        cur.close()

def buscar_cancion(id_cancion):
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_cancion, titulo, URL FROM cancion WHERE id_cancion = %s AND activo = TRUE;", (id_cancion,))
        return cur.fetchone()
    except psycopg2.Error as e:
        print(f"No se pudo buscar la canción: {e}")
        return None
    finally:
        if cur:
            cur.close()
    
def listar_canciones():
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_cancion, titulo, URL FROM cancion WHERE activo = TRUE;")
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
        cur.execute("SELECT ruta_archivo FROM cancion WHERE id_cancion = %s;", (id_cancion,))
        fila = cur.fetchone()

        if fila is None:
            print(f"No se encontró ninguna canción con el ID {id_cancion}.")
            return

        ruta = os.path.expanduser(fila[0])
        
        if os.path.isfile(ruta):
            os.remove(ruta)
            print("Archivo físico eliminado correctamente.")
            cur.execute("UPDATE cancion SET activo = FALSE WHERE id_cancion = %s;", (id_cancion,))
            conn.commit() 
            print("Registro desactivado en la base de datos.")
        else:
            print("No se encontró el archivo físico en la ruta especificada.")

    except psycopg2.Error as e:
        conn.rollback() 
        print(f"Error en la base de datos: {e}")
    finally:
        if cur:
            cur.close()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------




while True:

    print("\n--- MENÚ DE OPCIONES ---")
    print("1. Descargar canción")
    print("2. Eliminar canción")
    print("3. Ver lista de canciones descargables")
    print("4. Salir")

    deseo = input("Seleccione una opción: ")


    match int(deseo):
        case 1:
            url = input("URL de la cancion: ")
            descargarMusica(url, False)


        case 2:
            
            print(listar_canciones())
            id_cancion = input("Ingrese el ID de la canción a eliminar: ")
            eliminar_cancion(id_cancion)

        case 3: #en el futuro esto deberia ir en el frontend, pero por ahora lo dejo aca para probar la conexion a la base de datos y que se vea que funciona
            canciones = listar_canciones()
            if canciones:
                print("\n--- Lista de canciones descargables ---")
                for cancion in canciones:
                    print(f"ID: {cancion[0]}, Título: {cancion[1]}, URL: {cancion[2]}")
                print("\nIngrese el ID de la canción que desea descargar o '0' para regresar al menú principal.")
                id_cancion = input("ID de la canción: ")
                cancion = buscar_cancion(id_cancion)
                if cancion:
                    desear_descargar = input(f"¿Desea descargar esta canción? (s/n): {cancion[1]}  ")
                    if desear_descargar.lower() == 's':
                        descargarMusicaDefault(id_cancion, True)
                else:
                    print("Canción no encontrada.")
            else:
                print("No hay canciones disponibles para descargar.")     

        case 4:
            print("Déjela sonar")
            break

        case _:
            print("Opción no válida. Intente de nuevo.")

conn.close()