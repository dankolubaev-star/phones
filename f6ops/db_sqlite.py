from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent.parent / "phones.db"

def open_db():
    return sqlite3.connect(DB_PATH)

def init():
    con = open_db()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phone(
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        e164      TEXT UNIQUE NOT NULL,
        operator  TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_phone_e164 ON phone(e164);")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phone_page(
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_id  INTEGER NOT NULL REFERENCES phone(id) ON DELETE CASCADE,
        url       TEXT NOT NULL,
        title     TEXT,
        snippet   TEXT,
        status_code INTEGER,
        fetched_at DATETIME,
        found_at  DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_phone_page_phone_id ON phone_page(phone_id);")
    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS ux_phone_page_url ON phone_page(phone_id, url);")

    con.commit()
    con.close()

def upsert_phone(e164: str, operator: str):
    con = open_db()
    cur = con.cursor()

    cur.execute("SELECT id, operator FROM phone WHERE e164 = ?", (e164,))
    row = cur.fetchone()
    if row is None:
        cur.execute("INSERT INTO phone(e164, operator) VALUES(?, ?)", (e164, operator))
    else:
        pid, op = row
        if op != operator:
            cur.execute("UPDATE phone SET operator = ? WHERE id = ?", (operator, pid))

    con.commit()
    con.close()

def _get_phone_id(cur, e164: str) -> int:
    cur.execute("SELECT id FROM phone WHERE e164 = ?", (e164,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO phone(e164, operator) VALUES(?, ?)", (e164, None))
    return cur.lastrowid

def add_pages(e164: str, urls: list[str]):
    if not urls:
        return
    con = open_db()
    cur = con.cursor()

    pid = _get_phone_id(cur, e164)
    for u in urls:
        if not u:
            continue
        try:
            cur.execute(
                "INSERT OR IGNORE INTO phone_page(phone_id, url) VALUES(?, ?)",
                (pid, u)
            )
        except sqlite3.Error:
            pass

    con.commit()
    con.close()

def set_page_meta(e164: str, url: str, title: str | None = None,
                  snippet: str | None = None, status_code: int | None = None):
    con = open_db()
    cur = con.cursor()

    pid = _get_phone_id(cur, e164)
    cur.execute("SELECT id FROM phone_page WHERE phone_id = ? AND url = ?", (pid, url))
    row = cur.fetchone()
    if row is None:
        cur.execute("INSERT OR IGNORE INTO phone_page(phone_id, url) VALUES(?, ?)", (pid, url))

    cur.execute("""
        UPDATE phone_page
           SET title = COALESCE(?, title),
               snippet = COALESCE(?, snippet),
               status_code = COALESCE(?, status_code),
               fetched_at = CASE
                              WHEN ? IS NOT NULL THEN CURRENT_TIMESTAMP
                              ELSE fetched_at
                            END
         WHERE phone_id = ? AND url = ?
    """, (title, snippet, status_code, status_code, pid, url))

    con.commit()
    con.close()

def all_phones() -> list[tuple]:
    con = open_db()
    cur = con.cursor()
    cur.execute("SELECT id, e164, operator, created_at FROM phone ORDER BY id DESC")
    rows = cur.fetchall()
    con.close()
    return rows