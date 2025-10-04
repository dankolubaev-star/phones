from phoneops.db_sqlite import init, DB_PATH

if __name__ == "__main__":
    init()
    print(f"✅ SQLite база создана: {DB_PATH}  ini - init_db.py:5")