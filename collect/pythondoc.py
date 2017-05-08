import urllib.request
from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup

rootUrl = "https://docs.python.org/3/index.html"
pattern1 = "[a-z-\/]+\.html"
pattern2 = "[a-z-]+\.html"

def getContent(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",

    }
    req = urllib.request.Request(url,headers = headers)
    response = urllib.request.urlopen(req,timeout = 1000)
    content = response.read().decode("utf-8")
    return content

def getUrls(content):
    urls = []
    soup = BeautifulSoup(content,"html.parser")
    linksSeg = soup.find(class_ = "toctree-wrapper")
    segUrls = re.findall(pattern2,str(linksSeg))
    for shortUrl in segUrls:
        url = urljoin(rootUrl,shortUrl)
        if url not in urls:
            urls.append(url)
    return urls

def getUrlsFromIndexPage(rootUrl):
    urls = []
    content = getContent(rootUrl)
    segUrl = re.findall(pattern1,content)
    for shortUrl in segUrl:
        url = urljoin(rootUrl,shortUrl)
        if url not in urls:
            urls.append(url)
    return urls

if __name__ == "__main__":
    urlsOfArticlePages = []
    diffPartUrls = getUrlsFromIndexPage(rootUrl)
    for url in diffPartUrls:
        content = getContent(url)
        subUrls = getUrls(content)
        for url in subUrls:
            if url not in urlsOfArticlePages:
                urlsOfArticlePages.append(url)
    for url in urlsOfArticlePages:
        content = getContent(url)
        if content:
            soup = BeautifulSoup(content,"html.parser")
            pTags = soup.find_all("p")
            for pTag in pTags:
                if pTag.string:
                    with open ("../files/pythondoc.txt","w+",encoding="utf-8") as f: 
                        f.write(pTag.string)
                        f.write("\n")
     
    
