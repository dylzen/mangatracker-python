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
            ac_url TEXT UNIQUE,
            mal_url TEXT UNIQUE,
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
            rating_mal TEXT,
            members_mal TEXT,
            ranking_mal TEXT,
            popularity_mal TEXT,
            mal_updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_ac_urls():
    conn = _connect()
    rows = conn.execute("SELECT ac_url FROM manga WHERE ac_url IS NOT NULL").fetchall()
    conn.close()
    return [row["ac_url"] for row in rows]


def get_mal_urls():
    conn = _connect()
    rows = conn.execute("SELECT mal_url FROM manga WHERE mal_url IS NOT NULL").fetchall()
    conn.close()
    return [row["mal_url"] for row in rows]


def update_ac_data(ac_url, data):
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
        WHERE ac_url = ?
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
        ac_url,
    ))
    conn.commit()
    conn.close()


def update_mal_data(mal_url, data, timestamp):
    conn = _connect()
    conn.execute("""
        UPDATE manga SET
            rating_mal = ?,
            members_mal = ?,
            ranking_mal = ?,
            popularity_mal = ?,
            mal_updated_at = ?
        WHERE mal_url = ?
    """, (
        data["rating"],
        data["members"],
        data["ranking"],
        data["popularity"],
        timestamp,
        mal_url,
    ))
    conn.commit()
    conn.close()


def insert_manga(ac_url=None, mal_url=None):
    conn = _connect()
    conn.execute(
        "INSERT OR IGNORE INTO manga (ac_url, mal_url) VALUES (?, ?)",
        (ac_url, mal_url),
    )
    conn.commit()
    conn.close()
