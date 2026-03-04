import sqlite3
from datetime import datetime

DB_PATH = "engine.db"


def conectar():
    return sqlite3.connect(DB_PATH)


def inicializar():
    conn = conectar()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS hashes (
        hash TEXT PRIMARY KEY,
        caminho TEXT,
        criado_em TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        arquivo TEXT,
        pasta TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def hash_existe(hash_val):
    conn = conectar()
    c = conn.cursor()

    c.execute("SELECT 1 FROM hashes WHERE hash=?", (hash_val,))
    existe = c.fetchone() is not None

    conn.close()
    return existe


def salvar_hash(hash_val, caminho):
    conn = conectar()
    c = conn.cursor()

    c.execute(
        "INSERT OR IGNORE INTO hashes VALUES (?, ?, ?)",
        (hash_val, caminho, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()


def registrar_evento(tipo, arquivo, pasta):
    conn = conectar()
    c = conn.cursor()

    c.execute(
        "INSERT INTO eventos (tipo, arquivo, pasta, timestamp) VALUES (?, ?, ?, ?)",
        (tipo, arquivo, pasta, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()
