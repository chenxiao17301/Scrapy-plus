#coding:utf-8


from gevent.pool import Pool as BasePool
import gevent.monkey
gevent.monkey.patch_all()


class Pool(BasePool):

    def apply_async(self, func, args=None, kwds=None, callback=None):
        return BasePool().apply_async(func, args=(), kwds={}, callback=callback)
        #return super().apply_async(self, func, args=(), kwds={}, callback=None)

    def close(self):
        pass
