#coding:utf-8


class SpiderMiddleware(object):
    """
        爬虫中间件：在Spider提交数据给Engine时工作
    """
    def process_request(self, request):
        print("[SpiderMiddleware] Process Reqeuest <{}>".format(request.url))
        return request


    def process_item(self, item):
        print("[SpiderMiddleware] Process Item <{}>".format(type(item)))

        return item
