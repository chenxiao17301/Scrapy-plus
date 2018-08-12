#coding:utf-8

import requests
import chardet

from ..http.response import Response

from ..utils.log import logger

class Downloader(object):

    def send_request(self, request):
        logger.info("[Downloader] : Request [{}] <{}>".format(request.method, request.url))

        if request.method.upper() == "GET":
            response = requests.get(
                url = request.url,
                headers = request.headers,
                params = request.params,
                proxies = request.proxy

            )

        elif request.method.upper() == "POST":
            response = requests.post(
                url = request.url,
                headers = request.headers,
                data = request.formdata,
                proxies = request.proxy

            )
        else:
            # 如果请求方法不支持，则抛出异常
            raise Exception("Not Support method <{}>".format(request.method))


        logger.info("[Downloader]: Response [{}] <{}>".format(response.status_code, response.url))

        # 构建响应对象，返回给引擎
        return Response(
                url = response.url,
                body = response.content,
                #text = response.content.decode(chardet.detect(response.content)['encoding']),
                text = "",
                headers = response.headers,
                status_code = response.status_code,
                encoding = chardet.detect(response.content)['encoding'],
                request = request,
        )

