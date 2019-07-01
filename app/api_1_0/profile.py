# @Time    : 2019/7/1 17:57
# @Author  : young
import re

from flask import request, jsonify, current_app, session, g
from sqlalchemy.exc import IntegrityError

from . import api
from ..utils.response_code import RET
from .. import redis_store, db
from ..models import User


@api.route("/users", methods=["POST"])
def register():
    req_dict = request.get_json()

    mobile = req_dict.get("mobile")
    sms_code = req_dict.get("sms_code")
    password = req_dict.get("password")
    password2 = req_dict.get("password2")

    if not all([mobile, sms_code, password, password2]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    if not re.match(r"1[345678]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")

    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg="两次密码不一致")

    try:
        real_sms_code = redis_store.get("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="读取真实验证码异常")

    if real_sms_code is None:
        return jsonify(errno=RET.NODATA, errmsg="短音验证码失败")

    try:
        redis_store.delete("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)

    real_sms_code = real_sms_code.decode()
    if real_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误")

    user = User(name=mobile, mobile=mobile, password=password)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    session["name"] = mobile
    session["mobile"] = mobile
    session["user_id"] = user.id

    g.user_id = user.id

    return jsonify(errno=RET.OK, errmsg="注册成功")
