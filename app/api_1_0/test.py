# @Time    : 2019/6/30 21:15
# @Author  : young
from . import api


@api.route("/")
def index():
    return "hello world"
