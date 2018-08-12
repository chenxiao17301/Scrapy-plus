#coding:utf-8

import re
import json

from lxml import etree

class Response(object):
    """
        框架提供的响应类，用来保存HTTP响应相关的参数
    """
    def __init__(self, url, body, text, headers, status_code, encoding, request):
        self.url = url  # 响应的url地址
        self.body = body    # 响应的响应体内容
        self.text = text    # Unicode网页字符串
        self.headers = headers  # 响应的报头
        self.status_code = status_code  # 响应的状态码
        self.encoding = encoding # 响应的字符编码
        self.request = request  # 响应对应的请求对象


    def xpath(self, rule):
        html_obj = etree.HTML(self.body)
        return html_obj.xpath(rule)


    def re_findall(self, rule, string=None):
        """
            通过string参数控制，可以处理response.body 或 其他字符串的解析
        """
        if string is None:
            return re.findall(rule, self.body)
        else:
            return re.findall(rule, string)

    @property
    def json(self):
        try:
            return json.loads(self.body)
        except Exception as e:
            raise e

