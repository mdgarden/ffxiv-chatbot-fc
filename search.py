import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from chromedriver_py import binary_path


TARTO_URL = "https://ff14.tar.to/item"
# FFXIV_DB_URL = "https://jp.finalfantasyxiv.com/lodestone/playguide/db/search/?q="


def search_tarto(keyword):
    keyword = keyword[1:]
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Chrome(executable_path=binary_path, options=options)
    #     ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(), options=options
    # )

    browser.get(TARTO_URL + "/list")
    search_bar = browser.find_element_by_class_name(
        "search-section"
    ).find_element_by_tag_name("input")
    search_bar.send_keys(keyword)
    search_bar.send_keys(Keys.ENTER)
    time.sleep(1)
    item_link = browser.find_element_by_css_selector("div.item-name > a").get_attribute(
        "href"
    )
    browser.get(item_link)
    item_name = browser.find_element_by_css_selector(
        "div[id^='item-name'] > span"
    ).get_attribute("innerHTML")
    item_name_lang = browser.find_elements_by_css_selector(
        "div[id^='item-name-lang'] > span"
    )

    try:
        item_name_en = item_name_lang[0].get_attribute("innerHTML")
        item_name_jp = item_name_lang[2].get_attribute("innerHTML")
        message = (
            "KR : "
            + item_name
            + "\n"
            + "EN : "
            + item_name_en
            + "\n"
            + "JP : "
            + item_name_jp
        )
    except:
        message = "오류가 발생했습니다."

    browser.quit()
    return message


# 타르토맛에서 검색 : 검색결과가 없을 시 아직 한섭 업뎃 템이 아님
# 타르토맛에서 검색결과 없을시 ff14 공식 DB에서 검색
# 둘 다 없을 시 아이템 이름 재확인 요청
# 타르토맛에 결과가 있으면 한/일/영문 템이름 표시하고 해당 템 링크 전송
