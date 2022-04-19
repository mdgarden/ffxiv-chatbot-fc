import re
import json
import fasttext
from linebot.models import TextSendMessage

DB_PATH = "src/assets/data/items/item_db.json"
TARTO_URL = "https://ff14.tar.to/item/list?keyword="
FFXIV_LS_DB = "/lodestone/playguide/db/search/?q="
FFXIV_JP_URL = "https://jp.finalfantasyxiv.com"
FFXIV_NA_URL = "https://na.finalfantasyxiv.com"

# compile의 리턴값은 문자열이 아닌 클래스 참고 : https://nachwon.github.io/regular-expressions/
extract_hangul = re.compile("[\u3131-\u3163\uac00-\ud7a3]+")  # 한글만 추출하는 정규식
extract_hiragana = re.compile("[ぁ-んァ-ン 一-龥]+")  # 히라가나, 가타카나, 한자 추출


def classify_lang(text):
    model = fasttext.load_model("lid.176.ftz")
    locale = re.sub("__label__", "", model.predict(text)[0][0])
    return locale


def open_db_json():
    with open(DB_PATH, "r") as f:
        parsed_json = json.load(f)
    return parsed_json


def search_db(keyword):
    DB = open_db_json()
    locale = classify_lang(keyword)

    if locale != "en":
        if locale == "ko" or locale == "ja":
            pass
        else:
            locale = "en"

    result = []
    message = ""

    # 특수기호 검출시 작동안함
    if re.findall("[=#/?$!}]+", keyword) or len(keyword) == 0:
        return

    for item_num in DB:
        item_result = {
            "item_num": item_num,
            "words": {
                "ko": DB[item_num]["ko"],
                "ja": DB[item_num]["ja"],
                "en": DB[item_num]["en"],
            },
        }

        if keyword == DB[item_num][locale]:
            result.append(item_result)
            message = (
                '"'
                + keyword
                + '"의 검색결과입니다.'
                + "\n\n"
                + "Ko : "
                + result[0]["words"]["ko"]
                + "\n"
                + "Ja : "
                + result[0]["words"]["ja"]
                + "\n"
                + "En : "
                + result[0]["words"]["en"]
            )
            return TextSendMessage(text=message)

        elif keyword in DB[item_num][locale]:
            result.append(item_result)

    if len(result) == 0:
        message = keyword + "의 검색결과가 없습니다. 검색어를 확인해주세요."
        return TextSendMessage(text=message)

    elif len(result) == 1:
        message = (
            '"'
            + keyword
            + '"의 검색결과입니다.'
            + "\n\n"
            + "Ko : "
            + result[0]["words"]["ko"]
            + "\n"
            + "Ja : "
            + result[0]["words"]["ja"]
            + "\n"
            + "En : "
            + result[0]["words"]["en"]
        )
        return TextSendMessage(text=message)

    elif len(result) < 3 and len(result) > 1:
        message = (
            keyword
            + "의 검색결과입니다. \n총"
            + str(len(result))
            + "건의 결과에서 상위 목록을 표시합니다.\n\n============\n\n"
            + "Ko : "
            + result[len(result) - 1]["words"]["ko"]
            + "\n"
            + "Ja : "
            + result[len(result) - 1]["words"]["ja"]
            + "\n"
            + "En : "
            + result[len(result) - 1]["words"]["en"]
        )
        return TextSendMessage(text=message)

    else:
        message = (
            keyword
            + "의 검색결과입니다. \n총"
            + str(len(result))
            + "건의 결과에서 상위 목록을 표시합니다.\n\n============\n\n"
            + "① "
            + result[len(result) - 1]["words"][locale]
            + "\n"
            + "② "
            + result[len(result) - 2]["words"][locale]
            + "\n"
            + "③ "
            + result[len(result) - 3]["words"][locale]
        )
        return TextSendMessage(text=message)
