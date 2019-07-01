# @Time    : 2019/6/30 21:14
# @Author  : young
from flask import Blueprint

api = Blueprint("api_1_0", __name__)

from . import verify_code, profile, passport