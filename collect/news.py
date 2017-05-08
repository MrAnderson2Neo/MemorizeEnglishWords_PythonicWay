import re
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import threading
import io
import sys

"""
issue:

2.nytimes需要翻墙和付费的怎么办？
5.medium居然找不到文章的a标签！！！               
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
    # "guardian": {
    #     "url": "http://www.theguardian.com/",
    #     "pattern": "https:\/\/www.theguardian.com\/[a-zA-Z]+\/[0-9]+\/[a-zA-Z]+[\/a-zA-Z0-9-]+", #politics/2017/mar/05/xxx-xxx-xxx-xxx
    #     "article-area": "content__article-body",
    # },
    # "aol":{
    #     "url":"https://www.aol.com/",
    #     "pattern":"https:\/\/www.aol.com\/article\/[A-Za-z0-9]+\/[a-zA-Z0-9]+[\/a-zA-Z0-9-]+",
    #     "article-area":"article-content",
    # },
    "china daily":{
        "url":"http://www.chinadaily.com.cn/",
        "pattern":"[a-z\/]+\/[0-9-]+\/[0-9]+\/[a-zA-Z0-9_]+\.htm",      #  life/2017-05/08/content_29246312.htm  [a-z\/]+\/[0-9-]+\/[0-9]+[a-zA-Z0-9_]+\.htm
        "article-area":"lft_art",
    },
    # "washingtonpost":{
    #     "url":"https://www.washingtonpost.com/",
    #     "pattern":"https:\/\/www.washingtonpost.com\/[a-z]{3,10}\/[a-zA-Z\/0-9_-]+\/[a-zA-Z0-9-_]+",
    #     "article-area":"block",
    # },
}

excludeWords = ["Messenger", "Facebook", "Twitter", "Pinterest", "WhatsApp", "LinkedIn", "Copy this link"]


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #有这一句会使得测试print语句无法输出？

def makeRequest(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    }
    request = urllib.request.Request(url, headers=headers)
    return request


def makeFullUrls(shortUrls, baseUrl):
    urls = []
    for shortUrl in shortUrls:
        url = urljoin(baseUrl, shortUrl)
        urls.append(url)
    return urls


def getInitUrl(rootUrl, pattern):
    request = makeRequest(rootUrl)
    content = urllib.request.urlopen(request, timeout=1000).read().decode("utf-8")
    try:
        shortUrls = re.findall(pattern, content)
        urls = makeFullUrls(shortUrls, rootUrl)
        return urls
    except Exception as e:
        print("在获取文章列表的时候出错：", Exception, " : ", e)


def getContentAndOtherUrls(url, articleArea,pattern):
    request = makeRequest(url)
    try:
        content = urllib.request.urlopen(request, timeout=1000).read().decode("utf-8")
        soup = BeautifulSoup(content, "html.parser")
        title = soup.title.string
        print("正在爬取文章： " + title + "   " + url)
        article = getContent(soup,articleArea)
        urls = getOtherUrls(content,pattern,url)
        return  article,urls
    except Exception as e:
        print(Exception," : ",e)

def getContent(soup,articleArea):
    articleSegment = soup.find(class_=articleArea)
    if articleSegment:
        content = articleSegment.find_all("p")
        if content:  # 确保content不为空，这样就不用到下一步存储了
            return content
            # try:
            #     content = soup.find(class_=articleArea).find_all("p")
            #     return content
            # except Exception as e:
            #     print("此页面不属于文章正文页，没有你想要的内容，", Exception, " : ", e)

def getOtherUrls(content,pattern,baseUrl):
    try:
        shortUrls = re.findall(pattern, content)
        urls = makeFullUrls(shortUrls, baseUrl)
        return urls
    except Exception as e:
        print("在获取文章列表的时候出错：", Exception, " : ", e)

def storeWords(article):
    with open("test.txt", "a+", encoding="utf-8") as f:
        # 为什么使用下面的这部分文件无法保持？？？？
        # for line in content:
        #     if line.content:      #确保line（就是以前的p标签）里面是有内容的
        #         f.write(content.string)
        #         f.write("\n")
        #         f.close()
        try:
            for para in article:
                if para.string and para.sting not in excludeWords:
                    print("正在保持文章")
                    f.write(para.string)
                    f.write("\n")
        except Exception as e:
            print("在保持文章的时候出错：", Exception, " : ", e)


# 以下是多线程尝试：
# def main(url,pattern,articleArea):
#         urls = set(getInitUrl(url, pattern))  # 用set除去重复元素
#         for url in urls:
#             # print(url)
#             content = getContent(url, articleArea)
#             storeWords(content)
#
# def makeThreads():
#     threads = []
#     for site in SITES.keys():
#         print("正在获取 " + site + " 网站上的文章列表")
#         url, pattern, artilceArea = SITES[site]["url"], SITES[site]["pattern"], SITES[site]["article-area"]
#         t = threading.Thread(target = getInitUrl, args=(url,pattern,artilceArea))
#         threads.append(t)
#     return threads

# if __name__ == "__main__":
#     threads = makeThreads()
#     print(threads)
#     for t in threads:
#         t.setDaemon(True)
#         t.start()



# def magic(urls):
#     for url in urls:
#         # print(url)
#         article, urlsFromArticle = getContentAndOtherUrls(url, artilceArea,
#             pattern)  # 这里有一个接口，在文章详情页面的操作，文章详情页面也是有其他文章链接的，如何获取，有什么好的设计模式？
#         urlsFromArticle = set(urlsFromArticle)
#         if urlsFromArticle:
#             for url in urlsFromArticle:
#                 if url not in URLS:
#                     print("发现了新的url： " + url)
#                     URLS.append(url)
#         if article:  # 如果getContent()没有得到content，就会返回None，这里检查一下
#             storeWords(article)

if __name__ == "__main__":
    URLS = []
    for site in SITES.keys():
        print("正在获取 " + site + " 网站上的文章列表")
        url, pattern, artilceArea = SITES[site]["url"], SITES[site]["pattern"], SITES[site]["article-area"]
        urls = set(getInitUrl(url, pattern))  # 用set除去重复元素
        for url in urls:
            # print(url)
            try:
                article,urlsFromArticle = getContentAndOtherUrls(url, artilceArea,pattern)  # 这里有一个接口，在文章详情页面的操作，文章详情页面也是有其他文章链接的，如何获取，有什么好的设计模式？
                if urlsFromArticle:
                    urlsFromArticle = set(urlsFromArticle)
                    for url in urlsFromArticle:
                        if url not  in URLS:
                            print("发现了新的url： " + url )
                            URLS.append(url)
                if article:  # 如果getContent()没有得到content，就会返回None，这里检查一下
                    storeWords(article)
            except:
                pass
        while 1:
            for url in URLS:
                try:
                    article,urlsFromArticle = getContentAndOtherUrls(url, artilceArea,pattern)  # 这里有一个接口，在文章详情页面的操作，文章详情页面也是有其他文章链接的，如何获取，有什么好的设计模式？
                    if urlsFromArticle:
                        urlsFromArticle = set(urlsFromArticle)
                        for url in urlsFromArticle:
                            if url not  in URLS:
                                print("发现了新的url： " + url )
                                URLS.append(url)
                    if article:  # 如果getContent()没有得到content，就会返回None，这里检查一下
                        storeWords(article)
                except:
                    pass

