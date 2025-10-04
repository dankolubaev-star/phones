from f6ops.phone_entry import PhoneEntry
from f6ops.search_ddg import search_pages_by_phone
from f6ops.db_sqlite import init, upsert_phone, add_pages, all_phones

INPUT_FILE = "phones.txt"

def process_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            raw = line.strip()
            if not raw:
                continue

            pe = PhoneEntry(raw)

            upsert_phone(pe.e164, pe.operator)

            urls = search_pages_by_phone(pe.e164, max_results=5)

            uniq = []
            for u in urls:
                if u not in uniq:
                    uniq.append(u)

            if uniq:
                add_pages(pe.e164, uniq)

            print(pe.raw, "->", pe.e164, "->", pe.operator, "(страниц:", len(uniq), ")")
            for u in uniq:
                print("Исходный номер:", pe.raw)
                print("В формате E.164:", pe.e164)
                print("Оператор:", pe.operator)
                print("Количество страниц:", len(uniq))

    for u in uniq:
        print("Страница:", u)

if __name__ == "__main__":
    init()
    process_file(INPUT_FILE)
    print("Всего в БД:", len(all_phones()))