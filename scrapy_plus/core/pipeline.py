#coding:utf-8

class Pipeline(object):
    def process_item(self, item):
        print("[Pipeline]: item data : {}".format(item.data))
