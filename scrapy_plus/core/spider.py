#coding:utf-8

from ..http.request import Request
from ..items import Item

class Spider(object):

    #start_url = "http://www.baidu.com/"
    start_urls = []


    def start_requests(self):
        """
            返回第一个入口请求给引擎
        """
        for url in self.start_urls:
            yield Request(url)


    def parse(self, response):
        raise Exception("Must overwrite parse function!")
        # #content = {"content" : response.body}
        # content = response.body

        # item = Item(content)
        # return item
