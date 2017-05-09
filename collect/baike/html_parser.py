import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class HtmlParser(object):

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all("a",href = re.compile(r"/item/[\u4E00-\u9FA5A-Za-z0-9/_]+"))
        for link in links:
            new_url = link("href")
            new_full_url = urljoin(page_url,new_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}
        res_data['url'] = page_url
        # < dd class ="lemmaWgt-lemmaTitle-title" > < h1 > Python < / h1 >
        title_node = soup.find("dd",class_  = "lemmaWgt-lemmaTitle-title").find("h1")
        res_data["title"] = title_node.get_text()
        summary_node = soup.find("div",class_  = "lemma-summary")
        res_data['summary'] = summary_node.get_text()
        return res_data


    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont,"html.parser")
        new_urls = self._get_new_urls(page_url,soup)
        new_data = self._get_new_data(page_url,soup)
        return new_urls,new_data

