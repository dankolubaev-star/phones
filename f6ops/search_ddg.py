import requests
from bs4 import BeautifulSoup
import urllib.parse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36"
}

DDG_HTML = "https://duckduckgo.com/html/"

def _clean_phone(phone: str) -> str:
    """Очищает вход — оставляет только цифры и +, меняет 8 -> +7."""
    clean = "".join(ch for ch in phone if ch.isdigit() or ch == "+")
    if clean.startswith("8"):
        clean = "+7" + clean[1:]
    elif not clean.startswith("+"):
        clean = "+7" + clean
    return clean

def _extract_real_url(href: str) -> str:
    if not href:
        return ""
    if "uddg=" in href:
        try:
            real = href.split("uddg=")[-1]
            return urllib.parse.unquote(real)
        except Exception:
            return href 
    return href
def search_ddg_with_dorks(phone: str, max_results: int = 10) -> list:
    clean_phone = _clean_phone(phone)
    dorks = [
         f'"{clean_phone}"',                      
        f'"{clean_phone}" site:vk.com',
        f'"{clean_phone}" site:avito.ru',
        f'"{clean_phone}" site:ok.ru',
        f'"{clean_phone}" site:instagram.com',
        f'"{clean_phone}" intitle:контакт OR intitle:контакты',
        f'"{clean_phone}" inurl:contact OR inurl:contacts OR inurl:kontakty',
        f'"{clean_phone}" site:2gis.ru',
        f'"{clean_phone}" site:yellowpages.ru',
    ]
    results = []
    seen = set()
    for q in dorks:
        params = {"q": q, "kl": "ru-ru"}
        try:
            resp = requests.get(DDG_HTML, params=params, headers=HEADERS, timeout=10)
        except Exception as e:
            print("Ошибка", e)
            continue

        if resp.status_code != 200:
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        for a in soup.find_all("a"):
            href = a.get("href")
            if not href:
                continue

            href = _extract_real_url(href)

            if not href.startswith("http"):
                continue

            if "duckduckgo.com" in href and "uddg=" not in href:
                continue

            if href in seen:
                continue

            seen.add(href)
            results.append(href)

            if len(results) >= max_results:
                break

        if len(results) >= max_results:
            break

    return results