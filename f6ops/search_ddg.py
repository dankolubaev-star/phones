from ddgs import DDGS

def search_pages_by_phone(phone: str, max_results: int = 5) -> list[str]:
    results = [] 

    try:
        with DDGS() as ddgs:
            query = f'"{phone}"'
            for r in ddgs.text(query, max_results=max_results):
                if "href" in r:
                    results.append(r["href"])
    except Exception as e:
        print("Ошибка:", e)

    return results