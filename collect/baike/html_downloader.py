import urllib.request
import urllib.parse

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
}


class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None

        req = urllib.request.Request(url,headers = headers)
        response = urllib.request.urlopen(req, timeout = 1000)
        if response.getcode() != 200:
            return None
        return  response.read().decode("utf-8")



