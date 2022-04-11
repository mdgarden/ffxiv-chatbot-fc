import requests
from bs4 import BeautifulSoup
import urllib3

from src import template
from linebot.models import TextSendMessage

# import template
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

# ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}
# ua = UserAgent()
# header = {'user-agent':ua.chrome}
FFXIV_JP_URL = "https://jp.finalfantasyxiv.com"
FFXIV_NA_URL = "https://na.finalfantasyxiv.com"
LODESTONE = "/lodestone"

FFXIV_KR_URL = "https://www.ff14.co.kr"
KR_MAINTENANCE = "/news/notice?category=2"

jp_default_img = "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fbr4C0P%2FbtrlFLbcpd0%2FWji1bxqhhWiP0H1Hfgkya1%2Fimg.png"
kr_default_img = "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbjWmcb%2FbtrlFKch2Cz%2FoTZx8aGZPI57Pe7FKf1iUk%2Fimg.jpg"


def get_soup(url):
    request = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(request.text, "html.parser", from_encoding="utf-8")
    return soup


def extract_topic_post_jp():
    topics = []

    topic_list = get_soup(FFXIV_JP_URL + LODESTONE).find_all(
        "li", {"class": "news__list--topics"}
    )

    for li in topic_list:
        try:
            topic_title = li.find("p", {"class": "news__list--title"}).get_text()
            topic_time = li.find("time", {"class": "news__list--time"}).get_text()
            topic_url = li.find("a", {"class": "news__list--img"})["href"]
            topic_url_jp = FFXIV_JP_URL + topic_url
            topic_text = li.find("p", {"class": "mdl-text__xs-m16"}).get_text()
            banner_url = li.find("img")["src"]
            topic = {
                "title": topic_title,
                "url": topic_url_jp,
                "img_url": banner_url,
                "text": topic_text,
                "date": topic_time,
            }
            topics.append(topic)
        except Exception as ex:
            print(ex)
    message = template.generate_carousels(topics)
    return message


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
            post_date = m.find("time", {"class": "news__ic--maintenance"}).get_text(
                strip=True
            )

            item = {
                "title": m_title,
                "url": FFXIV_JP_URL + link,
                "img_url": jp_default_img,
                "text": maintenance_contents[maintenance_time:],
                "date": post_date,
            }
            lists.append(item)
        message = template.generate_carousels(lists)
    else:
        message = TextSendMessage(text="글섭의 최신 점검관련 공지가 없습니다.")

    return message


def extract_maintenance_post_kr():
    lists = []
    category_soup = get_soup(FFXIV_KR_URL + KR_MAINTENANCE).find_all(
        "span", {"class": "title"}
    )

    for post in category_soup:
        post_title = post.get_text(strip=True)
        post_link = FFXIV_KR_URL + post.find("a")["href"]
        article = get_soup(post_link)
        post_text = (
            article.find("div", {"class": "board_view_box"}).get_text(strip=True)
        )[30:]
        post_date = article.find("span", {"class": "date"}).get_text(strip=True)

        post = {
            "title": post_title,
            "url": post_link,
            "img_url": kr_default_img,
            "text": post_text,
            "date": post_date,
        }
        lists.append(post)

    message = template.generate_carousels(lists)
    if len(lists) == 0:
        message = "현재 점검 관련 게시글을 불러올 수 없거나, 해당 내용이 없습니다."
        return message
    return message


def extract_topic_kr():
    lists = []
    soup = get_soup(FFXIV_KR_URL).find_all("div", {"class": "mbanner_box"})

    for post in soup:
        post_title = (
            post.find("div", {"class": "title_box"}).find("h1").get_text(strip=True)
        )
        post_date = (
            post.find("div", {"class": "title_box"}).find("h2").get_text(strip=True)
        )
        post_link = post.find("a")["href"].split(",")
        post_text = (
            post.find("div", {"class": "title_box"}).find("p").get_text(strip=True)
        )
        try:
            post_img = (
                "https:"
                + post.select_one("div.mbanner_char")["style"]
                .split("url(")[1]
                .split(")")[0]
            )
        except Exception as ex:
            print(ex)
            post_img = kr_default_img

        # TODO : 아이콘이 없는 경우 배너 이미지 추출, 배너 이미지도 없는 경우 기본 사진으로 대체
        # try:
        #     post_banner = (
        #         "https:"
        #         + post.select_one("div.mbanner_box")["style"]
        #         .split("url(")[1]
        #         .split(")")[0]
        #     )
        # except Exception as ex:
        #     print(ex)
        #     post_img = kr_default_img

        post = {
            "title": post_title,
            # "url": FFXIV_KR_URL + post_link[0][20:-1],
            "url": FFXIV_KR_URL + post_link[0][20:-1]
            if "https://" not in str(post_link)
            else post_link[0][20:-1],
            "img_url": post_img,
            "text": post_text,
            "date": post_date,
        }
        lists.append(post)

    message = template.generate_carousels(lists)
    return message


# message = extract_topic_kr()
# print(message)
