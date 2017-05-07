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

7.在文章详情页面直接获取p标签会得到很多没有必要的内容，如何改进？（如何获取有价值的内容？？？）
bbc的文章正文全部都在：class="story-body"中
8.需要一个总调度器、url管理器

9.有时候出现：在获取文章内容的时候出错： <class 'Exception'>  :  'NoneType' object has no attribute 'find_all'
            在保持文章的时候出错： <class 'Exception'>  :  'NoneType' object is not iterable的问题时是因为抓取的文章不是我们需要的，没有正文，别方~~~
10.http://www.huffingtonpost.com/ 的文章链接有点复杂啊，而且有很多页面是视频，而且这些还和一般文章链接是一样的。
"""
SITES = {

    # "bbc":{
    #     "url":"http://www.bbc.com",
    #     "pattern":"(\/news\/[a-zA-Z-]+-[0-9]+)",
    #     "article-area":"story-body",
    # },
    # "huffingtonpost":{
    #     "url":"http://www.huffingtonpost.com/",
    #     "pattern":"http:\/\/www.huffingtonpost.com\/[a-zA-Z]+\/[a-zA-Z0-9-_?&;=]+",
    #     "article-area":"entry__text",
    # },
    # "guardian":{
    #     "url":"http://www.theguardian.com/",
    #     "pattern":"https:\/\/www.theguardian.com\/[a-zA-Z0-9-]+\/[A-Za-z0-9]+\/[a-zA-Z0-9]+[\/a-zA-Z0-9-]+",
    #     "article-area":"content__article-body",
    # },
    # "aol":{
    #     "url":"https://www.aol.com/",
    #     "pattern":"https:\/\/www.aol.com\/article\/[A-Za-z0-9]+\/[a-zA-Z0-9]+[\/a-zA-Z0-9-]+",
    #     "article-area":"article-content",
    # },
    # "china daily":{
    #     "url":"http://www.chinadaily.com.cn/",
    #     "pattern":"[a-z]{5,10}\/[0-9-\/]+\/[a-zA-Z0-9_\/]+\.htm",
    #     "article-area":"lft_art",
    # },
    "washingtonpost":{
        "url":"https://www.washingtonpost.com/",
        "pattern":"https:\/\/www.washingtonpost.com\/[a-z]{3,10}\/[a-zA-Z\/0-9_-]+\/[a-zA-Z0-9-_]+",
        "article-area":"block",
    }
}


excludeWords = ["Messenger","Facebook","Twitter","Pinterest","WhatsApp","LinkedIn","Copy this link"]
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
def getInitUrl(rootUrl,pattern):
    baseURL = rootUrl
    urls = []
    count = 0
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    }
    request = urllib.request.Request(rootUrl,headers=headers)
    try:
        response = urllib.request.urlopen(request,timeout = 1000).read()
        content = response.decode("utf-8")
        shortUrls =  re.findall(pattern, content)
        for shortUrl in shortUrls:
            count +=1
            url = urllib.request.urljoin(baseURL,shortUrl)
            urls.append(url)
        print(count)
        return urls
    except Exception as e:
        print("在获取文章列表的时候出错：",Exception," : ",e)


def getParas(url,articleArea):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    }
    request = urllib.request.Request(url,headers = headers)
    try:
        response = urllib.request.urlopen(request,timeout = 1000)
        content = response.read()
        soup = BeautifulSoup(content,"html.parser")
        paras = soup.find(class_ = articleArea).find_all("p")
        title = soup.title.string
        print("正在爬取文章： " + title + "   " + url)
        return paras
    except Exception as e:
        print("在获取文章内容的时候出错：",Exception," : ",e)



def storeWords(paras):
    with open("collection.txt","a+",encoding="utf-8") as f:
        try:
            for para in paras:
                if para.string and para.sting not in excludeWords:
                    f.write(para.string)
                    f.write("\n")
            f.write("------------------------------------------用于测试，分隔不同的文章---------------------------------------------------------\n")
        except Exception as e:
            print("在保持文章的时候出错：",Exception," : ",e)



for site in SITES.keys():
    print("正在获取 "+ site + " 网站上的文章列表")
    url,pattern,artilceArea = SITES[site]["url"],SITES[site]["pattern"],SITES[site]["article-area"]
    urls = set(getInitUrl(url,pattern))
    for url in urls:
        # print(url)
        paras = getParas(url,artilceArea)
        storeWords(paras)
