#coding:utf-8


#from scrapy_plus.core.pipeline import Pipeline
#class BaiduPipeline(Pipeline):

# 导入两个爬虫类，用来判断item数据所属spider，并分别处理
from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider



class BaiduPipeline1(object):
    def process_item(self, item, spider):
        if isinstance(spider, BaiduSpider):
            print("[BaiduPipeline1]: item data : {}".format(type(item.data)))

        return item


class BaiduPipeline2(object):
    def process_item(self, item, spider):
        if isinstance(spider, BaiduSpider):
            print("[BaiduPipeline2]: item data : {}".format(type(item.data)))

        return item


#class BaiduPipeline(Pipeline):
class DoubanPipeline1(object):
    def process_item(self, item, spider):
        if isinstance(spider, DoubanSpider):
            print("[DoubanPipeline1]: item data : {}".format(type(item.data)))

        return item

class DoubanPipeline2(object):
    def process_item(self, item, spider):
        if isinstance(spider, DoubanSpider):
            print("[DoubanPipeline2]: item data : {}".format(type(item.data)))

        return item
