import requests
from bs4 import BeautifulSoup
from linebot.models import (
    CarouselColumn,
    CarouselTemplate,
    TemplateSendMessage,
)


# ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}
# ua = UserAgent()
# header = {'user-agent':ua.chrome}
FFXIV_JP_URL = "https://jp.finalfantasyxiv.com"
FFXIV_NA_URL = "https://na.finalfantasyxiv.com"
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
            topic_text = li.find("p", {"class": "mdl-text__xs-m16"}).get_text()
            banner_url = li.find("img")["src"]
            topic = {
                "title": topic_title,
                "jp_url": topic_url_jp,
                "img_url": banner_url,
                "text": topic_text,
            }
            topics.append(topic)
        except Exception as ex:
            print(ex)
    message = generate_carousel(topics, 3)
    return message


# TODO: 영어 주소 왜 다른지 확인, 영어주소 넣을건지 뺄건지 정하기
# TODO: 점검 공지 내용 generate_carousel에서 돌아가도록 내용 정리
# TODO: 스포방지 모드일 때 한섭 공지 extract해서 답장하는 기능 넣기
# TODO: 점검 공지가 3개 이하일 경우에는?


def generate_carousel(column, count):
    """
    column = {"img_link": "", "title": "", "text": "", "url": ""}
    """

    columns = []
    for i in range(count):
        if i == 4:
            break
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
                        "label": "전체 읽기",
                        "uri": column[i]["jp_url"],
                    },
                ],
            )
        )

    return TemplateSendMessage(
        alt_text="PC 미지원 양식입니다.",
        template=CarouselTemplate(columns=columns, image_size="contain"),
    )


def extract_maintenance_post_jp():
    maintenance_url_list = []
    lists = []

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
            m = get_soup(FFXIV_JP_URL + link)
            m_title = (
                m.find("header", {"class": "news__header"}).find("h1").text.lstrip()
            )
            maintenance_contents = m.find(
                "div", {"class": "news__detail__wrapper"}
            ).get_text()
            maintenance_time = maintenance_contents.find("日　時")

            item = {
                "title": m_title,
                "jp_url": FFXIV_JP_URL + link,
                "img_url": default_img,
                "text": maintenance_contents[maintenance_time:],
            }
            lists.append(item)
        message = generate_carousel(lists, len(lists))
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
