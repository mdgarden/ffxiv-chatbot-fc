import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
FFXIV_JP_URL = "https://jp.finalfantasyxiv.com"
LODESTONE = "/lodestone"
FFXIV_KR_URL = "https://www.ff14.co.kr/main"

def extract_maintenance_post_jp():
    request = requests.get(FFXIV_JP_URL+LODESTONE, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")
    jp_notice = soup.find("div", {"class" : "toptabchanger_newsbox"})
    notice_list = jp_notice.find_all("li", {"class":"news__list"})
    maintenance_url = notice_list[1].find("a").attrs['href']

    maintenance_url_request = requests.get(FFXIV_JP_URL+maintenance_url, headers=headers)
    maintenance_contents = BeautifulSoup(maintenance_url_request.text, "html.parser").find("div", {"class":"news__detail__wrapper"}).get_text()
    maintenance_time = maintenance_contents.find('日　時')
    return maintenance_contents[maintenance_time:]

def extract_maintenance_post_kr():
    pass
