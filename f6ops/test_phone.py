from f6ops.phone_entry import PhoneEntry
from f6ops.search_ddg import search_pages_by_phone

raw = "8 (905) 111-22-33"
pe = PhoneEntry(raw)

print("Исходный номер:", pe.raw)
print("Нормализованный:", pe.e164)
print("Оператор:", pe.operator)

print("Поиск в DuckDuckGo")
urls = search_pages_by_phone(pe.e164, max_results=3)
if urls:
    print("Найдены страницы:")
    for u in urls:
        print("-", u)
else:
    print("Ничего не найдено")
