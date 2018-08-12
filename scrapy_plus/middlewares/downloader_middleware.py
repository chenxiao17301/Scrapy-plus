#coding:utf-8


class DownloaderMiddleware(object):
    """
        下载中间件：Downloader提交给Enigma的Response，或Engine提交给Downloader的Request
    """
    def process_request(self, request):
        print("[DownloaderMiddleware] Process Reqeuest <{}>".format(request.url))
        return request


    def process_response(self, response):
        print("[DownloaderMiddleware] Process Response <{}>".format(response.url))
        return response
