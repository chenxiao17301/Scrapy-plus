#coding:utf-8

from scrapy_plus.core.engine import Engine

# # 导入所有爬虫类
#from spiders.baidu import BaiduSpider
# from spiders.douban import DoubanSpider

# # 导入所有管道类
# from pipelines import BaiduPipeline1, BaiduPipeline2, DoubanPipeline1, DoubanPipeline2

# # 导入所有中间件类
# from middlewares import SpiderMiddleware1, SpiderMiddleware2, DownloaderMiddleware1, DownloaderMiddleware2


# import settings

# import importlib

from scrapy_plus.http.request import Request

import redis
import time

def main():
    # 1. 定时发送请求
    engine = Engine()
    while True:
        engine.start()
        time.sleep(3)


    # redis的 list 队列 相当于 python的 queue 队列
    # python的队列: FIFO

    # redis的队列： lpush + rpop : FIFO
    #              rpush + lpop : FIFO


    # key = "reqeust_queue"
    # #data = "hello world"
    # request = Request("http://www.baidu.com/")


# json.loads() : json字符串 -> python对象
# json.dumps() : Python对象 -> json字符串

# pickle.dumps() : Python对象 -> 二进制字符串
# pickle.loads() : 二进制字符串 -> python对象

    # import pickle

    # data = pickle.dumps(request)

    # redis_cli.lpush(key, data)
    # request = pickle.loads(redis_cli.rpop(key))
    # print(request)
    # print(type(request))





    # 构建自定义的Spider对象
    # baidu_spider = BaiduSpider()
    # douban_spider = DoubanSpider()
    # # 将对象做为参数传给Engine


    #getattr(对象，属性)
    #getattr(文件绝对路径，文件里的类)



    # # 构建需要执行的多个爬虫的字典
    # spiders = {
    #     BaiduSpider.name : BaiduSpider(),
    #     DoubanSpider.name : DoubanSpider()
    # }

    # # # 自定义管道
    # pipelines = [
    #     BaiduPipeline1(),
    #     BaiduPipeline2(),
    #     DoubanPipeline1(),
    #     DoubanPipeline2(),
    # ]

    # # 自定义爬虫中间件
    # spider_middlewares = [
    #     SpiderMiddleware1(),
    #     SpiderMiddleware2()
    # ]

    # # 自定义下载中间件
    # downloader_middlewares = [
    #     DownloaderMiddleware1(),
    #     DownloaderMiddleware2()
    # ]


    # engine = Engine(
    #     spiders = spiders,
    #     pipelines = pipelines,
    #     spider_mids = spider_middlewares,
    #     downloader_mids = downloader_middlewares
    # )


if __name__ == "__main__":
    main()
