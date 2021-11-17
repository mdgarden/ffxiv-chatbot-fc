from src import scrape_lodestone

command_list = {
    "@점검": {"category": "maintenance"},
    "@공지": {"category": "topics"},
    "@링크": {"category": "link"},
    "@타타루": {"category": "manual"},
}


def find_command(command):
    try:
        first_command = command_list[command]
    except Exception as ex:
        print(ex)

    if first_command is not None:
        category = command_list[command]["category"]
        if category == "maintenance":
            return scrape_lodestone.extract_maintenance_post_jp()
        elif category == "link":
            return send_link()
        elif category == "manual":
            return send_manual()
        elif category == "topics":
            return send_topics()
        else:
            pass


def find_command_kr(command):
    try:
        first_command = command_list[command]
    except Exception as ex:
        print(ex)

    if first_command is not None:
        category = command_list[command]["category"]
        if category == "maintenance":
            return scrape_lodestone.extract_maintenance_post_jp()
        elif category == "link":
            return send_link()
        elif category == "manual":
            return send_manual()
        elif category == "topics":
            return send_topics()
        else:
            pass


def send_topics():
    message = scrape_lodestone.extract_topic_post()
    return message


def send_manual():
    message = "명령어 목록이에용!\n@공지 : 최신 토픽 목록\n@점검 : 최신 점검 관련 공지 목록(한섭 업뎃 예정)\n!+검색어 : 해당 아이템을 검색 후 언어별 이름 출력\n@링크 : 각종 링크를 불러옵니다"
    return message


def send_link():
    message = "글섭 공홈 : https://jp.finalfantasyxiv.com/lodestone/ \n한섭 공홈 : https://www.ff14.co.kr/main \n지름신 : https://store.jp.square-enix.com/item_list.html?sale_cd=1#SERIES=11&pointercat=SERIES"
    return message
