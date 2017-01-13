import requests
from bs4 import BeautifulSoup
from faker import Factory


class ChinazClient:
    """客户端 查询站长之家域名是否已经备案"""

    def query_domain(self):
        fake = Factory.create()
        ua = fake.user_agent()
        headers = {'user-agent': ua}
        r = requests.get('http://127.0.0.1/', headers=headers)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, "html5lib")
        print(soup.prettify())
