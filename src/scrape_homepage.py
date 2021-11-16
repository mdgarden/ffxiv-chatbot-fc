import requests
from bs4 import BeautifulSoup
from linebot.models import (
    CarouselColumn,
    CarouselTemplate,
    TemplateSendMessage,
    template,
)

# from fake_useragent import UserAgent

# ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}
# ua = UserAgent()
# header = {'user-agent':ua.chrome}
FFXIV_JP_URL = "https://jp.finalfantasyxiv.com"
FFXIV_NA_URL = "https://na.finalfantasyxiv.com"
FFXIV_KR_URL = "https://www.ff14.co.kr"
LODESTONE = "/lodestone"
CHARACTER = "/character"
NOTICE = "/news/notice?category=2"
FFXIV_JP_DB_URL = "https://jp.finalfantasyxiv.com/lodestone/playguide/db/search/?q="
default_img = (
    "https://pbs.twimg.com/card_img/1458489866896154624/jBwpzaqT?format=png&name=small"
)


def get_soup(url):
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")
    return soup


def extract_topic_post():
    topics = []

    topic_list = get_soup(FFXIV_JP_URL + LODESTONE).find_all(
        "li", {"class": "news__list--topics"}
    )

    for li in topic_list:
        try:
            topic_title = li.find("p", {"class": "news__list--title"}).get_text()
            topic_url = li.find("a", {"class": "news__list--img"})["href"]
            topic_url_jp = FFXIV_JP_URL + topic_url
            topic_url_en = FFXIV_NA_URL + topic_url
            topic_text = li.find("p", {"class": "mdl-text__xs-m16"}).get_text()
            banner_url = li.find("img")["src"]
            topic = {
                "title": topic_title,
                "jp_url": topic_url_jp,
                "en_url": topic_url_en,
                "img_url": banner_url,
                "text": topic_text,
            }
            topics.append(topic)
        except Exception as ex:
            print(ex)
    message = generate_carousel(topics)
    return message


def generate_carousel(column):
    """
    column = {"img_link": "", "title": "", "text": "", "url": ""}
    """

    columns = []
    for i in range(3):
        title = column[i]["title"][:39]
        text = column[i]["text"][:55]
        columns.append(
            CarouselColumn(
                thumbnail_image_url=str(column[i]["img_url"]),
                title=str(title),
                text=str(text),
                actions=[
                    {
                        "type": "uri",
                        "label": "日本語",
                        "uri": column[i]["jp_url"],
                    },
                    {
                        "type": "uri",
                        "label": "English",
                        "uri": column[i]["en_url"],
                    },
                ],
            )
        )

    return TemplateSendMessage(
        alt_text="template",
        template=CarouselTemplate(columns=columns, image_size="contain"),
    )


def extract_maintenance_post_jp():
    maintenance_url_list = []
    num = 0
    message = "◆ 글섭 최신 점검 공지\n\n"

    notice_list = (
        get_soup(FFXIV_JP_URL + LODESTONE)
        .find("div", {"class": "toptabchanger_newsbox"})
        .find("ul")
        .find_all("li", {"class": "news__list"})
    )

    for li in notice_list:
        try:
            maintenance_url = li.find(
                "a", {"class": "news__list--link ic__maintenance--list"}
            ).attrs["href"]
            if (
                maintenance_url is not None
                and maintenance_url not in maintenance_url_list
            ):
                maintenance_url_list.append(maintenance_url)
        except Exception as ex:
            print(ex)

    if len(maintenance_url_list) >= 1:
        for link in maintenance_url_list:
            num += 1
            m = get_soup(FFXIV_JP_URL + link)
            m_title = (
                m.find("header", {"class": "news__header"}).find("h1").text.lstrip()
            )
            maintenance_contents = m.find(
                "div", {"class": "news__detail__wrapper"}
            ).get_text()
            maintenance_time = maintenance_contents.find("日　時")
            message = generate_carousel(
                default_img,
                m_title,
                maintenance_contents[maintenance_time:],
                FFXIV_JP_URL + link,
            )

    else:
        message = "글섭의 최신 점검관련 공지가 없습니다."

    return message


def extract_maintenance_post_kr():
    pass


def scrape_maintenances():
    pass


def extract_character_profile(info):

    character_url = FFXIV_JP_URL + LODESTONE + CHARACTER + "/" + info["profile"]
    contents = get_soup(character_url)

    character_name = contents.find("p", {"class": "frame__chara__name"}).get_text()
    try:
        character_title = contents.find(
            "p", {"class": "frame__chara__title"}
        ).get_text()
    except Exception as ex:
        print(ex)
        character_title = ""

    character_job = contents.find("div", {"class": "character__class__data"}).get_text()
    character_information = (
        character_title
        + "\n"
        + character_name
        + "\n"
        + character_job
        + "\n\n"
        + character_url
    )
    return character_information


def search_db(keyword):
    get_soup(FFXIV_JP_DB_URL + keyword)


# carousel 템플릿 작성 예시
# @handler.add(MessageEvent, message=TextMessage)
# def response_message(event):
#     # notesのCarouselColumnの各値は、変更してもらって結構です。
#     notes = [CarouselColumn(thumbnail_image_url="https://renttle.jp/static/img/renttle02.jpg",
#                             title="【ReleaseNote】トークルームを実装しました。",
#                             text="creation(創作中・考え中の何かしらのモノ・コト)に関して、意見を聞けるようにトークルーム機能を追加しました。",
#                             actions=[{"type": "message","label": "サイトURL","text": "https://renttle.jp/notes/kota/7"}]),

#              CarouselColumn(thumbnail_image_url="https://renttle.jp/static/img/renttle03.jpg",
#                             title="ReleaseNote】創作中の活動を報告する機能を追加しました。",
#                             text="創作中や考え中の時点の活動を共有できる機能を追加しました。",
#                             actions=[
#                                 {"type": "message", "label": "サイトURL", "text": "https://renttle.jp/notes/kota/6"}]),

#              CarouselColumn(thumbnail_image_url="https://renttle.jp/static/img/renttle04.jpg",
#                             title="【ReleaseNote】タグ機能を追加しました。",
#                             text="「イベントを作成」「記事を投稿」「本を登録」にタグ機能を追加しました。",
#                             actions=[
#                                 {"type": "message", "label": "サイトURL", "text": "https://renttle.jp/notes/kota/5"}])]

#     messages = TemplateSendMessage(
#         alt_text='template',
#         template=CarouselTemplate(columns=notes),
#     )

#     line_bot_api.reply_message(event.reply_token, messages=messages)
