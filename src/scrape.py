import requests
from bs4 import BeautifulSoup
from src import template


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
    soup = BeautifulSoup(request.text, "html.parser")
    return soup


def extract_topic_post_jp():
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
                "url": topic_url_jp,
                "img_url": banner_url,
                "text": topic_text,
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

            item = {
                "title": m_title,
                "url": FFXIV_JP_URL + link,
                "img_url": jp_default_img,
                "text": maintenance_contents[maintenance_time:],
            }
            lists.append(item)
        message = template.generate_carousels(lists)
    else:
        message = "글섭의 최신 점검관련 공지가 없습니다."

    return message


def extract_maintenance_post_kr():
    category_soup = get_soup(FFXIV_KR_URL + KR_MAINTENANCE).find_all(
        "span", {"class": "title"}
    )
    for article in category_soup:
        article_title = article.get_text(strip=True)
        article_link = FFXIV_KR_URL + article.find("a")["href"]
        print(article_title)
        print(article_link)

    message = "준비중"
    return message


def extract_topic_kr():
    pass


extract_maintenance_post_kr()
