import requests
from bs4 import BeautifulSoup

def fetch_title(url: str) -> str:
    try:
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            print("Ошибка при загрузке:", response.status_code)
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("title")

        if title_tag:
            return title_tag.text.strip()
        else:
            return ""

    except Exception as e:
        print("Ошибка при загрузке страницы:", e)
        return ""