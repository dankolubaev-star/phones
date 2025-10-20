from f6ops.phone_number import normalize_number
from f6ops.operators import get_operator_by_def
from f6ops.search_ddg import search_ddg
from f6ops.db_sqlite import init, upsert_phone, add_pages

def def_code_from_e164(e164):
    if e164.startswith("+79") and len(e164) >= 5:
        return e164[2:5]
    return None

init()

try:
    with open("phones.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
except Exception as e:
    print("Не удалось открыть phones.txt:", e)
    lines = []

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
        for u in urls:
            print(" -", u)
    else:
        print(f"Номер: {e164} | Оператор: {operator} | Ссылок: 0")

print("Готово.")