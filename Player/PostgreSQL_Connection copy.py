import psycopg2 # libreria para conectarse y usar PostgreSQL
import yt_dlp # libreria para bajar la musica con URL
import os # libreria que permite sacar el nombre del SO usado
from psycopg2 import OperationalError

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
# codigo sacado mayormente de https://stackoverflow.com/questions/35851281/python-finding-the-users-downloads-folder
def descargarMusica(URL):

    if os.name == 'nt':
        import ctypes
        from ctypes import windll, wintypes
        from uuid import UUID

        # ctypes GUID copied from MSDN sample code
        class GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", wintypes.DWORD),
                ("Data2", wintypes.WORD),
                ("Data3", wintypes.WORD),
                ("Data4", wintypes.BYTE * 8)
            ] 

            def __init__(self, uuidstr):
                uuid = UUID(uuidstr)
                ctypes.Structure.__init__(self)
                self.Data1, self.Data2, self.Data3, \
                    self.Data4[0], self.Data4[1], rest = uuid.fields
                for i in range(2, 8):
                    self.Data4[i] = rest>>(8-i-1)*8 & 0xff

        SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
        SHGetKnownFolderPath.argtypes = [
            ctypes.POINTER(GUID), wintypes.DWORD,
            wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
        ]

        def _get_known_folder_path(uuidstr):
            pathptr = ctypes.c_wchar_p()
            guid = GUID(uuidstr)
            if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
                raise ctypes.WinError()
            return pathptr.value

        FOLDERID_Download = '{374DE290-123F-4565-9164-39C4925E467B}'

        def get_download_folder():
            return _get_known_folder_path(FOLDERID_Download)
        
        ydl_opts = { # esto se saco de https://pypi.org/project/yt-dlp/#user-content-embedding-examples
            "format": "mp3/bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }],
            "paths": {
                "home" : get_download_folder() + "\\DejelaSonar", #no se como crear una nueva carpeta xd
                "temp" : get_download_folder()
            },
        }
    else:
        def get_download_folder():
            home = os.path.expanduser("~")
            return os.path.join(home, "Downloads")
        ydl_opts = {
            "format": "mp3/bestaudio/best", # se descargan archivos mp3 de la mejor calidad posible. Prioriza compatibilidad sobre calidad
            "postprocessors": [{            # tecnicamente esto el usuario podria modificarlo a voluntad en versiones futuras del proyecto
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }],
            "paths": {
                "home": get_download_folder(), # por ahora es una ruta fija
                "temp": "/tmp/yt-dlp",
            },
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # crea un objeto de la clase YoutubeDL con las configuraciones (ydl_opts) y se lo asigna a 'ydl'
        registrarRespuesta(ydl.download(URL)) # testiando <- el codigo original funcional es -> error_code = ydl.download(URL) 
                                        
                                       # la variable error_code es basicamente informativa para manejo de errores
                                       # recordar que el codigo se ejecuta de derecha a izquierda, asi que primero se realiza la descarga en el equipo
                                       # con la llamada del metodo .download inherente de los objetos YoutubeDL y luego se guarda su codigo 
                                       # de resultado (0 si no hubo errores).
        informacion = ydl.extract_info(URL, download=False) # este metodo se encuentra dentro de la libreria yt_dlp, linea 1673 de yt_dlp/YoutubeLD.py. 
                                                           # la forma del diccionario y su informacion depende del extractor del sitio usado, no de la libreria particularmente.
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
    if os.name == 'posix':
        cur.execute("""INSERT INTO cancion 
                    (titulo, duracion_segundos, ruta_archivo, formato)
                    VALUES (%s, %s, '~/Downloads', 'mp3')""", (nombre, duracion)) # por ahora dejar el formato de descarga estatico
        print("se guardo en la base de datos")
        conn.commit()
    else:
        cur.execute("""INSERT INTO cancion 
                    (titulo, duracion_segundos, ruta_archivo, formato)
                    VALUES (%s, %s, 'Descargas', 'mp3')""", (nombre, duracion)) 
        print("se guardo en la base de datos")
        conn.commit()
        
    cur.close()

 #metodo para guardar canciones que fallaron al descargar (como un control de fallas) y tenerlas documentadas

# se supone que esta funcion se llamaria en la linea 49 de este codigo
def registrarRespuesta(codigoError): #para documentar errorsillos, se entiende su natural importancia
    if codigoError == 0: #quiere decir que no hubo ningun problema, no hay necesidad de documentarlo
        return 0 
    else: #si hay problemas se documenta
    # llamar a la funcion externa de insertar error en la base de datos
        return 1
    
def eliminar_cancion(id_cancion):
    try:
        cur = conn.cursor()

        cur.execute("DELETE FROM cancion WHERE id_cancion = %s;", (id_cancion,))
        
       
        if cur.rowcount > 0: 
            print(f"Canción con ID {id_cancion} eliminada correctamente.")
            conn.commit()
        else:
            print(f"No se encontró ninguna canción con el ID {id_cancion}.")
            
    except psycopg2.Error as e:
        # Revertir transacción en caso de error
        conn.rollback()
        print(f"Error al eliminar la canción: {e}")
        
    finally:
        # Cerrar el cursor para liberar memoria
        if cur:
            cur.close()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
print("Que quiere hacer: \n1. descargar musica \n2. eliminar cancion \n3. salir")
deseo = input()

match int(deseo):
    case 1:
        url = input("URL de la cancion: ")
        descargarMusica(url)
    case 2:
        id_cancion = input("Ingrese el ID de la canción a eliminar: ")
        eliminar_cancion(id_cancion)
    case 3:
        print("Dejelá sonar")
   

conn.close()
