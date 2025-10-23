from pathlib import Path
from f6ops.phone_number import normalize_number
from f6ops.operators import get_operator_by_def
from f6ops.search_ddg import search_ddg
from f6ops.db_sqlite import init, upsert_phone, add_pages


def read_lines():
    path = Path(__file__).resolve().parent / "phones.txt"
    print(f"Читаю файл: {path}")

    if not path.exists():
        print("⚠️ Файл phones.txt не найден.")
        return []

    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        print(f"✅ Найдено строк: {len(lines)}")

        for i, line in enumerate(lines, 1):
            print(f" {i}: {repr(line)}")

        return lines

    except Exception as e:
        print("Ошибка при чтении файла:", e)
        return []


def def_code_from_e164(e164: str):
    if e164.startswith("+7") and len(e164) >= 5:
        return e164[2:5]  
    return None


def main():
    init()  
    lines = read_lines()

    if not lines:
        print("⚠️ Нет номеров для обработки.")
        return

    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue

        e164 = normalize_number(raw)
        code = def_code_from_e164(e164)
        operator = get_operator_by_def(code)

        upsert_phone(e164, operator)

        urls = search_ddg(e164, max_results=5)

        if urls:
            add_pages(e164, urls)
            print(f"Номер: {e164} | Оператор: {operator} | Ссылок: {len(urls)}")
            for link in urls:
                print(" -", link)
        else:
            print(f"Номер: {e164} | Оператор: {operator} | Ссылок не найдено")

    print("Готово")


if __name__ == "__main__":
    main()