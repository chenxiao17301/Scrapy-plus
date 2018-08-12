#coding:Utf-8


class Item(object):
    """
        框架设计的Item类，提供了data属性保存解析后的数据
    """
    def __init__(self, data):
        # 在设计类时，如果某个属性只允许查看，不允许修改。
        self._data = data

    @property
    def data(self):
        return self._data
