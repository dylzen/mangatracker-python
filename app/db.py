import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "mangatracker.db")


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS manga (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_a_url TEXT UNIQUE,
            source_b_url TEXT UNIQUE,
            titolo_italiano TEXT,
            storia TEXT,
            disegni TEXT,
            categoria TEXT,
            anno TEXT,
            volumi TEXT,
            ultimo_volume TEXT,
            ultima_data TEXT,
            prossimo_volume TEXT,
            prossima_data TEXT,
            stato_italia TEXT,
            rating TEXT,
            members TEXT,
            ranking TEXT,
            popularity TEXT,
            source_b_updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_source_a_urls():
    conn = _connect()
    rows = conn.execute("SELECT source_a_url FROM manga WHERE source_a_url IS NOT NULL").fetchall()
    conn.close()
    return [row["source_a_url"] for row in rows]


def get_source_b_urls():
    conn = _connect()
    rows = conn.execute("SELECT source_b_url FROM manga WHERE source_b_url IS NOT NULL").fetchall()
    conn.close()
    return [row["source_b_url"] for row in rows]


def update_source_a_data(source_a_url, data):
    conn = _connect()
    conn.execute("""
        UPDATE manga SET
            titolo_italiano = ?,
            storia = ?,
            disegni = ?,
            categoria = ?,
            anno = ?,
            volumi = ?,
            ultimo_volume = ?,
            ultima_data = ?,
            prossimo_volume = ?,
            prossima_data = ?,
            stato_italia = ?
        WHERE source_a_url = ?
    """, (
        data["titolo_italiano"],
        data["storia"],
        data["disegni"],
        data["categoria"],
        data["anno"],
        data["volumi"],
        data["ultimo_volume"],
        data["ultima_data"],
        data["prossimo_volume"],
        data["prossima_data"],
        data["stato_italia"],
        source_a_url,
    ))
    conn.commit()
    conn.close()


def update_source_b_data(source_b_url, data, timestamp):
    conn = _connect()
    conn.execute("""
        UPDATE manga SET
            rating = ?,
            members = ?,
            ranking = ?,
            popularity = ?,
            source_b_updated_at = ?
        WHERE source_b_url = ?
    """, (
        data["rating"],
        data["members"],
        data["ranking"],
        data["popularity"],
        timestamp,
        source_b_url,
    ))
    conn.commit()
    conn.close()


def insert_manga(source_a_url=None, source_b_url=None):
    conn = _connect()
    conn.execute(
        "INSERT OR IGNORE INTO manga (source_a_url, source_b_url) VALUES (?, ?)",
        (source_a_url, source_b_url),
    )
    conn.commit()
    conn.close()
