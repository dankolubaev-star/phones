import requests
from bs4 import BeautifulSoup

def search_ddg(phone, max_results=5):
    url = "https://duckduckgo.com/html/"
    params = {"q": f'"{phone}"'}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    results = []

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code != 200:
            print("Ошибка запроса:", response.status_code)
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.find_all("a", class_="result__a")

        for link in links:
            href = link.get("href")
            if href and href.startswith("http"):
                results.append(href)
            if len(results) >= max_results:
                break

    except Exception as e:
        print("Ошибка:", e)

    return results