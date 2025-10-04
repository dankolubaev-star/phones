# init_db.py
from f6ops.db_sqlite import init, DB_PATH

if __name__ == "__main__":
    init()
    print(f"✅ SQLite база готова: {DB_PATH}")