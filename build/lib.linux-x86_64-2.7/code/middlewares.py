#coding:utf-8

# 爬虫中间件
class SpiderMiddleware1(object):
    """
        爬虫中间件：在Spider提交数据给Engine时工作
    """
    def process_request(self, request, spider):
        print("[SpiderMiddleware1] Process Reqeuest <{}>".format(request.url))
        return request

    def process_item(self, item, spider):
        print("[SpiderMiddleware1] Process Item <{}>".format(type(item)))
        return item


class SpiderMiddleware2(object):
    """
        爬虫中间件：在Spider提交数据给Engine时工作
    """
    def process_request(self, request, spider):
        print("[SpiderMiddleware2] Process Reqeuest <{}>".format(request.url))
        return request


    def process_item(self, item, spider):
        print("[SpiderMiddleware2] Process Item <{}>".format(type(item)))
        return item



# 下载中间件
class DownloaderMiddleware1(object):
    """
        下载中间件：Downloader提交给Enigma的Response，或Engine提交给Downloader的Request
    """
    def process_request(self, request, spider):
        print("[DownloaderMiddleware1] Process Reqeuest <{}>".format(request.url))
        return request


    def process_response(self, response, spider):
        print("[DownloaderMiddleware1] Process Response <{}>".format(response.url))
        return response


class DownloaderMiddleware2(object):
    """
        下载中间件：Downloader提交给Enigma的Response，或Engine提交给Downloader的Request
    """
    def process_request(self, request, spider):
        print("[DownloaderMiddleware2] Process Reqeuest <{}>".format(request.url))
        return request


    def process_response(self, response, spider):
        print("[DownloaderMiddleware2] Process Response <{}>".format(response.url))
        return response





