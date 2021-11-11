import re
import json
import fasttext


# Skipgram model :


DB_PATH = "src/assets/data/item_db.json"
TARTO_URL = "https://ff14.tar.to/item/list?keyword="
FFXIV_LS_DB = "/lodestone/playguide/db/search/?q="
FFXIV_JP_URL = "https://jp.finalfantasyxiv.com"
FFXIV_NA_URL = "https://na.finalfantasyxiv.com"

# compile의 리턴값은 문자열이 아닌 클래스 참고 : https://nachwon.github.io/regular-expressions/
extract_hangul = re.compile("[\u3131-\u3163\uac00-\ud7a3]+")  # 한글만 추출하는 정규식
extract_hiragana = re.compile("[ぁ-んァ-ン 一-龥]+")  # 히라가나, 가타카나, 한자 추출
# extract_meta = re.findall("[-=.#/?:$}]+") z # 특수문자

# TODO: 클래스화
# 한글인지 일본어인지 구분...할 필요가 있음?
# 한글이면 한글 json에서, 그 외라면 전체 목록에서 검색
# 정확하게 일치하는 항목이 있으면 그 항목만 기존 방식대로 3언어로 돌려주기
# 만약 한글 일치항목이 없으면 스포일러 처리
# 여러 항목 있으면 전체 일치 항목과 상위 5건만 보여주기

# labels = ja, en, ko
global result


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
    result = []
    message = ""

    # 특수기호 검출시 작동안함
    if re.findall("[=#/?$!}]+", keyword):
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
                keyword
                + "의 검색결과입니다."
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
            return message

        elif keyword in DB[item_num][locale]:
            result.append(item_result)

    if len(result) == 0:
        message = keyword + "의 검색결과가 없습니다. 검색어를 확인해주세요."
        return message

    elif len(result) < 3:
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
        return message

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
        return message
