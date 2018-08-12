#coding:utf-8

from datetime import datetime



from ..http.request import Request
from ..http.response import Response
from ..items import Item

from spider import Spider
from scheduler import Scheduler
from downloader import Downloader
from pipeline import Pipeline

from ..middlewares.downloader_middleware import DownloaderMiddleware
from ..middlewares.spider_middleware import SpiderMiddleware

# 导入日志模块的logger对象，来狐狸日志信息
from ..utils.log import logger

from ..conf.default_settings import *




# 获取settigns的配置信息，选择并发类型
if ASYNC_TYPE == "thread":
    # 导入多进程模块里的线程池
    from multiprocessing.dummy import Pool
    logger.info("[Async Type]: {}".format(ASYNC_TYPE))

elif ASYNC_TYPE == "coroutine":
    from ..async.coroutine import Pool
    logger.info("[Async Type]: {}".format(ASYNC_TYPE))

else:
    raise Exception("Not Support Async Type: {}".format(ASYNC_TYPE))


import time



class Engine(object):
    """
        框架核心类，负责调度各个模块的功能执行
        提供了外部访问方法 start() 用来启动整个框架运行
    """
    def __init__(self):
        #self.spider = Spider()
        #self.spiders = spiders  # spiders 是一个包含东哥爬虫对象的字典
        self.spiders = self._auto_import_module_cls(SPIDERS, True)

        self.scheduler = Scheduler()
        self.downloader = Downloader()

        #self.pipelines = pipelines
        self.pipelines = self._auto_import_module_cls(PIPELINES)

        #self.downloader_mids = downloader_mids
        self.downloader_mids = self._auto_import_module_cls(DOWNLOADER_MIDDLEWARES)

        #self.spider_mids = spider_mids
        self.spider_mids = self._auto_import_module_cls(SPIDER_MIDDLEWARES)

        self.pool = Pool()
        self.total_response = 0
        self.is_running = True

    def _auto_import_module_cls(self, path_list=[], is_spider=False):
        if is_spider:
            instances = {}
        else:
            instances =  []

        import importlib


        for path in path_list:
            # 获取模块名
            module_name = path[:path.rfind(".")]
            # 获取类名
            class_name = path[path.rfind(".")+1:]

            # 根据模块名获取该模块的绝对路径
            result = importlib.import_module(module_name)

            # 根据模块返回该模块的指定类对象
            # 类对象  cls， 类实例化对象  cls()
            cls = getattr(result, class_name)

            if is_spider:
                # 构建实例化对象
                instances[cls.name] = cls()
            else:
                instances.append(cls())

        return instances


    def start(self):
        # 开始时间
        start = datetime.now()
        logger.info("Start time : {}".format(start))
        logger.info("----"*30)

        self._start_engine()

        # 结束时间
        end = datetime.now()

        logger.info("----"*30)
        logger.info("End time : {}".format(end))
        # 总计运行时间
        logger.info("Useing time : {}".format( (end - start).total_seconds() ))


    def _callback(self, _):
        if self.is_running:
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback)


    def _start_engine(self):
        # master只执行 添加请求，所以total_request会自增，
        # 但是不发送请求total_response不会自增
        if ROLE == "master" or ROLE is None:
            # 将Engine的工作分工，分为两部分：
            # 1 处理start_request请求并存如调度器中
            #self._execute_start_requests()
            self.pool.apply_async(self._execute_start_requests)
            #self._execute_start_requests()

        # slave只发送请求，所以total_response会自增
        # 但是不会添加start_requests()请求，所以total_request不会自增
        if ROLE == "slave" or ROLE is None:
            # 2. 处理请求发送，返回的响应（response) 数据提取（request、item
            for _ in range(ASYNC_COUNT):
                self.pool.apply_async(self._execute_request_response_item, callback=self._callback)
            #self._execute_request_response_item()


        while True:
            time.sleep(0.01)

            if ROLE in ['master', 'slave']:
                continue

            # slave在抓取的过程中，如果提交了新的请求，有可能会导致 解析的响应数 和 提交的请求数 相同
            # while 会判断退出
            if self.scheduler.total_request == self.total_response and self.scheduler.total_request != 0:
                self.is_running = False
                break

        self.pool.close()
        self.pool.join()

        logger.info("Main Thread is over!")


    def _execute_start_requests(self):
        # 将所有爬虫的start_urls里的请求全部放入同一个调度器中
        #[("baidu", baidu_spider), ("douban" : douban_spider)]
        for spider_name, spider in self.spiders.items():
            # 1. 从spider中获取第一批请求，交给调度器
            #request = self.spider.start_requests()
            for request in spider.start_requests():
                # 第一次处理请求时，就添加爬虫名，该爬虫名可以传递到后续提取的请求中
                request.spider_name = spider_name
                # 1.1 将请求交给spider中间件做处理，再返回处理后的请求
                for spider_mid in self.spider_mids:
                    request  = spider_mid.process_request(request, spider)

                self.scheduler.add_request(request)


    def _execute_request_response_item(self):
        # 每次while 循环，处理的都是同一个爬虫下的某一个请求
        #while True:
        # 2. 取出调度器的请求，并交给下载器，下载器返回响应交给spider解析
        request = self.scheduler.get_request()

        if not request:
            #break
            return

        # 获取请求对应的爬虫对象
        spider = self.spiders[request.spider_name]

        # 2.1 将调度器中返回的请求交给下载中间件做预处理，并返回处理后的请求
        for downloader_mid in self.downloader_mids:
            request = downloader_mid.process_request(request, spider)

        response = self.downloader.send_request(request)
        # 2.2 将下载器返回的响应交给下载中间件做预处理，并返回处理后的响应
        for downloader_mid in self.downloader_mids:
            response = downloader_mid.process_response(response, spider)
        #  将响应交给爬虫解析
        #parse_func = self.spider.parse(response)

        #爬虫对象的某个解析方法 parse， parse_page
        #getattr(spider, "parse_page")
        # 动态获取获取爬虫对象的该请求指定的回调函数，并将响应传入回调函数解析



        callback_func = getattr(spider, request.callback)
        parse_func = callback_func(response)




        for item_or_request in parse_func:
            # 3. 判断解析结果，如果是请求继续交给调度器；如果是item数据交给管道
            if isinstance(item_or_request, Request):
                item_or_request.spider_name = spider.name

                for spider_mid in self.spider_mids:
                    item_or_request  = spider_mid.process_request(item_or_request, spider)

                self.scheduler.add_request(item_or_request)

            elif isinstance(item_or_request, Item):
                for spider_mid in self.spider_mids:
                    item_or_request  = spider_mid.process_item(item_or_request, spider)

                for pipeline in self.pipelines:
                    item_or_request = pipeline.process_item(item_or_request, spider)
            else:
                raise Exception("Not support data type : <{}>".format(type(item_or_request)))


        self.total_response += 1


