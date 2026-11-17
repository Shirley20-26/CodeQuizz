import os
import sqlite3

_ruta = None

ESQUEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE COLLATE NOCASE,
    correo TEXT NOT NULL UNIQUE COLLATE NOCASE,
    fecha_nacimiento TEXT NOT NULL,
    hash_clave TEXT NOT NULL,
    hash_recuperacion TEXT NOT NULL,
    rol TEXT NOT NULL DEFAULT 'estudiante',
    intentos_fallidos INTEGER NOT NULL DEFAULT 0,
    bloqueado_hasta REAL NOT NULL DEFAULT 0,
    creado REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS sesion (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    token TEXT NOT NULL,
    iniciada REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS progreso (
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    fase TEXT NOT NULL,
    tema TEXT NOT NULL,
    nivel INTEGER NOT NULL,
    mejor_puntaje INTEGER NOT NULL DEFAULT 0,
    mejor_aciertos INTEGER NOT NULL DEFAULT 0,
    intentos INTEGER NOT NULL DEFAULT 0,
    superado INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (usuario_id, fase, tema, nivel)
);
"""


def iniciar(carpeta):
    """Crea la base de datos (si no existe) dentro de la carpeta de la app."""
    global _ruta
    os.makedirs(carpeta, exist_ok=True)
    _ruta = os.path.join(carpeta, "codequiz.db")
    con = _conectar()
    try:
        _revisar_version(con)
        with con:
            con.executescript(ESQUEMA)
    finally:
        con.close()


def _revisar_version(con):
    """Avisa si la base es de la Fase 2 (todavía guardaba la edad)."""
    columnas = [f["name"] for f in con.execute("PRAGMA table_info(usuarios)")]
    if columnas and "fecha_nacimiento" not in columnas:
        raise RuntimeError(
            "La base de datos es de la Fase 2. Cierra la app y borra este archivo: "
            + _ruta
        )


def ruta():
    return _ruta


def _conectar():
    con = sqlite3.connect(_ruta)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def ejecutar(sql, parametros=()):
    """INSERT / UPDATE / DELETE. Devuelve el id de la última fila creada."""
    con = _conectar()
    try:
        with con:
            return con.execute(sql, parametros).lastrowid
    finally:
        con.close()


def uno(sql, parametros=()):
    """SELECT que devuelve una sola fila (o None si no hay)."""
    con = _conectar()
    try:
        return con.execute(sql, parametros).fetchone()
    finally:
        con.close()