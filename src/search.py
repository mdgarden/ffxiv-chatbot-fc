import re
import json

DB_PATH = "src/assets/data/merged_db.json"

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


def open_db_json():
    with open(DB_PATH, "r") as f:
        parsed_json = json.load(f)
    return parsed_json


def search_db():
    pass
