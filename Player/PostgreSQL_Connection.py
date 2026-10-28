import psycopg2 # libreria para conectarse y usar PostgreSQL
import yt_dlp # libreria para bajar la musica con URL
import os # libreria que permite sacar el nombre del SO usado
from psycopg2 import OperationalError

# se crea una nueva instancia de conexion
try:
    conn = psycopg2.connect( # creacion de la variable de CONNections
        database = "postgres", # Nombre provisional para base de datos.
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

    # esto se saco de https://pypi.org/project/yt-dlp/#user-content-embedding-examples
    if os.name == 'posix': # los sistemas Unix (Linux/MacOS) devuelven esta cadena como nombre representativo
        ydl_opts = {
            "format": "mp3/bestaudio/best", # se descargan archivos mp3 de la mejor calidad posible. Prioriza compatibilidad sobre calidad
            "postprocessors": [{            # tecnicamente esto el usuario podria modificarlo a voluntad en versiones futuras del proyecto
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }],
            "paths": {
                "home": "~/Downloads", # por ahora es una ruta fija
                "temp": "/tmp/yt-dlp",
            },
        }
    else: # confuracion para sistemas windows
        ydl_opts = {
            "format": "mp3/bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }],
            "paths": {
                # poner direccion de windows. "home": "~/Downloads", cambiar la parte derecha
                # poner direccion correspondiente a windows"temp": "/tmp/yt-dlp", cambiar la parte derecha
            },
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # crea un objeto de la clase YoutubeDL con las configuraciones (ydl_opts) y se lo asigna a 'ydl'
        error_code = ydl.download(URL) # la variable error_code es basicamente informativa para manejo de errores
                                       # recordar que el codigo se ejecuta de derecha a izquierda, asi que primero se realiza la descarga en el equipo
                                       # con la llamada del metodo .download inherente de los objetos YoutubeDL y luego se guarda su codigo 
                                       # de resultado (0 si no hubo errores).
        informacion = ydl.extract_info(URL, download=True) # este metodo se encuentra dentro de la libreria yt_dlp, linea 1673 de yt_dlp/YoutubeLD.py. 
                                                |          # la forma del diccionario y su informacion depende del extractor del sitio usado, no de la libreria particularmente.
                                                           # algunas claves comunes son: id, title, url, duration, formats.
                                                           # download = true quiere decir que ya esta descargada la URL.
                                                           # habria que controlar las maneras cada extractor en funcion de la pagina.
                                                           # podemos tambien centrarnos en revisar solo el extractor de youtube
    insertarMusica(informacion) # se actualiza la base de datos con la nueva cancion

def insertarMusica(info): #aqui se actualiza la base de datos
    nombre = info["title"]
    duracion = info["duration"]

    # la tabla canciones en la base de datos tiene los campos: 
    # id_cancion (PK), titulo (NOT NULL), duracion_segundos(NOT NULL)
    # ruta_archivo(NOT NULL), formato (NOT NULL), id_album, numero_pista
    
    cur = conn.cursor()
    
    #hay que mirar si se puede volver variable la direccion de descarga, con eso se vuelve innecesario el if/else
    if os.name == 'posix'{
        cur.execute("""INSERT INTO cancion 
                    (titulo, duracion_segundos, ruta_archivo, formato)
                    VALUES (%s, %s, '~/Downloads', 'mp3')""", (nombre, duracion)) # por ahora dejar el formato de descarga estatico
        print("se guardo en la base de datos")
        conn.commit()
    }else{
        cur.execute("""INSERT INTO cancion 
                    (titulo, duracion_segundos, ruta_archivo, formato)
                    VALUES (%s, %s, 'Descargas', 'mp3')""", (nombre, duracion)) 
        print("se guardo en la base de datos")
        conn.commit()
    }
    cur.close()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
print("Que quiere hacer: \n1. descargar musica \n2. salir")
deseo = input()

if int(deseo) == 1:
    url = input("URL de la cancion: ")
    descargarMusica(url)
elif int(deseo) == 2:
    print("adios!")

conn.close()
    #metodo para guardar canciones que fallaron al descargar (como un control de fallas) y tenerlas documentadas
    
