"""
1.每个词条有一个 id = "bodyContent",包含了正文内容，可以缩小范围。
2.词条页面url很统一： /wiki/Multi-paradigm_programming_language
3.为什么有些p标签的内容无法保存？
4.应该重构一下代码：分为两部分：第一部分专注于获取相关url，第二部分专注于保持内容
"""
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

TOPICS = {
    "python": "https://en.wikipedia.org/wiki/Python_(programming_language)",
}

pattern = "\/wiki\/[a-zA-Z0-9_\(\)]+"
baseUrl = "https://en.wikipedia.org/wiki"


def getBodyContent(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    }
    req = urllib.request.Request(url,headers = headers)
    try:
        response = urllib.request.urlopen(req)
        content = response.read().decode("utf-8")
        soup = BeautifulSoup(content, "html.parser")
        bodyContent = soup.find(id="bodyContent")
        title = soup.find(id = "firstHeading").string
        print("正在爬取词条： " + title + "   " + url)
        return bodyContent
    except:
        pass


def getWikis(bodyContent, baseUrl):
    bodyContent = str(bodyContent)
    URLS = []
    wikis = re.findall(pattern, bodyContent)
    for wiki in wikis:
        fullWikiUrl = urllib.parse.urljoin(baseUrl, wiki)
        if fullWikiUrl not in URLS:
            URLS.append(fullWikiUrl)
    return URLS


def storeWikiContent(bodyContent, topic):  # 接口：bodyContent是一个soup对象
    paras = bodyContent.find_all("p")
    with open("wikipedia" + "-" + topic + ".txt", "a+", encoding="utf-8") as f:
        for para in paras:
            if para:
                f.write(para.get_text())
                f.write("\n")
    print("成功保持词条的内容！")


url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
topic = "python"

bodyContent = getBodyContent(url)
wikiUrls = set(getWikis(bodyContent, baseUrl))
for wikiUrl in wikiUrls:
    bodyContent = getBodyContent(wikiUrl)
    if bodyContent:
        storeWikiContent(bodyContent, topic)
    wikiUrls = getWikis(bodyContent, baseUrl)
    for wikiUrl in wikiUrls:
        bodyContent = getBodyContent(wikiUrl)
        if bodyContent:
            storeWikiContent(bodyContent, topic)
            wikiUrls = getWikis(bodyContent, baseUrl)
        for wikiUrl in wikiUrls:
            bodyContent = getBodyContent(wikiUrl)
            if bodyContent:
                storeWikiContent(bodyContent, topic)
                wikiUrls = getWikis(bodyContent, baseUrl)

