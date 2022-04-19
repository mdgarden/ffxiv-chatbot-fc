from src import scrape
from linebot.models import TextSendMessage

command_list = {
    "@점검": {"category": "maintenance"},
    "@공지": {"category": "topics"},
    "@토픽": {"category": "topics"},
    "@링크": {"category": "link"},
    "@타타루": {"category": "manual"},
    "@시간": {"category": "time"},
}

# TODO:링크 버튼 형식으로 만들기


def find_command(region, command):
    # send error if command is not correct or not found
    try:
        command_list[command]
    except Exception as e:
        print(e)
        print("command not found")
        return

    if command_list[command] is not None:
        category = command_list[command]["category"]

        if category == "maintenance" and region == "jp":
            return scrape.extract_maintenance_post_jp()
        elif category == "maintenance" and region == "kr":
            return scrape.extract_maintenance_post_kr()
        elif category == "link":
            return send_link()
        elif category == "manual":
            return send_manual()
        elif category == "topics" and region == "jp":
            return scrape.extract_topic_post_jp()
        elif category == "topics" and region == "kr":
            return scrape.extract_topic_post_kr()


def send_manual():
    message = """명령어 목록이에용!
    @공지 : 최신 토픽 목록
    @점검 : 최신 점검 관련 공지 목록(한섭 업뎃 예정)
    !+검색어 : 해당 아이템을 검색 후 언어별 이름 출력
    @링크 : 각종 링크를 불러옵니다
    """

    return TextSendMessage(text=message)


def send_link():
    message = """글섭 공홈 : https://jp.finalfantasyxiv.com/lodestone/
    한섭 공홈 : https://www.ff14.co.kr/main
    지름신 : https://store.jp.square-enix.com/item_list.html?sale_cd=1#SERIES=11&pointercat=SERIES
    """
    return TextSendMessage(text=message)
