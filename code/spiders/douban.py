#coding:utf-8

# 导入框架的Spider类和Request类和Item类
from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.items import Item

class DoubanSpider(Spider):

    name = "douban"
    # start_urls = [
    #     "http://www.baidu.com/",
    #     "http://www.itcast.cn/",
    #     "http://www.baidu.com/"
    # ]
    start_urls = ["https://movie.douban.com/top250?start=" + str(page) for page in range(0, 226, 25)]

    def start_requests(self):
        for url in self.start_urls:
            # 不指定callback，默认响应由parse解析
            yield Request(url, dont_filter = True)
            # yield Request(url,callback="parse")


    def parse(self, response):
        # item = {}
        # item['title'] = response.xpath("//head/title/text()")[0]
        # yield Item(item)

        node_list = response.xpath("//div[@class='hd']")[:3]
        for node in node_list:
            item = {}
            item['page_title'] = node.xpath("./a/span/text()")[0]
            item['page_link'] = node.xpath("./a/@href")[0]
            # Item数据，交给管道
            yield Item(item)
            # Request对象，Engine发送，并由指定的回调函数parse_page解析
            # 在提交请求时，url地址字符串不能为Unicode，否则添加到Redis队列试，pickle序列化会出错
            #yield Request(item['page_link'].encode("utf-8"), callback="parse_page")


    def parse_page(self, response):
        print("[parse_page] : [{}] <{}>".format(response.status_code, response.url))
        yield Item({})
