```sql

USUARIO(
    id_usuario PK,
    nombre,
    correo,
    fecha_registro
)

ARTISTA(
    id_artista PK,
    nombre_artistico,
    biografia
)

ALBUM(
    id_album PK,
    titulo,
    fecha_lanzamiento
)

ALBUM_ARTISTA(
    id_album PK, FK  ALBUM.id_album,
    id_artista PK, FK  ARTISTA.id_artista
)

CANCION(
    id_cancion PK,
    titulo,
    duracion,
    ruta_archivo,
    formato,
    id_album FK  ALBUM.id_album NULL,
)

ARTISTA_CANCION(
    id_artista PK, FK  ARTISTA.id_artista,
    id_cancion PK, FK  CANCION.id_cancion,
    rol
)

GENERO(
    id_genero PK,
    nombre,
    descripcion
)

CANCION_GENERO(
    id_cancion PK, FK  CANCION.id_cancion,
    id_genero PK, FK GENERO.id_genero
	)```