import time
import requests
import json
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}


TARTO_URL = "https://ff14.tar.to/item"
TARTO_SEARCH = "/list/?redirect=true&quick-search-option=item&keyword="
TARTO_VIEW = "/view/"
FFXIV_DB_URL = "https://jp.finalfantasyxiv.com/lodestone/playguide/db/search/?q="


def get_soup(url):
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")
    time.sleep(0.5)
    return soup


# 타르토맛에서 검색 : 검색결과가 없을 시 아직 한섭 업뎃 템이 아님
# 타르토맛에서 검색결과 없을시 ff14 공식 DB에서 검색
# 둘 다 없을 시 아이템 이름 재확인 요청
# 타르토맛에 결과가 있으면 한/일/영문 템이름 표시하고 해당 템 링크 전송


def search_tarto(keyword):
    keyword = keyword[1:]
    item_html = get_soup(TARTO_URL + TARTO_SEARCH + keyword)
    item_info = item_html.find_all("script")[-5].get_text()
    # except:
    #     message = "아직 한국 서버에 업데이트 되지 않은 항목입니다."

    item_id = item_info[item_info.find('[{"id":') + 7 : item_info.find(',"icon"')]
    item_link = TARTO_URL + TARTO_VIEW + item_id
    try:
        item_name_lang = get_soup(item_link).find("div", {"id": "item-name-lang"}).text
        item_name_kr = get_soup(item_link).find("div", {"id": "item-name"}).text
    except:
        item_name_lang = ""
        item_name_kr = ""
    message = keyword + " 검색결과 : " + item_name_kr + item_name_lang + "\n\n" + item_link
    return message


def search_ffxiv_db():
    pass


def search_keyword():
    pass


# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.utils import ChromeType
# from chromedriver_py import binary_path


# TARTO_URL = "https://ff14.tar.to/item"
# # FFXIV_DB_URL = "https://jp.finalfantasyxiv.com/lodestone/playguide/db/search/?q="


# def search_tarto(keyword):
#     keyword = keyword[1:]
#     options = Options()
#     options.add_argument("--headless")
#     browser = webdriver.Chrome(executable_path=binary_path, options=options)
#     #     ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(), options=options
#     # )

#     browser.get(TARTO_URL + "/list")
#     search_bar = browser.find_element_by_class_name(
#         "search-section"
#     ).find_element_by_tag_name("input")
#     search_bar.send_keys(keyword)
#     search_bar.send_keys(Keys.ENTER)
#     time.sleep(1)
#     item_link = browser.find_element_by_css_selector("div.item-name > a").get_attribute(
#         "href"
#     )
#     browser.get(item_link)
#     item_name = browser.find_element_by_css_selector(
#         "div[id^='item-name'] > span"
#     ).get_attribute("innerHTML")
#     item_name_lang = browser.find_elements_by_css_selector(
#         "div[id^='item-name-lang'] > span"
#     )

#     try:
#         item_name_en = item_name_lang[0].get_attribute("innerHTML")
#         item_name_jp = item_name_lang[2].get_attribute("innerHTML")
#         message = (
#             "KR : "
#             + item_name
#             + "\n"
#             + "EN : "
#             + item_name_en
#             + "\n"
#             + "JP : "
#             + item_name_jp
#         )
#     except:
#         message = "오류가 발생했습니다."

#     browser.quit()
#     return message


# 타르토맛에서 검색 : 검색결과가 없을 시 아직 한섭 업뎃 템이 아님
# 타르토맛에서 검색결과 없을시 ff14 공식 DB에서 검색
# 둘 다 없을 시 아이템 이름 재확인 요청
# 타르토맛에 결과가 있으면 한/일/영문 템이름 표시하고 해당 템 링크 전송
