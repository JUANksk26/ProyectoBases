
CREATE TABLE usuario (
    id_usuario BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    correo VARCHAR(254) NOT NULL UNIQUE,
    fecha_registro TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE artista (
    id_artista BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_artistico VARCHAR(200) NOT NULL,
    biografia TEXT
);

CREATE TABLE album (
    id_album BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    fecha_lanzamiento DATE
);

CREATE TABLE album_artista (
    id_album BIGINT NOT NULL,
    id_artista BIGINT NOT NULL,

    PRIMARY KEY (id_album, id_artista),

    FOREIGN KEY (id_album)
        REFERENCES album(id_album)
        ON DELETE CASCADE,

    FOREIGN KEY (id_artista)
        REFERENCES artista(id_artista)
        ON DELETE CASCADE
);

CREATE TABLE cancion (
    id_cancion BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,

    duracion_segundos INTEGER NOT NULL
        CHECK (duracion_segundos > 0),

    ruta_archivo TEXT NOT NULL UNIQUE,
    formato VARCHAR(10) NOT NULL,

    id_album BIGINT,
    numero_pista INTEGER
        CHECK (numero_pista > 0),

    FOREIGN KEY (id_album)
        REFERENCES album(id_album)
        ON DELETE SET NULL
);

CREATE UNIQUE INDEX uq_cancion_pista_album
ON cancion (id_album, numero_pista)
WHERE id_album IS NOT NULL
  AND numero_pista IS NOT NULL;

CREATE TABLE artista_cancion (
    id_artista BIGINT NOT NULL,
    id_cancion BIGINT NOT NULL,


    PRIMARY KEY (id_artista, id_cancion),

    FOREIGN KEY (id_artista)
        REFERENCES artista(id_artista)
        ON DELETE CASCADE,

    FOREIGN KEY (id_cancion)
        REFERENCES cancion(id_cancion)
        ON DELETE CASCADE

);

CREATE TABLE genero (
    id_genero BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE TABLE cancion_genero (
    id_cancion BIGINT NOT NULL,
    id_genero BIGINT NOT NULL,

    PRIMARY KEY (id_cancion, id_genero),

    FOREIGN KEY (id_cancion)
        REFERENCES cancion(id_cancion)
        ON DELETE CASCADE,

    FOREIGN KEY (id_genero)
        REFERENCES genero(id_genero)
        ON DELETE CASCADE
);