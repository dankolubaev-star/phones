import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

TIMEOUT = 10


def extract_real_url(href: str) -> str:
    if not href:
        return ""

    if "uddg=" in href:
        try:
            return unquote(href.split("uddg=")[-1])
        except:
            return href

    return href


def search_ddg(phone: str, max_results: int = 5):
    query = f'"{phone}"'
    base_url = "https://duckduckgo.com/html/"
    params = {"q": query}

    print(f"\n DDG запрос: {query}")

    resp = requests.get(base_url, params=params, headers=HEADERS, timeout=TIMEOUT)
    print("Код ответа (1):", resp.status_code)

    if resp.status_code == 202:
        print("DDG вернул 202, ждем")
        time.sleep(1)
        resp = requests.get(base_url, params=params, headers=HEADERS, timeout=TIMEOUT)
        print("Код ответа (2):", resp.status_code)

    if resp.status_code != 200:
        print("Ошибка: DDG не вернул 200. Пропускаем номер.")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    links = []

    for a in soup.find_all("a"):
        href = a.get("href", "")
        real = extract_real_url(href)

        if real.startswith("http") and "duckduckgo.com" not in real:
            if real not in links: 
                links.append(real)

        if len(links) >= max_results:
            break

    print("найдено ссылок:", len(links))
    return links