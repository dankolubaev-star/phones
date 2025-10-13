from f6ops.phone_entry import PhoneEntry
from f6ops.search_ddg import search_pages_by_phone
from f6ops.db_sqlite import init, upsert_phone, add_pages

init()

try:
    with open("phones.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
except Exception as e:
    print("Ошибка при открытии phones.txt:", e)
    lines = []

for raw in lines:
    raw = raw.strip()
    if not raw:
        continue  

    pe = PhoneEntry(raw)
    if not pe.e164:
        print("Неверный номер:", raw)
        continue

    upsert_phone(pe.e164, pe.operator)

    urls = search_pages_by_phone(pe.e164, max_results=5)

    if len(urls) > 0:
        add_pages(pe.e164, urls)

    print("Номер:", pe.e164, "| Оператор:", pe.operator, "| Найдено:", len(urls))

    for link in urls:
        print("-", link)
    else:
        print("Номер:", pe.e164, "| Оператор:", pe.operator, "| Не найдено:")