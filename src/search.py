import re
import json


TARTO_URL = "https://ff14.tar.to/item/list?keyword="
FFXIV_LS_DB = "/lodestone/playguide/db/search/?q="
FFXIV_JP_URL = "https://jp.finalfantasyxiv.com"
FFXIV_NA_URL = "https://na.finalfantasyxiv.com"

# compile의 리턴값은 문자열이 아닌 클래스 참고 : https://nachwon.github.io/regular-expressions/
extract_hangul = re.compile("[\u3131-\u3163\uac00-\ud7a3]+")  # 한글만 추출하는 정규식
extract_hiragana = re.compile("[ぁ-んァ-ン 一-龥]+")  # 히라가나, 가타카나, 한자 추출
extract_meta = re.compile("[-=.#/?:$}]+")  # 특수문자

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

    response = {
        id: "",
        "origin_locale": "",
        "kr": "",
        "jp": "",
        "en": "",
    }

    # 리스폰스 초기화
    def __init__(self, keyword):
        self.keyword = keyword

    def set_locale(self):
        # check language
        if self.keyword.extract_hangul:
            self.locale = "kr"
            self.item_list = self.ko_item_data
        elif self.keyword.extract_hiragana:
            self.locale = "ja"
            self.item_list = self.item_data
        elif self.keyword.extract_meta:
            self.loacle = "meta"
        else:
            self.locale = "en"
            self.item_list = self.item_data

    def switch_locale(self):
        if self.locale == "ja":
            self.locale = "en"
        elif self.locale == "en":
            self.locale = "ja"

    def switch_list(self):
        if self.item_list == self.item_data:
            self.item_list = self.ko_item_data

    def search_perfect_match(self):
        if self.loacle == "ja" or "en":
            for item in self.item_list:
                if item[0][self.locale] == self.keyword:
                    self.save_global_data(item)
                    return
                elif self.keyword in item[0][self.locale]:
                    self.save_global_data(item)

        else:
            for item in self.item_list:
                if item[0][self.locale] == self.keyword:
                    self.save_kr_data(item)

    def save_global_data(self, item):
        self.response["id"] == item[0]
        self.response[self.locale] == self.keyword
        self.switch_locale()
        self.response[self.locale] == self.keyword
        self.switch_list()
        self.response["kr"] == self.search_item_by_id()

    def save_kr_data(self, item):
        self.response["id"] == item[0]
        self.response[self.locale] == self.keyword
        self.switch_list()
        self.locale = "ja"
        self.response["ja"] == self.search_item_by_id()
        self.locale = "en"
        self.response["en"] == self.search_item_by_id()

    def search_item_by_id(self):
        self.item_list[self.response["id"] - 1]
        pass

    def extract_db(self):
        self.set_locale()
        # 완전일치, 부분일치 넣기
        # 한국어가 아니라면 전체 아이템 검색
        if self.locale == "meta":
            return
        else:
            # 완전일치
            self.search_perfect_match()


# f = Search(keyword)
# f.extract_db()
