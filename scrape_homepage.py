import requests
from bs4 import BeautifulSoup

# from fake_useragent import UserAgent

# ssl._create_default_https_context = ssl._create_unverified_context
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}
# ua = UserAgent()
# header = {'user-agent':ua.chrome}
FFXIV_JP_URL = "https://jp.finalfantasyxiv.com"
LODESTONE = "/lodestone"
CHARACTER = "/character"
FFXIV_KR_URL = "https://www.ff14.co.kr"
NOTICE = "/news/notice?category=2"


def get_soup(url):
    request = requests.get(url, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")
    return soup


def extract_maintenance_post_jp():
    jp_notice_block = get_soup(FFXIV_JP_URL + LODESTONE).find(
        "div", {"class": "toptabchanger_newsbox"}
    )
    notice_list = jp_notice_block.find_all("li", {"class": "news__list"})
    maintenance_url = notice_list[1].find("a").attrs["href"]
    # TODO : 멘테 태그로 찾을 수 있게 변경 / 22일 당일 공홈 html구조 확인

    maintenance_contents = (
        get_soup(FFXIV_JP_URL + maintenance_url)
        .find("div", {"class": "news__detail__wrapper"})
        .get_text()
    )
    maintenance_time = maintenance_contents.find("日　時")
    message = (
        "◆글섭 최신 점검 공지\n\n"
        + maintenance_contents[maintenance_time:]
        + "\n\n"
        + FFXIV_JP_URL
        + maintenance_url
    )
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
    except:
        pass
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
