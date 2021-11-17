import requests
from bs4 import BeautifulSoup

# from linebot.models import (
#     CarouselColumn,
#     CarouselTemplate,
#     TemplateSendMessage,
# )

# ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}

FFXIV_KR_URL = "https://www.ff14.co.kr"
MAINTENANCE = "/news/notice?category=2"


def get_soup(url):
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")
    return soup


def extract_maintenance_post_kr():
    category_soup = get_soup(FFXIV_KR_URL + MAINTENANCE).find_all(
        "a", {"class": "title"}
    )
    print(category_soup)

    message = "준비중"
    return message


extract_maintenance_post_kr()
