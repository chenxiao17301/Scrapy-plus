#coding:utf-8

# 导入框架的Spider类、Request类和Item类
from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.items import Item

class BaiduSpider(Spider):

    name = "baidu"

    start_urls = [
        "http://www.baidu.com",
        "http://news.baidu.com/",
        "http://www.baidu.com/"
    ]

    def start_requests(self):
        for url in self.start_urls:
            # 不指定callback，默认响应由parse解析
            # 2. dont_filter 请求可以不去重
            yield Request(url, dont_filter=True)
            # yield Request(url,callback="parse")



    def parse(self, response):
        item = {}
        item['title'] = response.xpath("//head/title/text()")[0]
        yield Item(item)

