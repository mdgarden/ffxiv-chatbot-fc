import time
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from chromedriver_py import binary_path

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}

TARTO_URL = "https://ff14.tar.to/item"
FFXIV_JP_DB_URL = "https://jp.finalfantasyxiv.com/lodestone/playguide/db/search/?q="
FFXIV_JP_URL = "https://jp.finalfantasyxiv.com"


def get_soup(url):
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")
    return soup


def search_jp_db(keyword):
    jp_db_item_link = (
        get_soup(FFXIV_JP_DB_URL + keyword)
        .find("a", {"class": "db_popup db-table__txt--detail_link"})
        .attrs["href"]
    )
    jp_db_item_link = FFXIV_JP_URL + jp_db_item_link
    return jp_db_item_link


def search_tarto(keyword):
    chrome_options = Options()
    chrome_options.binary_location = os.getenv("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(
        executable_path=str(os.getenv("CHROMEDRIVER_PATH")),
        chrome_options=chrome_options,
    )
    browser.get(TARTO_URL + "/list")
    print(browser.session_id)
    search_bar = browser.find_element_by_class_name(
        "search-section"
    ).find_element_by_tag_name("input")
    search_bar.send_keys(keyword)
    search_bar.send_keys(Keys.ENTER)
    time.sleep(0.5)
    try:
        item_link = browser.find_element_by_css_selector(
            "div.item-name > a"
        ).get_attribute("href")
        browser.get(item_link)
    except:
        message = "검색결과가 없습니다."

    try:
        # 아이템 한국어명 취득
        item_name = browser.find_element_by_css_selector(
            "div[id^='item-name'] > span"
        ).get_attribute("innerHTML")

        # 아이템 글로벌명 취득
        item_name_lang = browser.find_elements_by_css_selector(
            "div[id^='item-name-lang'] > span"
        )
        item_name_en = item_name_lang[0].get_attribute("innerHTML")
        item_name_jp = item_name_lang[2].get_attribute("innerHTML")
        jp_link = search_jp_db(item_name_jp)
        message = f'→"{keyword}"의 검색결과 : \n\n・{item_name}\n{item_link}\n\n・{item_name_jp}\n{jp_link}\n\n・{item_name_en}'

    except:
        message = "오류가 발생했습니다."

    browser.quit()
    return message
