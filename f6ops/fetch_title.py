import time
from phone_number import normalize_number
from search_ddg import search_ddg

FILE_PATH = "phones.txt"

def read_phones_from_file(path):
    phones = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            print("Всего строк:", len(lines))  
            for line in lines:
                line = line.strip()
                if line != "":
                    phones.append(line)
    except FileNotFoundError:
        print("Ошибка: файл не найден:", path)

    return phones


def process_phone(phone):
    print("\n==============================")
    print("Номер обрабатывается:", phone)

    normalized = normalize_number(phone)
    print("Номер нормализованный:", normalized)

    if normalized is None:
        print("Ошибка: номер не удалось нормализовать")
        return

    print("Делаю поиск в DuckDuckGo-")

    urls = search_ddg(normalized)

    if urls:
        print("Найденные ссылки:")
        for u in urls:
            print(" -", u)
    else:
        print("Ссылки не найдены для этого номера.")


def main():
    print("")

    phones = read_phones_from_file(FILE_PATH)

    if len(phones) == 0:
        print("Файл пустой или номеров нет.")
        return

    print("Номера для обработки:", len(phones))

    for phone in phones:
        process_phone(phone)
        time.sleep(1)  

    print("\nГотово. Все номера обработаны.")


if __name__ == "__main__":
    main()