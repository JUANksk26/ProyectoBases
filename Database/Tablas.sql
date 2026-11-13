/*
-- Habilitar la generación de UUIDs (nativo en PostgreSQL 13+)
-- CREATE EXTENSION IF NOT EXISTS "pgcrypto"; -- (Descomentar si usas una versión anterior)

CREATE TABLE Usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre_usuario VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    fecha_registro TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Artistas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(255) NOT NULL
);

CREATE TABLE Albumes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo VARCHAR(255) NOT NULL,
    artista_id UUID REFERENCES Artistas(id) ON DELETE CASCADE
);

CREATE TABLE Canciones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    youtube_id VARCHAR(50) UNIQUE NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    artista_id UUID REFERENCES Artistas(id) ON DELETE SET NULL,
    album_id UUID REFERENCES Albumes(id) ON DELETE SET NULL,
    ruta_archivo TEXT NOT NULL,
    duracion INTEGER -- Duración en segundos
);

CREATE TABLE Registro_Descargas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID REFERENCES Usuarios(id) ON DELETE CASCADE,
    cancion_id UUID REFERENCES Canciones(id) ON DELETE CASCADE,
    fecha_descarga TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Historial_Reproducciones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID REFERENCES Usuarios(id) ON DELETE CASCADE,
    cancion_id UUID REFERENCES Canciones(id) ON DELETE CASCADE,
    fecha_inicio TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    porcentaje_escuchado DECIMAL(4,3) CHECK (porcentaje_escuchado >= 0 AND porcentaje_escuchado <= 1)
);
*/
