# @Time    : 2019/7/1 9:54
# @Author  : young
from werkzeug.routing import BaseConverter


# 定义正则转换器
class ReConverter(BaseConverter):
    def __init__(self, url_map, regex):
        super().__init__(url_map)
        self.regex = regex
