import os
import requests
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}

TARTO_URL = "https://ff14.tar.to/item/list?keyword="
FFXIV_LS_DB = "/lodestone/playguide/db/search/?q="
FFXIV_JP_URL = "https://jp.finalfantasyxiv.com"
FFXIV_NA_URL = "https://na.finalfantasyxiv.com"

extract_hangul = re.compile("[^ \u3131-\u3163\uac00-\ud7a3]+")  # 한글만 추출하는 정규식

item_search_result = {
    "kr_name": "",
    "kr_link": "",
    "jp_name": "",
    "jp_link": "",
    "en_name": "",
    "en_link": "",
    "is_spoiler": False,
}


def open_browser():
    chrome_options = Options()
    chrome_options.binary_location = os.getenv("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    # 창 안닫는 옵션
    # chrome_options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(
        executable_path=str(os.getenv("CHROMEDRIVER_PATH")),
        chrome_options=chrome_options,
    )
    return browser


def get_soup(url):
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")
    return soup


def search_jp_db(keyword):
    jp_db_item_link = (
        get_soup(FFXIV_JP_URL + FFXIV_LS_DB + keyword)
        .find("a", {"class": "db_popup db-table__txt--detail_link"})
        .attrs["href"]
    )
    jp_db_item_link = FFXIV_JP_URL + jp_db_item_link
    return jp_db_item_link


def search_na_db(keyword):
    na_db_item_link = (
        get_soup(FFXIV_NA_URL + FFXIV_LS_DB + keyword)
        .find("a", {"class": "db_popup db-table__txt--detail_link"})
        .attrs["href"]
    )
    na_db_item_link = FFXIV_NA_URL + na_db_item_link
    return na_db_item_link


def search_tarto(keyword):
    # TODO: 브라우저를 열고 닫지않고 그냥 계속 켜두는 방법
    browser = open_browser()
    browser.get(TARTO_URL + keyword)

    try:
        item_link = browser.find_element_by_css_selector(
            "div.item-name > a"
        ).get_attribute("href")
        item_search_result["kr_link"] = item_link
        browser.get(item_link)
    except:
        message = "검색결과가 없습니다."

    try:
        # 아이템 한국어명 취득
        item_search_result["kr_name"] = browser.find_element_by_css_selector(
            "div[id^='item-name'] > span"
        ).get_attribute("innerHTML")

        # 아이템 글로벌명 취득
        item_name_lang = browser.find_elements_by_css_selector(
            "div[id^='item-name-lang'] > span"
        )
        item_search_result["ja_name"] = item_name_lang[2].get_attribute("innerHTML")
        item_search_result["en_name"] = item_name_lang[0].get_attribute("innerHTML")
        item_search_result["jp_link"] = search_jp_db(item_search_result["ja_name"])
        item_search_result["en_link"] = search_na_db(item_search_result["en_name"])
        return
    except:
        message = "오류가 발생했습니다."


def result_message(items):
    message = f'→"{items}"의 검색결과 : \n\n・{item_search_result["kr_name"]}\n{item_search_result["kr_link"]}\n\n・{item_search_result["ja_name"]}\n{item_search_result["jp_link"]}\n\n・{item_search_result["en_name"]}\n・{item_search_result["en_link"]}'
    return message

    # browser.close()
    return message


# TODO: 클래스화
# 한글인지 일본어인지 구분
# 한글이면 한글 json에서, 그 외라면 전체 목록에서 검색
# 정확하게 일치하는 항목이 있으면 그 항목만 기존 방식대로 3언어로 돌려주기
# 만약 한글 일치항목이 없으면 스포일러 처리
# 여러 항목 있으면 전체 일치 항목과 상위 5건만 보여주기


class Search:

    with open("/src/assets/data/items.json", "r") as f:
        item_data = json.load(f)
    with open("/src/assets/data/ko-items.json", "r") as f:
        ko_item_data = json.load(f)

    # 검색어 초기화
    def __init__(self, keyword):
        self.keyword = keyword

    def search_items(keyword):
        # 완전일치, 부분일치 넣기
        pass
