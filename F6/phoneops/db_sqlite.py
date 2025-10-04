import sqlite3
from pathlib import Path

# путь к файлу базы
DB_PATH = Path(__file__).resolve().parent / "phones.db"

def connect():
    """Подключение к базе (или её создание)"""
    return sqlite3.connect(DB_PATH)

def init():
    """Создаём таблицы, если их ещё нет"""
    conn = connect()
    cur = conn.cursor()

    # таблица телефонов
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT UNIQUE,
        operator TEXT
    )
    """)

    # таблица страниц, где встретился номер
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_id INTEGER,
        url TEXT,
        FOREIGN KEY(phone_id) REFERENCES phones(id)
    )
    """)

    conn.commit()
    conn.close()

def add_phone(number, operator):
    """Добавляем телефон в базу"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO phones (number, operator) VALUES (?, ?)", (number, operator))
    conn.commit()
    conn.close()

def add_page(phone_number, url):
    """Добавляем страницу, где встретился номер"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM phones WHERE number = ?", (phone_number,))
    row = cur.fetchone()
    if row:
        phone_id = row[0]
        cur.execute("INSERT INTO pages (phone_id, url) VALUES (?, ?)", (phone_id, url))
        conn.commit()
    conn.close()

def get_phones():
    """Вывести все телефоны"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phones")
    rows = cur.fetchall()
    conn.close()
    return rows