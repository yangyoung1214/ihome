# @Time    : 2019/7/1 20:35
# @Author  : young
import re

from flask import current_app, jsonify, request, session, g

from . import api
from .. import redis_store, db, constants
from ..utils.response_code import RET
from ..models import User


@api.route("/sessions", methods=["POST"])
def login():
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")

    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数缺失")

    if not re.match(r"1[345678]\d{9}", mobile):
        return jsonify(errno=RET.DATAERR, errmsg="手机号格式错误")

    user_ip = request.remote_addr

    try:
        access_nums = redis_store.get("access_num_%s" % user_ip)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg="错误次数过多，请稍后重试")

    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")

    if user is None or not user.check_password(password):
        try:
            redis_store.incr("access_num_%s" % user_ip)
            redis_store.expire("access_num_%s" % user_ip, constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)

        return jsonify(errno=RET.NODATA, errmsg="用户名或密码错误")

    session["name"] = user.name
    session["mobile"] = user.mobile
    session["user_id"] = user.id
    g.user_id = user.id

    return jsonify(errno=RET.OK, errmsg="登陆成功")


@api.route("/sessions")
def check_login():
    name = session.get("name")

    if name is None:
        return jsonify(errno=RET.SESSIONERR, errmsg="false")
    else:
        return jsonify(errno=RET.OK, errmsg="true", datas={"name": name})


@api.route("/sessions", methods=["DELETE"])
def logout():
    csrf_token = session.get("csrf_token")
    session.clear()
    session["csrf_token"] = csrf_token
    return jsonify(errno=RET.OK, errmsg="成功退出")
