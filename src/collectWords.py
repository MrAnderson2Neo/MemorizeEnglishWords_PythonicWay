import urllib.request
from bs4 import BeautifulSoup
import sys
import io
import re
from urllib.parse import urljoin
"""
issue:
1.cnn、mail online的文章的a标签没有class,如何获取连接？也许可以先获取所有链接，然后过滤？只有是cnn站内的链接，并且以.html结尾的才可以？
2.nytimes需要翻墙和付费的怎么办？
3.nbc的a标签是这样的：<a href="/news/world/navy-seal-killed-somalia-idd-15-year-veteran-kyle-milliken-n755836">
                                  <h3 class="item-heading item-heading_md">Warrior Spirit': Pentagon IDs Navy SEAL Killed in Somalia </h3></a>
   区分：外部链接是以http开头的，而内部链接省略了主域名，也许可以这样区分
4.washingtonpost:<a class="" href="https://www.washingtonpost.com/news/retropolis/wp/2017/05/06/discovered-philadelphias-high-tech-totally-natural-plumbing-of-1812/" 
                data-pb-field="web_headline" data-pb-url-field="canonical_url" data-pb-placeholder="Write headline here">Philly’s high-tech, totally organic municipal plumbing — from 1812</a>
 bs怎么通过任意标签选择？比如通过data-dp-filed?或许class为空也可以选择？
5.medium居然找不到文章的a标签！！！               

bbc: class="gs-c-promo-heading nw-o-link-split__anchor gs-o-faux-block-link__overlay-link gel-waterloo-bold"
雅虎不好搞："yahoo news":["http://news.yahoo.com/","Td(n)"] ,a标签太乱了！！考虑使用re，不用bs

6.china daily a标签没有clasa
7.在文章详情页面直接获取p标签会得到很多没有必要的内容，如何改进？（如何获取有价值的内容？？？）
"""
SITES = {
    # "bbc":["http://www.bbc.com/news","gs-c-promo-heading"],
    # "huffingtonpost":["http://www.huffingtonpost.com/","bn-card-headline"],
    # "guardian":["http://www.theguardian.com/","u-faux-block-link__overlay"],
    # "quora":["https://www.quora.com/","question_link"],
    # "aol":["https://www.aol.com/","link-out"],
}

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

def getParas(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    }
    request = urllib.request.Request(url,headers = headers)
    try:
        response = urllib.request.urlopen(request,timeout = 1000)
        content = response.read()
        soup = BeautifulSoup(content,"html.parser")
        paras = soup.find_all("p")
        title = soup.title.string
        print("正在爬取文章： " + title + "   " + url)
        return paras
    except:
        print("出了点小问题...没事，接着下一个...")

def getInitUrl(rootUrl,classPattern):
    baseURL = rootUrl
    urls = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    }
    request = urllib.request.Request(rootUrl,headers=headers)
    try:
        response = urllib.request.urlopen(request,timeout = 1000).read()
        content = response.decode("utf-8")
        soup = BeautifulSoup(content,"html.parser")
        for link in soup.find_all(class_ = classPattern):
            urls.append(urljoin(baseURL,link.get('href')))
        return urls
    except:
        print("出了点小问题...没事，接着下一个...")


def storeWords(paras):
    with open("collection.txt","a+",encoding="utf-8") as f:
        for para in paras:
            try:
                f.write(para.string)
                f.write("\n")
            except:
                continue
# def iterSites(SITES):
#     for tag in list(SITES.keys()):
#         for siteName in list(SITES[tag].keys()):
#             if not isinstance(SITES[tag][siteName],dict):
#                 yield SITES[tag][siteName]
# allSites = list(iterSites(SITES))


for site in SITES.keys():
    print("正在获取 "+ site + " 网站上的文章列表")
    url,classPattern = SITES[site][0],SITES[site][1]
    urls = getInitUrl(url,classPattern)
    for url in urls:
        paras = getParas(url)
        storeWords(paras)
