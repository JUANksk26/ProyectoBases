import psycopg2 # libreria para conectarse y usar PostgreSQL
import yt_dlp # libreria para bajar la musica con URL
import os # libreria que permite sacar el nombre del SO usado
from psycopg2 import OperationalError

#se crea una nueva instancia de conexion
try:
    conn = psycopg2.connect( #creacion de la variable de CONNections
        database = "postgres", # Podemos dejar el nombre por defecto de la base de datos en 'postgres'. O cambiarlo por el del proyecto en cuyo caso necesitaríamos cambiar esta funcion y crear una que defina una nueva base de datos.
        user = "postgres",
        host = "localhost",
        password = 'k3){"3SFQ7/n',
        port = 5432
    )
    print("Conexion exitosa")
except OperationalError as e:
    print(f"No se pudo conectar a la base de datos, error: {e}")

# funcion para bajar musica de la web a partir de una url dada por el usuario
def descargarMusica(URL):
    # metodo para agregar canciones al directorio (entender como funciona lo que devuelve la api y guardarlo en el directorio deseado)
    
    artistaCancion = ""

    #esto se saco de https://pypi.org/project/yt-dlp/#user-content-embedding-examples
    if os.name == 'posix': #los sistemas Unix (Linux/MacOS) devuelven esta cadena como nombre representativo
        ydl_opts = {
            "format": "m4a/bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            }],
            "paths": {
                "home": "~/Downloads", #por ahora es una ruta fija
                "temp": "/tmp/yt-dlp",
            },
        }
    else: # el sistema de windows devuelve la cadena "nt" pero da igual en este caso
        ydl_opts = {
            "format": "m4a/bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            }],
            "paths": {
                # poner direccion de windows. "home": "~/Downloads", cambiar la parte derecha
                # poner direccion correspondiente a windows"temp": "/tmp/yt-dlp", cambiar la parte derecha
            },
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URL)
        informacion = ydl.extract_info(URL, download=True) # este metodo lo dio la ia, librerias de mierda no se entiende nada
    insertarMusica(informacion)

def insertarMusica(info): #aqui se actualiza la base de datos
    nombre = info["title"]
    duracion = info["duration"]

    cur = conn.cursor()
    cur.execute("""INSERT INTO cancion 
                    (titulo, duracion_segundos, ruta_archivo, formato)
                    VALUES (%s, %s, '~/Downloads', 'm4a')""", (nombre, duracion)) #pq mierda se concatena con tuplas
    print("se guardo en la base de datos")
    conn.commit()
    cur.close()

print("Que quiere hacer: \n1. descargar musica \n2. salir")
deseo = input()

if int(deseo) == 1:
    url = input("URL de la cancion: ")
    descargarMusica(url)
elif int(deseo) == 2:
    print("adios!")

conn.close()
    #metodo para guardar canciones que fallaron al descargar (como un control de fallas) y tenerlas documentadas
    