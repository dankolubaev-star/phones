import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "phones.db"

def init():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            e164 TEXT UNIQUE,
            operator TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_page (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_id INTEGER,
            url TEXT,
            UNIQUE(phone_id, url)
        )
    """)
    con.commit()
    con.close()

def _phone_id(e164):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id FROM phone WHERE e164 = ?", (e164,))
    row = cur.fetchone()
    con.close()
    return row[0] if row else None

def upsert_phone(e164, operator):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO phone (e164, operator)
        VALUES (?, ?)
        ON CONFLICT(e164) DO UPDATE SET operator=excluded.operator
    """, (e164, operator))
    con.commit()
    con.close()

def add_pages(e164, urls):
    pid = _phone_id(e164)
    if not pid:
        return
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    for u in urls:
        cur.execute("""
            INSERT OR IGNORE INTO phone_page (phone_id, url)
            VALUES (?, ?)
        """, (pid, u))
    con.commit()
    con.close()