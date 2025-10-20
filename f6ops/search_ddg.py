import requests
from bs4 import BeautifulSoup
import urllib.parse

def search_ddg(phone, max_results=5):
    """
    Делает поиск по номеру телефона в DuckDuckGo (через HTML-версию).
    Возвращает список ссылок, где встречается этот номер.
    """

    clean = "".join(ch for ch in phone if ch.isdigit() or ch == "+")
    if clean.startswith("8"):
        clean = "+7" + clean[1:]
    elif not clean.startswith("+"):
        clean = "+7" + clean

    url = "https://duckduckgo.com/html/"
    params = {"q": f'"{clean}"'}
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/117.0 Safari/537.36"
        )
    }

    results = []

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.find_all("a")

        for link in links:
            href = link.get("href")
            if not href:
                continue

            if "uddg=" in href:
                href = urllib.parse.unquote(href.split("uddg=")[-1])

            if href.startswith("http"):
                results.append(href)

            if len(results) >= max_results:
                break

    except Exception as e:
        print("Ошибка при поиске:", e)

    return results