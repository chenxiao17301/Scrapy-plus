#coding:utf-8

# 根据异常判断，导入适合解释器环境的队列类
# try:
#     from Queue import Queue
# except:
#     from queue import Queue

from ..utils.log import logger

from ..conf.default_settings import *
# 根据解释器环境，判断是py2/py3，并导入对应的队列类
#from six.moves.queue import Queue

# 判断用户角色，如果是非分布式，使用Python的队列；如果是分布式，使用Redis的队列
if ROLE == None:
    from six.moves.queue import Queue
    from ..queue.set import NormalFilterSet as Set
    logger.info("ROLE is {}".format(ROLE))

elif ROLE in ['master', 'slave']:
    from ..queue.queue import Queue
    from ..queue.set import RedisFilterSet as Set
    logger.info("ROLE is {}".format(ROLE))
else:
    raise ImportError("Not Support this Role : <{}>".format(ROLE))

import six


class Scheduler(object):
    def __init__(self):
        self.queue = Queue()
        self._filter_set = Set()
        self.total_request = 0



    def add_request(self, request):
        # 请求是否去重的控制，如果不去重，直接将请求加入请求队列
        if request.dont_filter:
            self.queue.put(request)
            self.total_request += 1
        else:
            fp = self._get_fingerprint(request)
            if self._filter_request(fp, request):
                self._filter_set.add_fp(fp)
                self.queue.put(request)
                self.total_request += 1



    def get_request(self):
        try:
            return self.queue.get(False)
        except:
            return False


    def _filter_request(self, fp, request):
        """
            请求去重，并返回判断结果
        """
        # 如果请求的url地址不在去重集合中，那么返回True，表示允许添加到请求队列中
        #if fp not in self._filter_set:
        if not self._filter_set.is_filter(fp):
            return True
        else:
            # 否则，表示重复， 不允许添加
            logger.info("Filter request: [{}] <{}>".format(request.method, request.url))
            return False


    def _get_fingerprint(self, request):
        import w3lib.url
        from hashlib import sha1

        # 对url地址进行规整排序处理
        url = w3lib.url.canonicalize_url(request.url)

        # 将请求方法转为大写处理
        method = request.method.upper()

        # 保证返回一个字典（不管用户有没有传参，面sha1生成数据出错）
        params = request.params if request.params else {}
        params = str(sorted(params.items(), key=lambda x : x[0]))

        formdata = request.formdata if request.formdata else {}
        formdata = str(sorted(formdata.items(), key=lambda x : x[0]))


        sha1_data = sha1()
        # update()必须接收一个字节码字符串  python2 str unicode, python3 bytes str
        sha1_data.update(self._get_utf8_str(url))
        sha1_data.update(self._get_utf8_str(method))
        sha1_data.update(self._get_utf8_str(params))
        sha1_data.update(self._get_utf8_str(formdata))

        # 生成一个16进制数的字符串，做为请求指纹
        fp = sha1_data.hexdigest()

        return fp

    # 判断字符串的类型，如果是Unicode则转为utf-8
    def _get_utf8_str(self, string):
        if six.PY2:
            if isinstance(string, str):
                return string
            else:
                return string.encode("utf-8")
        else:
            if isinstance(string, bytes):
                return string
            else:
                return string.encode("utf-8")


# 不可逆加密算法

# python_obj = json.loads(json_str)
# json_str = json.dumps(python_obj)


