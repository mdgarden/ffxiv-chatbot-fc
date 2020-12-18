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
    return soup


# 타르토맛에서 검색 : 검색결과가 없을 시 아직 한섭 업뎃 템이 아님
# 타르토맛에서 검색결과 없을시 ff14 공식 DB에서 검색
# 둘 다 없을 시 아이템 이름 재확인 요청
# 타르토맛에 결과가 있으면 한/일/영문 템이름 표시하고 해당 템 링크 전송


def search_tarto(keyword):
    item_html = get_soup(TARTO_URL + TARTO_SEARCH + keyword)
    item_info = item_html.find_all("script")[-5].get_text()
    # except:
    #     message = "아직 한국 서버에 업데이트 되지 않은 항목입니다."

    item_id = item_info[item_info.find('[{"id":') + 7 : item_info.find(',"icon"')]
    item_link = TARTO_URL + TARTO_VIEW + item_id
    item_contents = get_soup(item_link).find("div", {"id": "item-section"})
    item_name_lang = item_contents.find("div", {"id": "item-name-lang"}).get_text()
    item_name_kr = item_contents.find("div", {"id": "item-name"}).get_text()
    message = keyword + "검색결과 : " + item_name_kr + item_name_lang + "\n\n" + item_link
    return message


def search_ffxiv_db():
    pass


def search_keyword():
    pass
