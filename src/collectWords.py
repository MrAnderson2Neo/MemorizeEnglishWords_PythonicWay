import urllib.request
from bs4 import BeautifulSoup
import sys
import io
import re
from urllib.parse import urljoin

SITES = {
    "news":{
        "bbc":"http://www.bbc.com/news",         #class = "block-link__overlay-link"
        "yahoo news":"http://news.yahoo.com/",   #class = "Td(n)"
        "google news":"http://news.google.com/",  #class = "article""
        "huffingtonpost":"http://www.huffingtonpost.com/",
        "cnn":"http://www.cnn.com/",
        "nytimes":"http://www.nytimes.com/",
        "fox":"http://www.foxnews.com/",
        "nbc":"http://www.nbcnews.com/",
        "mail online":"http://www.dailymail.co.uk/",
        "washington post":"http://www.washingtonpost.com/",
        "guardian":"http://www.theguardian.com/",
    },
    "blog":{
        "quora":"https://www.quora.com/",
        "medium":"https://medium.com/",
    },
}
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')



def getParas(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    }
    request = urllib.request.Request(url,headers = headers)
    response = urllib.request.urlopen(request)
    content = response.read()
    soup = BeautifulSoup(content,"html.parser")
    paras = soup.find_all("p")
    return paras

def getInitUrl(rootUrl,classPattern):
    baseURL = rootUrl
    urls = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    }
    request = urllib.request.Request(rootUrl,headers=headers)
    response = urllib.request.urlopen(request).read()
    content = response.decode("utf-8")
    soup = BeautifulSoup(content,"html.parser")
    for link in soup.find_all(class_ = classPattern):
        urls.append(urljoin(baseURL,link.get('href')))
    print(urls)
    return urls


def storeWords(paras):
    with open("articles.txt","a+") as f:    
        for para in paras:
            try:
                f.write(para.string)
            except:
                continue
def iterSites(SITES):
    for tag in list(SITES.keys()):
        for siteName in list(SITES[tag].keys()):
            if not isinstance(SITES[tag][siteName],dict):
                yield SITES[tag][siteName]
allSites = list(iterSites(SITES))



if __name__ == "__main__":
    urls = getInitUrl("https://www.yahoo.com/news/","Fw(b)")
    print(urls)
    for url in urls:
        paras = getParas(url)
        storeWords(paras)
