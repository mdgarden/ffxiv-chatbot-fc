from scrape_homepage import extract_maintenance_post_jp, extract_character_profile

command_list = {
    "@점검": {"category": "maintenance"},
    "@이엣타이가": {"category": "character", "name": "House Tiger", "profile": "23985452"},
    "@엣탱": {"category": "character", "name": "Alpha Sertan", "profile": "23508489"},
    "@튜플": {
        "category": "character",
        "name": "Tuple Cardinality",
        "profile": "23240790",
    },
    "@교수님": {"category": "character", "name": "Meetra Surik", "profile": "14369815"},
    "@로딩": {"category": "character", "name": "Cilia Aden", "profile": "25206858"},
    "@링크": {"category": "link"},
    "@타타루": {"category": "manual"},
}


def find_command(command):
    try:
        first_command = command_list[command]
    except:
        pass

    if first_command is not None:
        category = command_list[command]["category"]
        if category == "maintenance":
            return extract_maintenance_post_jp()
        elif category == "link":
            return send_link()
        elif category == "character":
            return extract_character_profile(first_command)
        elif category == "manual":
            return send_manual()
        else:
            pass


def send_manual():
    message = "명령어 목록이에용!\n@+캐릭터 이름 : 로드스톤 링크\n@점검 : 최신 점검 관련 공지 목록(한섭 업뎃 예정)\n!+검색어 : 해당 아이템을 검색 후 언어별 이름 출력(업뎃예정)\n@공홈 : 공홈 링크를 불러옵니다"
    return message


def send_link():
    message = "글섭 공홈 : https://jp.finalfantasyxiv.com/lodestone/ \n한섭 공홈 : https://www.ff14.co.kr/main \n지름신 강림 : https://store.jp.square-enix.com/item_list.html?sale_cd=1#SERIES=11&pointercat=SERIES"
    return message