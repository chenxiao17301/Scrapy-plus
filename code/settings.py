#coding:utf-8


# 覆盖了框架default_settings里的同名配置
DEFAULT_LOG_FILENAME = 'myspider.log'    # 默认日志文件名称


SPIDERS = [
    "spiders.baidu.BaiduSpider",
    "spiders.douban.DoubanSpider",
]


PIPELINES = [
    "pipelines.BaiduPipeline1",
    "pipelines.DoubanPipeline1",
]

# SPIDER_MIDDLEWARES = [
#     "middlewares.SpiderMiddleware1",
#     "middlewares.SpiderMiddleware2"
# ]

# DOWNLOADER_MIDDLEWARES = [
#     "middlewares.DownloaderMiddleware1",
#     "middlewares.DownloaderMiddleware2"
# ]

# 并发类型
# ASYNC_TYPE = "thread"
ASYNC_TYPE = "coroutine"
# 并发数量，对应Enginefor迭代中的 线程数、协程数量
ASYNC_COUNT = 3

# 启用分布式，请求队列在Redis数据库中
# ROLE = "master"
ROLE = "slave"

#非分布式，请求队列在Queue
# ROLE = None


# redis请求队列默认配置
REDIS_QUEUE_NAME = 'request_queue'
REDIS_QUEUE_HOST = 'localhost'
REDIS_QUEUE_PORT = 6379
REDIS_QUEUE_DB = 0


# Redis指纹集合配置参数
REDIS_SET_NAME = "fingerprint_set"
REDIS_SET_HOST = "127.0.0.1"
REDIS_SET_PORT = 6379
REDIS_SET_DB = 0

