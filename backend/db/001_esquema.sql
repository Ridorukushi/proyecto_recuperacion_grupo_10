-- Esquema del catálogo (spec 001, data-model.md). Solo crea las tablas si faltan; nunca borra datos.

CREATE TABLE IF NOT EXISTS municipio (
    clave  text PRIMARY KEY,
    nombre text NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS sitio (
    id                      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    slug                    text NOT NULL UNIQUE CHECK (slug ~ '^[a-z0-9-]{1,120}$'),
    nombre                  text NOT NULL UNIQUE CHECK (char_length(nombre) BETWEEN 1 AND 120),
    nombre_normalizado      text NOT NULL,
    municipio_clave         text NOT NULL REFERENCES municipio (clave),
    categoria               text NOT NULL CHECK (categoria IN (
        'arqueologia', 'naturaleza', 'aventura', 'cultura', 'religioso', 'gastronomia', 'termales')),
    descripcion             text CHECK (char_length(descripcion) <= 400),
    latitud                 numeric(8, 5) NOT NULL CHECK (latitud BETWEEN 1.5 AND 3.9),
    longitud                numeric(8, 5) NOT NULL CHECK (longitud BETWEEN -76.6 AND -74.4),
    horario                 text CHECK (char_length(horario) <= 200),
    como_llegar             text CHECK (char_length(como_llegar) <= 500),
    fecha_referencia_precio date
);

CREATE TABLE IF NOT EXISTS precio (
    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sitio_id  integer NOT NULL REFERENCES sitio (id) ON DELETE CASCADE,
    concepto  text NOT NULL CHECK (char_length(concepto) BETWEEN 1 AND 80),
    valor_cop integer NOT NULL CHECK (valor_cop >= 0)
);

CREATE TABLE IF NOT EXISTS fuente (
    id       integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sitio_id integer NOT NULL REFERENCES sitio (id) ON DELETE CASCADE,
    url      text NOT NULL CHECK (url ~ '^https?://' AND char_length(url) <= 500)
);
